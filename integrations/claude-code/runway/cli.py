"""claude-runway: how much room is left in this session's context and in the 5-hour window.

    claude-runway status            context, 5-hour window, burn rate, time left
    claude-runway check "<prompt>"  estimate a prompt and say whether it fits, without sending it
    claude-runway backtest          replay your transcripts and score the predictor
    claude-runway calibrate         write per-tier numbers measured from your history
    claude-runway accuracy          how the live predictions compared with what turns cost
    claude-runway init              write ~/.claude/runway/config.json with defaults and notes
    claude-runway install-hooks     register the hook (and, with --statusline, the status line)
    claude-runway uninstall-hooks   remove them again
"""
import argparse
import json
import os
import shutil
import sys
import time
from statistics import median

import config
import estimator
import hooks
import runway
import transcripts

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "claude-runway")
MARKER = "claude-runway"


# ------------------------------------------------------------------ history --

def history_rows(root, chars_per_token):
    """Every completed turn with at least one API call, oldest first, from every transcript.

    Row: dict(ts, session, prompt, cwd, before, first, calls, total, after). For
    a session's first turn there is no previous context, so `before` is derived
    from its first call: the context it read, less the prompt.
    """
    seen, rows, now = set(), [], time.time()
    for path in transcripts.main_transcripts(root):
        s = transcripts.parse_session(path, seen)
        live = now - os.path.getmtime(path) < hooks.RESOLVE_AFTER_IDLE
        for i, t in enumerate(s.turns):
            if not t.calls or (live and i == len(s.turns) - 1):
                continue  # no API call, or a turn that may still be running
            first = t.ctx_before is None
            before = t.ctx_before if not first else max(0, t.calls[0].context - len(t.text) / chars_per_token)
            rows.append(dict(ts=t.ts or 0, session=s.session_id, prompt=t.text, cwd=t.cwd or s.cwd,
                             before=before, first=first, calls=len(t.calls), total=t.total,
                             after=t.ctx_after))
    rows.sort(key=lambda r: r["ts"])
    return rows


def fit(rows, cfg):
    """Calibrated tiers and first-turn context from rows, or (None, None, counts) with too little data.

    Always starts from the shipped defaults (with your keywords), never from
    numbers an earlier calibrate measured: those already saw every turn, which
    would leak later turns into a walk-forward test and compound on re-runs.
    """
    tiers, counts = estimator.calibrate(
        [(r["prompt"], r["before"], r["calls"], r["total"], r["after"]) for r in rows],
        uncalibrated(cfg)["tiers"], cfg["chars_per_token"])
    firsts = [r["before"] for r in rows if r["first"]]
    return tiers, (int(median(firsts)) if firsts else None), counts


def predict_row(row, cfg):
    """What the predictor would have said before this turn ran."""
    return estimator.predict(row["prompt"], None if row["first"] else row["before"], cfg, row["cwd"])


def step_rows(rows):
    return [(r["calls"], r["total"], r["before"]) for r in rows]


def range_coverage(rows, chars_per_token):
    """Walk-forward: for each turn, the quick-to-heavy range from the turns before it. Returns (inside, scored)."""
    inside = scored = 0
    for i, r in enumerate(rows):
        prof = estimator.step_profile(step_rows(rows[:i]))
        if prof is None:
            continue
        s = estimator.scenarios(r["before"], len(r["prompt"]) / chars_per_token, prof)
        scored += 1
        inside += s["quick"]["tokens"] <= r["total"] <= s["heavy"]["tokens"]
    return inside, scored


def ape(pred, actual):
    return abs(pred - actual) / actual * 100.0 if actual else None


def score(errors):
    errors = [e for e in errors if e is not None]
    if not errors:
        return {"n": 0}
    return {"n": len(errors), "mape": sum(errors) / len(errors), "median_ape": median(errors),
            "within_50": 100.0 * sum(1 for e in errors if e <= 50) / len(errors)}


