"""The two places Claude Code runs runway: a UserPromptSubmit hook and a status line segment.

UserPromptSubmit
    Predicts the prompt before it runs. When it may not finish before the
    5-hour limit (or on every prompt, with gate "always"), it blocks the prompt
    and shows the estimate; the prompt never reaches Claude, so this costs
    nothing. Sending the same text again within confirm_seconds runs it.
    Otherwise it appends the prediction to predictions.jsonl and shows
    one line through `systemMessage`. Plain stdout from this hook would be added
    to Claude's context on every prompt, costing tokens and steering the model;
    systemMessage is shown to the person only. It never blocks a prompt: every
    error is swallowed (and the last one written to last-error.txt), and it
    always exits 0.

    It does not need a Stop hook to learn what a turn actually cost. Claude Code
    writes the transcript asynchronously, so at Stop the last messages may not be
    on disk yet. Instead, each prompt resolves the earlier, finished turns of its
    session against their predictions, matched by prompt_id, and
    `claude-runway accuracy` resolves the rest.

Status line
    Claude Code hands the status line the real 5-hour quota (rate_limits) and
    the context window size. The segment saves them to limits.json, where the
    hook and the CLI read them, and prints one short line.
"""
import hashlib
import json
import os
import sys
import time
import traceback

import config
import estimator
import runway
import transcripts

RESOLVE_AFTER_IDLE = 600  # seconds: a session's last turn counts as finished after this long without writes
# Built-in commands that run no model turn. Anything else, skills and /compact included, is predicted.
LOCAL_COMMANDS = {"clear", "model", "config", "help", "status", "cost", "usage", "login", "logout", "exit",
                  "quit", "resume", "plugin", "reload-plugins", "permissions", "hooks", "memory", "theme",
                  "vim", "doctor", "mcp", "agents", "statusline", "fast", "effort", "context", "export"}


def prompt_hash(text):
    return hashlib.sha256((text or "").strip().encode("utf-8")).hexdigest()[:16]


def load_limits():
    try:
        with open(config.path("limits.json")) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def context_limit(cfg, limits, session_id):
    if cfg.get("context_limit"):
        return int(cfg["context_limit"])
    size = ((limits.get("sessions") or {}).get(session_id or "") or {}).get("context_window_size")
    return int(size) if size else config.DEFAULT_CONTEXT_LIMIT


def assess(session, prompt, cwd, cfg, now=None, limits=None):
    """Prediction, context runway and quota runway for one prompt."""
    now = time.time() if now is None else now
    limits = load_limits() if limits is None else limits
    ctx_now = session.context if session else None
    pred = estimator.predict(prompt, ctx_now, cfg, cwd)
    limit = context_limit(cfg, limits, session.session_id if session else None)
    ctx = runway.context_runway(ctx_now, pred, limit, runway.recent_growth(session.turns) if session else None)
    hours = cfg["quota"]["window_hours"]
    calls = transcripts.scan_calls(config.projects_dir(), now - 2 * hours * runway.HOUR, now)
    burn = transcripts.burn_rate(calls, now, cfg["burn_window_minutes"])
    quota = runway.quota_runway(calls, now, pred["tokens"], burn, cfg, limits)
    return pred, ctx, quota, calls


def resolve(session, current_prompt_id=None, now=None):
    """Record actuals for this session's finished turns that have a prediction and no actual yet."""
    now = time.time() if now is None else now
    done = {a.get("prompt_key") for a in config.read_jsonl("actuals.jsonl")}
    pending = [p for p in config.read_jsonl("predictions.jsonl")
               if p.get("session_id") == session.session_id and p.get("prompt_key") not in done]
    if not pending:
        return 0
    try:
        idle = now - os.path.getmtime(session.path) > RESOLVE_AFTER_IDLE
    except OSError:
        idle = False
    by_id = {t.prompt_id: i for i, t in enumerate(session.turns) if t.prompt_id}
    by_hash = {prompt_hash(t.text): i for i, t in enumerate(session.turns)}
    written = 0
    for p in pending:
        i = by_id.get(p.get("prompt_id")) if p.get("prompt_id") else by_hash.get(p.get("prompt_sha"))
        if i is None:
            continue
        turn = session.turns[i]
        finished = i < len(session.turns) - 1 or idle or (current_prompt_id and turn.prompt_id != current_prompt_id)
        if not finished or not turn.calls:
            continue
        actual = turn.total
        config.append_jsonl("actuals.jsonl", {
            "prompt_key": p["prompt_key"], "session_id": session.session_id, "tier": p.get("tier"),
            "predicted": p.get("tokens"), "actual": actual, "calls": len(turn.calls) + len(turn.sub_calls),
            "predicted_calls": p.get("calls"),
            "error_pct": round(100.0 * (p.get("tokens", 0) - actual) / actual, 1) if actual else None,
            "resolved_at": now,
        })
        written += 1
    return written


