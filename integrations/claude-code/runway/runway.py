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
        after = sum(c.total for c in calls if c.ts > at)
        snap_pct = float(five["used_percentage"])
        pct_per_token = snap_pct / before if before > 0 and snap_pct > 0 else None
        out.update(source="claude-code", resets_at=resets_at, tokens=before + after,
                   pct=min(100.0, snap_pct + (pct_per_token or 0) * after))
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
        out["room_tokens"] = room / pct_per_token
        out["next_turn_pct"] = pct_per_token * predicted_tokens
        if out["next_turn_pct"] > 0:
            out["turns_left"] = int(room // out["next_turn_pct"])
        room_after = max(0.0, room - out["next_turn_pct"])
        out["runs_out_during"] = out["next_turn_pct"] > room
        reset = out["minutes_to_reset"]

        def minutes(r):
            mins = r / (pct_per_token * pace)
            return (min(mins, reset) if reset is not None else mins), (
                "reset" if reset is not None and reset <= mins else "quota")

        if pace > 0:
            out["minutes_left"], out["limited_by"] = minutes(room)
            # The main number: how long you can keep working once this prompt has run.
            out["minutes_left_after"], out["after_limited_by"] = minutes(room_after)
    return out


FITS, MAY_NOT_FIT, WONT_FIT, UNKNOWN = "fits", "may not fit", "won't fit", "unknown"


def verdict(pred, quota, ratio_range=None):
    """Will this turn finish before the 5-hour quota runs out?

    Only the quota can cut a turn off. A full context does not: Claude Code
    compacts it and carries on, so context is reported, never a reason to stop.

    ratio_range is (low, high): how far actual turns have landed from their
    predictions in your history (see `calibrate`). Without it the verdict rests
    on the single estimate and says so.
    """
    est = pred["tokens"]
    lo, hi = (est * ratio_range[0], est * ratio_range[1]) if ratio_range else (est, est)
    room = quota.get("room_tokens")
    if room is None:
        level = UNKNOWN
    elif hi <= room:
        level = FITS
    elif lo > room:
        level = WONT_FIT
    else:
        level = MAY_NOT_FIT
    return {"level": level, "low": lo, "high": hi, "room_tokens": room, "ranged": bool(ratio_range)}


def time_left_after(quota):
    """How long you can keep working once this prompt has run, in one phrase."""
    reset = quota.get("minutes_to_reset")
    if quota.get("pct") is None:
        return "unknown: no 5-hour quota reading (install the runway status line, or set quota.token_cap)"
    if quota.get("runs_out_during"):
        return ("none: you would hit the 5-hour limit during this prompt"
                + (f"; the window resets in {human_minutes(reset)}" if reset is not None else ""))
    after = quota.get("minutes_left_after")
    if after is None:
        turns = quota.get("turns_left")
        return ("after it, no pace to measure yet (nothing used in this window)"
                + (f"; room for ~{max(0, turns - 1)} more prompts like this one" if turns is not None else ""))
    pace = "your pace over the last hour" if quota.get("pace_source") == "recent" else "your average pace this window"
    if quota.get("after_limited_by") == "reset":
        return (f"after it, enough to keep working until the window resets in {human_minutes(reset)} "
                f"(at {pace} you would not run out)")
    now = quota.get("minutes_left")
    return (f"after it, ~{human_minutes(after)} of work at {pace}"
            + (f" (~{human_minutes(now)} now)" if now is not None else "")
            + (f"; the window resets in {human_minutes(reset)}" if reset is not None else ""))


def preflight_message(pred, ctx, quota, v, history_turns, confirm_seconds=None):
    """What the prompt is estimated to cost and the verdict; with confirm_seconds, the block message."""
    head = {WONT_FIT: "this prompt is unlikely to finish before your 5-hour limit",
            MAY_NOT_FIT: "this prompt may not finish before your 5-hour limit",
            FITS: "this prompt should fit", UNKNOWN: "5-hour quota unknown, so no verdict"}[v["level"]]
    est = f"~{human_tokens(pred['tokens'])} tokens ({pred['tier']}, ~{pred['calls']} call(s))"
    if v["ranged"]:
        est += f", likely {human_tokens(v['low'])}-{human_tokens(v['high'])}"
    paused = "Paused" if v["level"] in (WONT_FIT, MAY_NOT_FIT) else "Before it runs"
    lines = [f"[Runway] {paused + ': ' if confirm_seconds else ''}{head}.",
             f"  Time left  {time_left_after(quota)}",
             f"  Estimate   {est}"]
    if quota.get("pct") is not None:
        q = f"  5h window  {quota['pct']:.0f}% used now"
        if quota.get("next_turn_pct") is not None:
            q += f", ~{min(100.0, quota['pct'] + quota['next_turn_pct']):.0f}% after it"
        if quota.get("minutes_to_reset") is not None:
            q += f", resets in {human_minutes(quota['minutes_to_reset'])}"
        lines.append(q)
    if ctx.get("pct") is not None:
        lines.append(f"  Context    {ctx['pct']:.0f}% -> ~{min(ctx['after_pct'], 100):.0f}%"
                     + (" (Claude Code will compact it and carry on)" if ctx["after_pct"] >= 100 else ""))
    if not v["ranged"]:
        lines.append(f"  Rough: only {history_turns} past turn(s) to learn from, so no error range yet.")
    if confirm_seconds:
        mins = confirm_seconds // 60 or 1
        go = "Run it anyway" if v["level"] in (WONT_FIT, MAY_NOT_FIT) else "To run it"
        lines.append(f"{go}: press Up, then Enter, within {mins} min. Otherwise do nothing; it was not sent.")
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


def summary_line(pred, ctx, quota, calibrated, v=None):
    """The one line the hook shows the user."""
    parts = [f"next: {pred['tier']}, ~{human_tokens(pred['tokens'])} tokens over ~{pred['calls']} call(s)"
             + ("" if calibrated else " (uncalibrated)")
             + (f", {v['level']}" if v and v["level"] != UNKNOWN else "")]
    if ctx["pct"] is not None:
        tl = ctx["turns_left"]
        parts.append(f"context {ctx['pct']:.0f}% -> ~{min(ctx['after_pct'], 100):.0f}%"
                     + (f", ~{tl} turns to full" if tl is not None else ""))
    if quota["pct"] is not None:
        q = f"5h {quota['pct']:.0f}% used"
        if quota["next_turn_pct"] is not None:
            q += f" (+{quota['next_turn_pct']:.1f}%)"
        if quota.get("runs_out_during"):
            q += ", the limit would be hit during this prompt"
        elif quota.get("minutes_left_after") is not None:
            q += (f", enough after it to work until the reset in {human_minutes(quota['minutes_to_reset'])}"
                  if quota.get("after_limited_by") == "reset"
                  else f", ~{human_minutes(quota['minutes_left_after'])} of work left after it")
        elif quota["minutes_to_reset"] is not None:
            q += f", resets in {human_minutes(quota['minutes_to_reset'])}"
        parts.append(q)
    else:
        parts.append(f"5h window {human_tokens(quota['tokens'])} tokens, quota unknown")
    return "[Runway] " + " | ".join(parts)