def fmt_score(s):
    if not s.get("n"):
        return "no turns"
    return (f"MAPE {s['mape']:6.1f}%   median APE {s['median_ape']:6.1f}%   "
            f"within ±50%: {s['within_50']:5.1f}%   (n={s['n']})")


# ----------------------------------------------------------------- commands --

def uncalibrated(cfg):
    """The shipped defaults, with the user's keywords."""
    return dict(cfg, calibrated=None, tiers={k: dict(v, keywords=cfg["tiers"][k]["keywords"])
                                             for k, v in config.DEFAULT_TIERS.items()})


def walk_forward(rows, cfg):
    """One prediction per row, each made with a calibration fitted only on the rows before it."""
    uncal, out = uncalibrated(cfg), []
    for i, row in enumerate(rows):
        tiers, first_ctx, _ = fit(rows[:i], cfg) if i >= 3 else (None, None, None)
        live = dict(cfg, tiers=tiers, calibrated={"first_context": first_ctx}) if tiers else uncal
        out.append(predict_row(row, live))
    return out


def cmd_backtest(args):
    cfg = config.load()
    rows = history_rows(config.projects_dir(), cfg["chars_per_token"])
    if not rows:
        print("No completed turns with API usage found under " + config.projects_dir())
        return 1
    sessions = len({r["session"] for r in rows})
    walk, default_err, naive_err, by_tier = [], [], [], {}
    uncal = uncalibrated(cfg)
    last_total = {}
    for i, (row, p) in enumerate(zip(rows, walk_forward(rows, cfg))):
        e = ape(p["tokens"], row["total"])
        walk.append(e)
        by_tier.setdefault(p["tier"], []).append((e, p["calls"], row["calls"]))
        default_err.append(ape(predict_row(row, uncal)["tokens"], row["total"]))
        prev = last_total.get(row["session"]) or (rows[i - 1]["total"] if i else None)
        if prev is not None:
            naive_err.append(ape(prev, row["total"]))
        last_total[row["session"]] = row["total"]

    inside, scored = range_coverage(rows, cfg["chars_per_token"])
    report = {
        "turns": len(rows), "sessions": sessions,
        "range": {"inside": inside, "scored": scored},
        "walk_forward": score(walk), "defaults": score(default_err), "naive_previous_turn": score(naive_err),
        "by_tier": {t: dict(score([x[0] for x in v]),
                            predicted_calls=median(x[1] for x in v), actual_calls=median(x[2] for x in v))
                    for t, v in sorted(by_tier.items())},
    }
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    span = time.strftime("%Y-%m-%d", time.localtime(rows[0]["ts"])), time.strftime("%Y-%m-%d", time.localtime(rows[-1]["ts"]))
    print(f"Backtest: {len(rows)} turns with API calls, {sessions} session(s), {span[0]} to {span[1]}")
    print("Each turn is predicted using only turns that finished before it (walk-forward).\n")
    print(f"  runway, walk-forward   {fmt_score(report['walk_forward'])}")
    print(f"  runway, defaults only  {fmt_score(report['defaults'])}")
    print(f"  naive: previous turn   {fmt_score(report['naive_previous_turn'])}")
    print(f"\n  quick-to-heavy range   {inside} of {scored} turns landed inside it"
          + (f" ({100 * inside / scored:.0f}%)" if scored else "")
          + "; this is the range the time-left estimate shows")
    print("\n  by tier (walk-forward)")
    for t, s in report["by_tier"].items():
        print(f"    {t:6} {fmt_score(s)}   calls: predicted {s['predicted_calls']:g}, actual {s['actual_calls']:g}")
    w, n = report["walk_forward"], report["naive_previous_turn"]
    print()
    if len(rows) < 30:
        print(f"  Small sample: {len(rows)} turns. Treat these numbers as a smoke test, not a measurement;\n"
              "  with under 30 turns no verdict is drawn against the baseline.")
    elif w.get("n") and n.get("n"):
        verdict = "beats" if w["median_ape"] < n["median_ape"] else "does not beat"
        print(f"  On median APE, runway {verdict} simply repeating the previous turn's cost.")
    print("  Run `claude-runway calibrate` to write the measured numbers into config.json.")
    return 0