def user_prompt_submit(payload, now=None):
    """Returns the hook's stdout (a JSON object as text), or '' when there is nothing to show."""
    now = time.time() if now is None else now
    cfg = config.load()
    prompt = payload.get("prompt") or ""
    cwd = payload.get("cwd")
    path = payload.get("transcript_path") or ""
    session = transcripts.parse_session(path) if path and os.path.isfile(path) else None
    prompt_id = payload.get("prompt_id")
    if session is not None:
        resolve(session, prompt_id, now)
    words = prompt.strip().split()
    if len(words) == 1 and words[0].lstrip("/") in LOCAL_COMMANDS and words[0].startswith("/"):
        return ""  # runs no model turn: nothing to predict
    pred, ctx, quota, _ = assess(session, prompt, cwd, cfg, now)
    sha = prompt_hash(prompt)
    cal = cfg.get("calibrated") or {}
    v = runway.verdict(pred, quota, cal.get("ratio_range"))

    # The gate. A prompt it pauses never reaches Claude; sending the same text
    # again within confirm_seconds runs it.
    gate = cfg.get("gate", "always")
    wait = int(cfg.get("confirm_seconds") or 120)
    key = f"{payload.get('session_id') or (session.session_id if session else '')}:{sha}"
    pending = {k: t for k, t in load_pending().items() if isinstance(t, (int, float)) and now - t < wait}
    confirmed = pending.pop(key, None) is not None
    pause = not confirmed and (gate == "always" or (gate == "risky" and v["level"] in (runway.MAY_NOT_FIT,
                                                                                         runway.WONT_FIT)))
    if pause:
        pending[key] = now
    save_pending(pending)
    if pause:
        return json.dumps({"decision": "block",
                           "reason": runway.preflight_message(pred, ctx, quota, v, cal.get("turns", 0), wait)})
    config.append_jsonl("predictions.jsonl", {
        "ts": now, "session_id": payload.get("session_id") or (session.session_id if session else None),
        "prompt_id": prompt_id, "prompt_sha": sha, "prompt_key": prompt_id or sha,
        "prompt_chars": len(prompt), "tier": pred["tier"], "calls": pred["calls"], "tokens": pred["tokens"],
        "prompt_tokens": pred["prompt_tokens"], "context_before": pred["context_before"],
        "context_limit": ctx["limit"], "quota_pct": quota["pct"], "quota_source": quota["source"],
        "calibrated": bool(cfg.get("calibrated")), "verdict": v["level"], "confirmed": confirmed,
    })
    line = runway.summary_line(pred, ctx, quota, bool(cfg.get("calibrated")), v)
    return json.dumps({"systemMessage": ("[Runway] Running it, as you confirmed. " + line[9:]) if confirmed
                       else line})


def load_pending():
    try:
        with open(config.path("pending.json")) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_pending(pending):
    if pending or os.path.exists(config.path("pending.json")):
        config.write_atomic(config.path("pending.json"), pending)


def save_limits(payload, now=None):
    now = time.time() if now is None else now
    data = load_limits()
    rl = payload.get("rate_limits")
    if isinstance(rl, dict) and rl:
        data["rate_limits"] = rl
        data["captured_at"] = now
    sid = payload.get("session_id")
    size = (payload.get("context_window") or {}).get("context_window_size")
    if sid and size:
        sessions = data.get("sessions") or {}
        sessions[sid] = {"context_window_size": size, "at": now}
        data["sessions"] = dict(sorted(sessions.items(), key=lambda kv: kv[1].get("at", 0))[-50:])
    if data:
        config.write_atomic(config.path("limits.json"), data)
    return data


def statusline(payload, now=None):
    now = time.time() if now is None else now
    cfg = config.load()
    limits = save_limits(payload, now)
    parts = []
    cw = payload.get("context_window") or {}
    if cw.get("used_percentage") is not None:
        parts.append(f"ctx {float(cw['used_percentage']):.0f}%")
    hours = cfg["quota"]["window_hours"]
    calls = transcripts.scan_calls(config.projects_dir(), now - 2 * hours * runway.HOUR, now)
    burn = transcripts.burn_rate(calls, now, cfg["burn_window_minutes"])
    quota = runway.quota_runway(calls, now, 0, burn, cfg, limits)
    if quota["pct"] is not None:
        q = f"5h {quota['pct']:.0f}%"
        if quota["minutes_to_reset"] is not None:
            q += f" · resets {runway.human_minutes(quota['minutes_to_reset'])}"
        if quota["minutes_left"] is not None and quota.get("limited_by") == "quota":
            q += f" · ~{runway.human_minutes(quota['minutes_left'])} at this pace"
        parts.append(q)
    if not parts:
        return ""
    line = "⛽ " + " · ".join(parts)
    return line if "NO_COLOR" in os.environ else f"\033[36m{line}\033[0m"


def run(kind):
    """Entry point for hooks: never raises, never blocks, always exits 0."""
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        out = user_prompt_submit(payload) if kind == "user-prompt-submit" else statusline(payload)
        if out:
            print(out)
    except Exception:  # noqa: BLE001  a hook must not break the session it observes
        try:
            os.makedirs(config.home(), exist_ok=True)
            with open(config.path("last-error.txt"), "w") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + kind + "\n" + traceback.format_exc())
        except OSError:
            pass
    return 0
