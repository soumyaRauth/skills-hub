"""How much room is left: in the context window, and in the 5-hour usage window.

The 5-hour window is read, in order of trust, from:

1. claude-code  Claude Code's own rate_limits.five_hour (percent used, reset
                time), saved by the runway status line. It counts everything
                the plan counts, including other devices and claude.ai. Usage
                after the snapshot is added at the rate the snapshot implies.
2. token_cap    quota.token_cap from config.json, against tokens counted in
                local transcripts, in a window that starts at the first call
                after five idle hours.
3. unknown      neither: usage and burn rate are shown, time left is not.

Converting a percentage into turns uses percent-per-token from the snapshot,
which is high when other devices also used the window. That errs toward
reporting less runway, not more.
"""
from statistics import median

from estimator import MIN_STEP_HISTORY as MIN_PROFILE_TURNS

HOUR = 3600.0


def window_start(calls, now, hours):
    """Start of the 5-hour window that is open now, or None when none is open.

    A window opens with the first call after the previous one closed.
    """
    start = None
    for c in calls:
        if start is None or c.ts >= start + hours * HOUR:
            start = c.ts
    if start is None or now >= start + hours * HOUR:
        return None
    return start


def context_runway(session_ctx, predicted, limit, recent_growth):
    used = session_ctx or 0
    growth = recent_growth if recent_growth and recent_growth > 0 else predicted["context_growth"]
    left = limit - used
    return {
        "used": used,
        "limit": limit,
        "pct": 100.0 * used / limit if limit else None,
        "after_pct": 100.0 * predicted["context_after"] / limit if limit else None,
        "growth_per_turn": growth,
        "turns_left": int(left // growth) if growth > 0 and left > 0 else 0 if left <= 0 else None,
    }


def recent_growth(turns, n=10):
    """Median context growth per turn over the session's last n completed turns, or None."""
    deltas = [t.ctx_after - t.ctx_before for t in turns[-n:]
              if t.calls and t.ctx_before is not None and t.ctx_after is not None]
    deltas = [d for d in deltas if d > 0]  # a /compact shrinks the context; it is not a turn's growth
    return median(deltas) if len(deltas) >= 2 else None


def quota_runway(calls, now, predicted_tokens, burn, cfg, snapshot):
    """Percent used, reset time, minutes and turns left. `calls` covers at least the last 2 x window hours."""
    hours = cfg["quota"]["window_hours"]
    five = ((snapshot or {}).get("rate_limits") or {}).get("five_hour") or {}
    resets_at = five.get("resets_at")
    out = {"source": "unknown", "pct": None, "resets_at": None, "minutes_to_reset": None,
           "tokens": 0, "burn_per_min": burn, "minutes_left": None, "turns_left": None, "next_turn_pct": None}

    pct_per_token = None
    if isinstance(resets_at, (int, float)) and resets_at > now and five.get("used_percentage") is not None:
        start = resets_at - hours * HOUR
        at = snapshot.get("captured_at") or now
        before = sum(c.total for c in calls if start <= c.ts <= at)
        since = sum(c.total for c in calls if c.ts > at)
        snap_pct = float(five["used_percentage"])
        pct_per_token = snap_pct / before if before > 0 and snap_pct > 0 else None
        out.update(source="claude-code", resets_at=resets_at, tokens=before + since,
                   pct=min(100.0, snap_pct + (pct_per_token or 0) * since))
    else:
        start = window_start(calls, now, hours)
        tokens = sum(c.total for c in calls if start is not None and c.ts >= start)
        out.update(tokens=tokens, resets_at=start + hours * HOUR if start is not None else None)
        cap = cfg["quota"].get("token_cap")
        if cap:
            pct_per_token = 100.0 / cap
            out.update(source="token_cap", pct=min(100.0, tokens * pct_per_token))

    if out["resets_at"] is not None:
        out["minutes_to_reset"] = max(0.0, (out["resets_at"] - now) / 60.0)

    # Your pace: tokens per minute over the last burn window. After a break
    # that is zero, which would say nothing about how long you can work, so
    # fall back to your average since this 5-hour window opened.
    pace, out["pace_source"] = burn, "recent"
    if pace <= 0 and start is not None and out["tokens"] > 0:
        pace, out["pace_source"] = out["tokens"] / max(5.0, (now - start) / 60.0), "window"
    out["pace"] = pace

    if pct_per_token and out["pct"] is not None:
        room = max(0.0, 100.0 - out["pct"])
        out["pct_per_token"] = pct_per_token
        out["room_tokens"] = room / pct_per_token
        out["next_turn_pct"] = pct_per_token * predicted_tokens
        if out["next_turn_pct"] > 0:
            out["turns_left"] = int(room // out["next_turn_pct"])
        if pace > 0:
            a = after(out, 0)
            # The status line and `status` read "reset" (you would not run out first) or "quota".
            out["minutes_left"] = a["minutes"]
            out["limited_by"] = "reset" if a["status"] == "reset" else "quota"
    return out


def after(quota, tokens):
    """Where you stand once a prompt of `tokens` has run.

    status: "limit" (the 5-hour limit is hit during it), "reset" (you would not
    run out before the window resets), "time" (minutes of work left at your
    pace), "nopace" (nothing used yet in this window to measure a pace from),
    or "unknown" (no quota reading).
    """
    ppt = quota.get("pct_per_token")
    if not ppt or quota.get("pct") is None:
        return {"status": "unknown", "minutes": None, "pct_after": None}
    room = max(0.0, 100.0 - quota["pct"])
    cost = ppt * tokens
    pct_after = min(100.0, quota["pct"] + cost)
    reset = quota.get("minutes_to_reset")
    if cost > room:
        return {"status": "limit", "minutes": 0.0, "pct_after": 100.0}
    pace = quota.get("pace") or 0
    if pace <= 0:
        return {"status": "nopace", "minutes": None, "pct_after": pct_after}
    mins = (room - cost) / (ppt * pace)
    if reset is not None and reset <= mins:
        return {"status": "reset", "minutes": reset, "pct_after": pct_after}
    return {"status": "time", "minutes": mins, "pct_after": pct_after}


FITS, MAY_NOT_FIT, WONT_FIT, UNKNOWN = "fits", "may not fit", "won't fit", "unknown"


def verdict(scen, quota):
    """Will this prompt finish before the 5-hour quota runs out, across its quick-to-heavy range?

    Only the quota can cut a turn off. A full context does not: Claude Code
    compacts it and carries on, so context is reported, never a reason to stop.
    """
    room = quota.get("room_tokens")
    lo, hi = scen["quick"]["tokens"], scen["heavy"]["tokens"]
    if room is None:
        level = UNKNOWN
    elif hi <= room:
        level = FITS
    elif lo > room:
        level = WONT_FIT
    else:
        level = MAY_NOT_FIT
    return {"level": level, "low": lo, "high": hi, "room_tokens": room}


BOLD, GREEN, YELLOW, RED, DIM, RESET = "\033[1m", "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[0m"
TONE = {"fits": GREEN, "may not fit": YELLOW, "won't fit": RED, "unknown": YELLOW}


def paint(text, *codes, color=True):
    """Wrap text in ANSI codes when color is on. Claude Code shows them, or strips them cleanly."""
    return "".join(codes) + text + RESET if color and codes else text


def _short(a):
    """The time left after a prompt, in a few words."""
    if a["status"] == "limit":
        return "none, the 5h limit is hit partway"
    if a["status"] == "reset":
        return f"~{human_minutes(a['minutes'])}, it lasts until the reset"
    if a["status"] == "nopace":
        return f"{a['pct_after']:.0f}% used after it"
    return f"~{human_minutes(a['minutes'])}"


def _cell(a):
    """The same, for a table cell."""
    if a["status"] == "reset":
        return f"~{human_minutes(a['minutes'])} (until the reset)"
    return "limit hit partway" if a["status"] == "limit" else _short(a)


def time_left_headline(scen, quota, level, color=False):
    """The highlighted answer: time left once the prompt has run, if it is typical."""
    typ = _short(after(quota, scen["typical"]["tokens"]))
    return paint(f"⏳ TIME LEFT after this prompt: {typ}", BOLD, TONE.get(level, ""), color=color)


VERDICT = {WONT_FIT: "⛔ Unlikely to finish before your 5-hour limit, even if it turns out quick.",
           MAY_NOT_FIT: "⚠️  May not finish before your 5-hour limit if it turns out heavy.",
           FITS: "✅ Should fit, even if it turns out heavy.",
           UNKNOWN: "❔ No 5-hour quota reading yet, so no time estimate."}


def preflight_message(scen, ctx, quota, v, profile, confirm_seconds=None, color=False):
    """The estimate shown before a prompt runs; with confirm_seconds, the message that holds it back."""
    lines = ["⛽ Runway · " + ("waiting for you to confirm this prompt" if confirm_seconds
                               else "estimate for this prompt (nothing was sent)"), ""]
    reset = quota.get("minutes_to_reset")
    if quota.get("pct") is None:
        lines += [VERDICT[UNKNOWN],
                  "   Install the runway status line (install-hooks --statusline), or set quota.token_cap.", ""]
    else:
        lines.append(time_left_headline(scen, quota, v["level"], color))
        pace = "at your pace over the last hour" if quota.get("pace_source") == "recent" else \
            "at your average pace this window"
        now = quota.get("minutes_left")
        lines.append(paint(f"   if it turns out typical, {pace}"
                           + (f" · ~{human_minutes(now)} left right now" if now is not None else ""),
                           DIM, color=color))
        lines += ["", paint(VERDICT[v["level"]], BOLD, color=color), ""]
        lines.append(paint(f"   {'If it turns out':<17}{'Steps':>5}{'Tokens':>9}   Time left after", DIM, color=color))
        for name in ("quick", "typical", "heavy"):
            sc = scen[name]
            row = (f" {'▸' if name == 'typical' else ' '} {name:<17}{sc['steps']:>5}"
                   f"{human_tokens(sc['tokens']):>9}   {_cell(after(quota, sc['tokens']))}")
            lines.append(paint(row, BOLD, color=color) if name == "typical" else row)
        q = f"{quota['pct']:.0f}% used" + (f" · resets in {human_minutes(reset)}" if reset is not None else "")
        lines += ["", f"   5h window   {q}"]
    if ctx.get("pct") is not None:
        lines.append(f"   Context     {ctx['pct']:.0f}% used"
                     + (" · Claude Code compacts it when full, and carries on" if ctx["pct"] >= 80 else ""))
    if profile:
        cov = profile.get("coverage")
        lines.append(f"   Based on    your last {profile['turns']} prompts"
                     + (f" · {cov[0]} of {cov[1]} landed in this range" if cov and cov[1] else ""))
    else:
        lines.append(f"   Based on    starting defaults, until you have {MIN_PROFILE_TURNS} prompts of history")
    if confirm_seconds:
        mins = confirm_seconds // 60 or 1
        go = "Run it anyway" if v["level"] in (WONT_FIT, MAY_NOT_FIT) else "To run it"
        lines += ["", paint(f"👉 {go}: press ↑ then Enter within {mins} min.", BOLD, color=color)
                  + " To drop it, do nothing; it was not sent."]
    return "\n".join(lines)


def human_tokens(n):
    if n is None:
        return "?"
    n = float(n)
    for unit, size in (("M", 1e6), ("k", 1e3)):
        if abs(n) >= size:
            return f"{n / size:.1f}{unit}"
    return str(int(n))


def human_minutes(m):
    if m is None:
        return "?"
    m = int(round(m))
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


def summary_line(scen, ctx, quota, confirmed=False, color=False):
    """The one line shown once a prompt runs."""
    parts = ["⛽ Runway" + (" · running it, as you confirmed" if confirmed else "")]
    if quota["pct"] is not None:
        v = verdict(scen, quota)
        ends = {n: _cell(after(quota, scen[n]["tokens"])) for n in ("quick", "heavy")}
        parts.append(time_left_headline(scen, quota, v["level"], color)
                     + f" (quick: {ends['quick']} · heavy: {ends['heavy']})")
        parts.append(f"5h used {quota['pct']:.0f}%"
                     + (f", resets in {human_minutes(quota['minutes_to_reset'])}"
                        if quota.get("minutes_to_reset") is not None else ""))
    else:
        parts.append(f"5h window {human_tokens(quota['tokens'])} tokens, quota unknown")
    if ctx.get("pct") is not None:
        parts.append(f"context {ctx['pct']:.0f}%")
    return " · ".join(parts)