def cmd_calibrate(args):
    say = (lambda *a: None) if args.quiet else print
    cfg = config.load()
    rows = history_rows(config.projects_dir(), cfg["chars_per_token"])
    tiers, first_ctx, counts = fit(rows, cfg)
    if not tiers:
        say("Not enough history to calibrate: no completed turns with API calls.")
        return 1
    profile = estimator.step_profile(step_rows(rows))
    say(f"Measured from {len(rows)} turns.")
    if profile:
        profile["coverage"] = list(range_coverage(rows, cfg["chars_per_token"]))
        inside, scored = profile["coverage"]
        say(f"  steps per prompt   quick {profile['quick']}, typical {profile['typical']}, heavy {profile['heavy']}"
            f" (10th percentile, median, 90th percentile)")
        say(f"  extra per step     {profile['extra_per_step']:,} tokens beyond re-reading the context")
        say(f"  track record       {inside} of {scored} prompts landed inside the quick-to-heavy range, each"
            " predicted only from the prompts before it")
    else:
        say(f"  steps per prompt   needs {estimator.MIN_STEP_HISTORY} prompts of history, have {len(rows)};"
            " starting defaults until then")
    say(f"  first-turn context {first_ctx:,}" if first_ctx is not None else "  first-turn context: not measured")
    if args.dry_run:
        say("\n--dry-run: config.json not changed.")
        return 0
    cfg["tiers"] = tiers
    cfg["calibrated"] = {"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "at_ts": time.time(), "turns": len(rows),
                         "turns_per_tier": counts, "first_context": first_ctx, "steps": profile}
    config.save(cfg)
    say(f"\nWrote {config.path('config.json')}")
    return 0


def cmd_accuracy(args):
    root = config.projects_dir()
    preds = config.read_jsonl("predictions.jsonl")
    for sid in sorted({p.get("session_id") for p in preds if p.get("session_id")}):
        path = transcripts.find_transcript(root, session_id=sid)
        if path:
            hooks.resolve(transcripts.parse_session(path))
    actuals = config.read_jsonl("actuals.jsonl")
    print(f"{len(preds)} prediction(s) logged, {len(actuals)} resolved against the transcript.")
    if not actuals:
        print("Nothing to score yet: actuals appear once a predicted turn has finished.")
        return 0
    ranged = [a for a in actuals if a.get("in_range") is not None]
    if ranged:
        hits = sum(1 for a in ranged if a["in_range"])
        print(f"  inside the quick-to-heavy range: {hits} of {len(ranged)} prompts")
    errs = [ape(a["predicted"], a["actual"]) for a in actuals if a.get("actual")]
    print("  typical-case error " + fmt_score(score(errs)))
    for tier in sorted({a.get("tier") for a in actuals}):
        print(f"  {str(tier):7} " + fmt_score(score([ape(a["predicted"], a["actual"]) for a in actuals
                                                   if a.get("tier") == tier and a.get("actual")])))
    print("\n  latest")
    for a in actuals[-8:]:
        print(f"    {a.get('tier', '?'):6} predicted {runway.human_tokens(a['predicted']):>7}  "
              f"actual {runway.human_tokens(a['actual']):>7}  error {a.get('error_pct', 0):+7.1f}%  "
              f"calls {a.get('predicted_calls')}->{a.get('calls')}")
    return 0


def cmd_status(args):
    cfg = config.load()
    now = time.time()
    root = config.projects_dir()
    path = transcripts.find_transcript(root, cwd=args.cwd or os.getcwd(), session_id=args.session)
    session = transcripts.parse_session(path) if path else None
    limits = hooks.load_limits()
    done = [t for t in (session.turns if session else []) if t.calls]
    typical = int(median(t.total for t in done[-10:])) if done else 0
    hours = cfg["quota"]["window_hours"]
    calls = transcripts.scan_calls(root, now - 2 * hours * runway.HOUR, now)
    burn = transcripts.burn_rate(calls, now, cfg["burn_window_minutes"])
    quota = runway.quota_runway(calls, now, typical, burn, cfg, limits)
    limit = hooks.context_limit(cfg, limits, session.session_id if session else None)
    pseudo = {"context_growth": 0, "context_after": (session.context or 0) if session else 0}
    ctx = runway.context_runway(session.context if session else None, pseudo, limit,
                                runway.recent_growth(session.turns) if session else None)
    if args.json:
        print(json.dumps({"session": session.session_id if session else None, "context": ctx,
                          "quota": quota, "typical_turn_tokens": typical}, indent=2))
        return 0
    print(f"Session    {session.session_id if session else 'none found'}"
          + (f"  ({os.path.basename(os.path.dirname(path))})" if path else ""))
    if session and session.context is not None:
        tl = ctx["turns_left"]
        print(f"Context    {session.context:,} / {limit:,} tokens ({ctx['pct']:.1f}%)"
              + (f", ~{tl} turns to full at ~{runway.human_tokens(ctx['growth_per_turn'])}/turn"
                 if tl is not None and runway.recent_growth(session.turns) else ""))
    else:
        print("Context    no API calls in this session yet")
    if done:
        print(f"Turns      {len(done)} with API calls; median of the last {min(10, len(done))}: "
              f"{runway.human_tokens(typical)} tokens, "
              f"{median(len(t.calls) for t in done[-10:]):g} calls")
    rate, rate_minutes = burn
    print(f"Burn       {runway.human_tokens(rate)} tokens/min"
          + (f" over the last {runway.human_minutes(rate_minutes)} of work"
             f" (looking back {cfg['burn_window_minutes']} min)" if rate else " (idle)"))
    src = {"claude-code": "Claude Code's rate limits", "token_cap": "quota.token_cap in config.json",
           "unknown": "unknown"}[quota["source"]]
    if quota["pct"] is not None:
        line = f"5h window  {quota['pct']:.1f}% used ({src}), {runway.human_tokens(quota['tokens'])} tokens locally"
        if quota["minutes_to_reset"] is not None:
            line += f", resets in {runway.human_minutes(quota['minutes_to_reset'])}"
        print(line)
        if quota["minutes_left"] is not None:
            how = ("the window resets first" if quota.get("limited_by") == "reset"
                   else f"at your pace over the last {runway.human_minutes(quota.get('pace_minutes'))}")
            print(f"Time left  ~{runway.human_minutes(quota['minutes_left'])} ({how})"
                  + (f"; ~{quota['turns_left']} typical turns" if quota["turns_left"] is not None else ""))
        else:
            print("Time left  not burning right now"
                  + (f"; ~{quota['turns_left']} typical turns" if quota["turns_left"] is not None else ""))
    else:
        print(f"5h window  {runway.human_tokens(quota['tokens'])} tokens locally"
              + (f", resets in {runway.human_minutes(quota['minutes_to_reset'])}"
                 if quota["minutes_to_reset"] is not None else ", no window open"))
        print("Time left  unknown: install the status line (install-hooks --statusline) so Claude Code reports the\n"
              "           quota, or set quota.token_cap in " + config.path("config.json"))
    if not cfg.get("calibrated"):
        print("\nPredictions use uncalibrated defaults. Run `claude-runway calibrate`.")
    return 0


def cmd_check(args):
    """Estimate a prompt without sending it anywhere."""
    cfg = config.load()
    root = config.projects_dir()
    cwd = args.cwd or os.getcwd()
    path = transcripts.find_transcript(root, cwd=cwd, session_id=args.session)
    session = transcripts.parse_session(path) if path else None
    prompt = " ".join(args.prompt) if args.prompt else sys.stdin.read()
    pred, ctx, quota, _ = hooks.assess(session, prompt, cwd, cfg)
    cal = cfg.get("calibrated") or {}
    base = pred["context_before"] if pred["context_before"] is not None else (cal.get("first_context") or 0)
    scen = estimator.scenarios(base, pred["prompt_tokens"], cal.get("steps"))
    color = sys.stdout.isatty() and "NO_COLOR" not in os.environ and bool(cfg.get("color", True))
    print(runway.preflight_message(scen, ctx, quota, runway.verdict(scen, quota), cal.get("steps"), color=color))
    if session:
        print(f"   Session     {session.session_id} (the latest in {os.path.basename(os.path.dirname(path))})")
    return 0


def cmd_init(args):
    target, created = config.init()
    print(("Wrote " if created else "Already exists, left as is: ") + target)
    return 0


# ------------------------------------------------------------ settings.json --

def _ours(hook):
    return isinstance(hook, dict) and MARKER in str(hook.get("command", ""))


def _load_settings(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        text = f.read()
    if not text.strip():
        return {}
    data = json.loads(text)  # ValueError on invalid JSON: the caller refuses to write
    if not isinstance(data, dict):
        raise ValueError("settings is not a JSON object")
    return data


def _backup(path):
    if os.path.exists(path):
        dest = f"{path}.runway-backup-{time.strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(path, dest)
        return dest
    return None


def hook_command(kind):
    # `|| true`: if the clone moves, python exits 2, and a UserPromptSubmit hook
    # that exits 2 blocks every prompt.
    return f'python3 "{SCRIPT}" hook {kind} || true'


# install-hooks --statusline keeps a status line it did not write. Claude Code reports the quota to the
# status line and nowhere else (hooks.save_limits runs in that segment alone), so a user who stops at
# this message never gets a real 5-hour window. Say what is lost and give the recipe in full: whoever
# installed with npx has no clone to open the README in.
STATUSLINE_KEPT = "left your existing status line alone"


def statusline_recipe(settings_path):
    return f"""
Your status line is your own, so runway left it alone — but Claude Code reports the 5-hour quota to
the status line and nowhere else, so until runway's segment runs, `status` cannot show time left and
`check` has no real window to judge against.

Print both. Claude Code shows every line your command emits:

    #!/usr/bin/env bash
    input=$(cat)
    printf '%s' "$input" | <your current status line command>
    printf '%s' "$input" | python3 "{SCRIPT}" statusline

Save that as, say, ~/.claude/statusline-combined.sh, chmod +x it, and point statusLine.command in
{settings_path} at it."""


def install(settings_path, statusline=False):
    """Returns a list of what changed. Raises ValueError on unreadable settings, writing nothing."""
    data = _load_settings(settings_path)
    changes = []
    hooks_cfg = data.setdefault("hooks", {})
    if not isinstance(hooks_cfg, dict):
        raise ValueError('"hooks" in settings is not an object')
    groups = hooks_cfg.setdefault("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError('"hooks.UserPromptSubmit" in settings is not a list')
    if not any(_ours(h) for g in groups if isinstance(g, dict) for h in g.get("hooks") or []):
        groups.append({"hooks": [{"type": "command", "command": hook_command("user-prompt-submit"),
                                  "timeout": 10}]})
        changes.append("added the UserPromptSubmit hook")
    if statusline:
        current = data.get("statusLine")
        if not current:
            data["statusLine"] = {"type": "command", "command": f'python3 "{SCRIPT}" statusline'}
            changes.append("set the status line")
        elif not _ours(current):
            changes.append(STATUSLINE_KEPT)
    if any(c.startswith(("added", "set")) for c in changes):
        backup = _backup(settings_path)
        if backup:
            changes.append(f"backed up the previous settings to {backup}")
        config.write_atomic(settings_path, data)
    return changes


def uninstall(settings_path):
    data = _load_settings(settings_path)
    changes = []
    hooks_cfg = data.get("hooks")
    if isinstance(hooks_cfg, dict):
        for event in list(hooks_cfg):
            groups = hooks_cfg[event]
            if not isinstance(groups, list):
                continue
            kept = []
            for g in groups:
                if isinstance(g, dict) and isinstance(g.get("hooks"), list):
                    inner = [h for h in g["hooks"] if not _ours(h)]
                    if len(inner) != len(g["hooks"]):
                        changes.append(f"removed the {event} hook")
                    if inner:
                        kept.append(dict(g, hooks=inner))
                else:
                    kept.append(g)
            if kept:
                hooks_cfg[event] = kept
            else:
                del hooks_cfg[event]
        if not hooks_cfg:
            del data["hooks"]
    if _ours(data.get("statusLine")):
        del data["statusLine"]
        changes.append("removed the status line")
    if changes:
        backup = _backup(settings_path)
        if backup:
            changes.append(f"backed up the previous settings to {backup}")
        config.write_atomic(settings_path, data)
    return changes


def cmd_install(args):
    path = args.settings or os.path.join(config.claude_dir(), "settings.json")
    try:
        changes = install(path, args.statusline)
    except ValueError as e:
        print(f"Not changed: {path} could not be read as JSON settings ({e}). Fix it and run again.")
        return 1
    target, created = config.init()
    print(path + ": " + ("; ".join(changes) if changes else "already installed, nothing changed"))
    if created:
        print("Wrote " + target)
    if STATUSLINE_KEPT in changes:
        print(statusline_recipe(path))
    if not args.statusline:
        print("For the real 5-hour quota, also install the status line: install-hooks --statusline")
    return 0


def cmd_uninstall(args):
    path = args.settings or os.path.join(config.claude_dir(), "settings.json")
    try:
        changes = uninstall(path)
    except ValueError as e:
        print(f"Not changed: {path} could not be read as JSON settings ({e}).")
        return 1
    print(path + ": " + ("; ".join(changes) if changes else "nothing of runway's was installed"))
    print(f"Your data in {config.home()} is kept. Delete that folder to remove it.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="claude-runway", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("status", help="context, 5-hour window, burn rate and time left")
    p.add_argument("--session", help="session id (default: latest in this directory's project)")
    p.add_argument("--cwd", help="project directory (default: the current one)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("check", help="estimate a prompt and say whether it fits, without sending it")
    p.add_argument("prompt", nargs="*", help="the prompt (or pipe it on stdin)")
    p.add_argument("--session", help="session id (default: latest in this directory's project)")
    p.add_argument("--cwd", help="project directory, for @file mentions (default: the current one)")
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("backtest", help="replay your transcripts and score the predictor")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_backtest)
    p = sub.add_parser("calibrate", help="write per-tier numbers measured from your history to config.json")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--quiet", action="store_true", help="print nothing (the hook runs it in the background)")
    p.set_defaults(func=cmd_calibrate)
    sub.add_parser("accuracy", help="score the live predictions the hook logged").set_defaults(func=cmd_accuracy)
    sub.add_parser("init", help="write config.json with defaults and notes").set_defaults(func=cmd_init)
    for name, func, text in (("install-hooks", cmd_install, "register the hook in settings.json"),
                             ("uninstall-hooks", cmd_uninstall, "remove runway from settings.json")):
        p = sub.add_parser(name, help=text)
        p.add_argument("--settings", help="settings file (default: ~/.claude/settings.json)")
        if name == "install-hooks":
            p.add_argument("--statusline", action="store_true",
                           help="also set the status line, if you do not have one")
        p.set_defaults(func=func)
    p = sub.add_parser("hook", help="run as a Claude Code hook (reads the hook JSON on stdin)")
    p.add_argument("kind", choices=["user-prompt-submit"])
    p.set_defaults(func=lambda a: hooks.run(a.kind))
    sub.add_parser("statusline", help="run as a status line segment").set_defaults(
        func=lambda a: hooks.run("statusline"))
    args = ap.parse_args(argv)
    return args.func(args)
