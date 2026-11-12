"""Self-check for claude-runway. Run: python3 integrations/claude-code/runway/test_runway.py

Builds synthetic transcripts in a temporary Claude directory; never reads or
writes the real ~/.claude.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stdout
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TMP = tempfile.mkdtemp(prefix="runway-test-")
os.environ["CLAUDE_CONFIG_DIR"] = os.path.join(TMP, "claude")
os.environ["CLAUDE_RUNWAY_HOME"] = os.path.join(TMP, "runway")
os.environ["NO_COLOR"] = "1"
os.environ["CLAUDE_RUNWAY_NO_REFRESH"] = "1"  # no background re-measurement during tests

import cli  # noqa: E402
import config  # noqa: E402
import estimator  # noqa: E402
import hooks  # noqa: E402
import runway  # noqa: E402
import transcripts  # noqa: E402

NOW = time.time()
PROJECTS = config.projects_dir()


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat().replace("+00:00", "Z")


def human(text, pid, t, **kw):
    return dict({"type": "user", "promptId": pid, "timestamp": iso(t), "cwd": "/work/app",
                 "origin": {"kind": "human"}, "message": {"role": "user", "content": text}}, **kw)


def call(mid, t, inp, cc, cr, out, blocks=1, side=False):
    """One API response written as `blocks` entries that repeat its usage, as Claude Code writes them."""
    usage = {"input_tokens": inp, "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr,
             "output_tokens": out}
    return [{"type": "assistant", "timestamp": iso(t), "isSidechain": side, "requestId": "req-" + mid,
             "message": {"id": mid, "model": "claude-test", "usage": usage,
                         "content": [{"type": "text", "text": "x"}]}} for _ in range(blocks)]


def tool_result(pid, t):
    return {"type": "user", "promptId": pid, "timestamp": iso(t), "toolUseResult": {},
            "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}


def write(path, entries):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
        f.write('{"type": "assistant", "partial')  # a half-written last line must be tolerated
    return path


def flat(*items):
    out = []
    for i in items:
        out.extend(i if isinstance(i, list) else [i])
    return out


# A session: two prompts. The first makes two calls, each written 3 times;
# the second makes one call and runs a subagent. Noise that must not start a
# turn: tool results, a skill body (isMeta), a task notification, a slash
# command's local output.
T0 = NOW - 3600
S1 = os.path.join(PROJECTS, "-work-app", "s1.jsonl")
write(S1, flat(
    human("explain the parser", "p1", T0),
    call("m1", T0 + 1, 10, 1000, 5000, 100, blocks=3),
    tool_result("p1", T0 + 2),
    dict(human("<skill body>", "p1", T0 + 2), isMeta=True),
    call("m2", T0 + 3, 5, 200, 6000, 300, blocks=2),
    human("<task-notification>done</task-notification>", None, T0 + 4, origin={"kind": "task-notification"}),
    human("<local-command-stdout>ok</local-command-stdout>", "px", T0 + 4, origin=None),
    human("refactor @lib/a.py and @lib/b.py across the codebase", "p2", T0 + 60),
    call("m3", T0 + 61, 5, 2000, 6200, 500),
    call("sc1", T0 + 62, 7, 100, 0, 50, side=True),
))
write(os.path.join(PROJECTS, "-work-app", "s1", "subagents", "agent-1.jsonl"),
      flat(call("sub1", T0 + 65, 3, 400, 0, 40, side=True)))

# A resumed session that copied m3 into its file: counted once across files.
S2 = os.path.join(PROJECTS, "-work-other", "s2.jsonl")
write(S2, flat(human("fix the typo in README", "q1", T0 + 120), call("m3", T0 + 61, 5, 2000, 6200, 500),
               call("m4", T0 + 121, 2, 300, 9000, 80)))

# Something far outside every window.
write(os.path.join(PROJECTS, "-work-old", "old.jsonl"),
      flat(human("old", "o1", NOW - 30 * 3600), call("old1", NOW - 30 * 3600, 1, 1, 1, 1)))
os.utime(os.path.join(PROJECTS, "-work-old", "old.jsonl"), (NOW - 30 * 3600, NOW - 30 * 3600))

# ------------------------------------------------------- RUN-001..004 parser --

s = transcripts.parse_session(S1)
assert [t.prompt_id for t in s.turns] == ["p1", "p2"], [t.prompt_id for t in s.turns]   # RUN-002
assert [c.id for c in s.calls] == ["m1", "m2", "m3"]                                     # RUN-001
t1, t2 = s.turns
assert t1.total == (10 + 1000 + 5000 + 100) + (5 + 200 + 6000 + 300)                     # RUN-001: once each
assert t1.ctx_before is None and t2.ctx_before == 5 + 200 + 6000
assert s.context == 5 + 2000 + 6200                                                      # RUN-003
assert {c.id for c in t2.sub_calls} == {"sc1", "sub1"}                                   # subagents join their turn
assert t2.total == (5 + 2000 + 6200 + 500) + (7 + 100 + 50) + (3 + 400 + 40)
assert t1.text == "explain the parser"

calls = transcripts.scan_calls(PROJECTS, NOW - 10 * 3600, NOW)                           # RUN-004
ids = [c.id for c in calls]
assert sorted(ids) == sorted(["m1", "m2", "m3", "sc1", "sub1", "m4"]), ids
assert ids.count("m3") == 1 and "old1" not in ids

assert transcripts.find_transcript(PROJECTS, cwd="/work/app") == S1
assert transcripts.find_transcript(PROJECTS, session_id="s2") == S2
assert transcripts.project_dir_for("/a b/c.d", "/r") == "/r/-a-b-c-d"

# ---------------------------------------------------------------- RUN-005 burn --

recent = [c for c in calls if c.ts >= NOW - 3600]
assert transcripts.burn_rate(calls, NOW, 60) == sum(c.total for c in recent) / ((NOW - recent[0].ts) / 60)
assert transcripts.burn_rate(calls, NOW + 7200, 60) == 0.0                               # idle

# ----------------------------------------------------------- RUN-006 estimator --

cfg = config.load()
proj = os.path.join(TMP, "proj")
os.makedirs(os.path.join(proj, "lib"))
with open(os.path.join(proj, "lib", "a.py"), "w") as f:
    f.write("x" * 700)
assert estimator.mentions('see @lib/a.py, @"my notes.md" and email a@b.com') == ["lib/a.py", "my notes.md"]
chars, found = estimator.mention_chars("look at @lib/a.py and @lib/missing.py and @lib", proj)
assert chars == 700 and found == ["lib/a.py"]                                            # missing / dir count 0
assert estimator.prompt_tokens("@lib/a.py", proj, 3.5)[0] == round((9 + 700) / 3.5)
tiers = cfg["tiers"]
assert estimator.classify("why does this fail?", tiers) == "qa"
assert estimator.classify("add a retry to the upload", tiers) == "edit"
assert estimator.classify("refactor the auth module", tiers) == "multi"
assert estimator.classify("what about @a.py and @b.py", tiers, files=2) == "multi"
assert estimator.classify("address the comment", tiers) == "qa"                          # whole words: not "add"
p = estimator.predict("add a retry", 10_000, cfg)
e = tiers["edit"]
assert p["tier"] == "edit" and p["tokens"] == e["calls"] * (10_000 + p["prompt_tokens"]) + e["extra_tokens"]
assert estimator.predict("add a retry", None, cfg)["context_before"] is None             # first turn: no crash

# -------------------------------------------------------------- RUN-009 quota --

flat_calls = [transcripts.Call(f"c{i}", NOW - 600 + i * 60, "m", {"input_tokens": 1000}) for i in range(10)]
nothing = runway.quota_runway(flat_calls, NOW, 1000, 100.0, cfg, {})
assert nothing["source"] == "unknown" and nothing["pct"] is None and nothing["tokens"] == 10_000
assert nothing["minutes_left"] is None

capped = dict(cfg, quota=dict(cfg["quota"], token_cap=100_000))
q = runway.quota_runway(flat_calls, NOW, 1000, 100.0, capped, {})
assert q["source"] == "token_cap" and abs(q["pct"] - 10.0) < 1e-9
# 90% room at 0.001%/token: 90 turns of 1,000; 900 minutes at 100/min, but the window resets after 290.
assert q["turns_left"] == 90 and abs(q["minutes_to_reset"] - 290) < 1e-6
assert abs(q["minutes_left"] - 290) < 1e-6 and q["limited_by"] == "reset"
q = runway.quota_runway(flat_calls, NOW, 1000, 1000.0, capped, {})
assert abs(q["minutes_left"] - 90) < 1e-6 and q["limited_by"] == "quota"                  # faster burn: quota first

snap = {"rate_limits": {"five_hour": {"used_percentage": 20.0, "resets_at": NOW + 3600}}, "captured_at": NOW - 330}
q = runway.quota_runway(flat_calls, NOW, 1000, 100.0, cfg, snap)
# 5 calls (5,000 tokens) before the snapshot made 20%: 0.004%/token; 5 more since add 20% -> 40%.
assert q["source"] == "claude-code" and abs(q["pct"] - 40.0) < 1e-9, q
assert abs(q["next_turn_pct"] - 4.0) < 1e-9 and q["turns_left"] == 15
assert abs(q["minutes_left"] - 60.0) < 1e-6 and q["limited_by"] == "reset"               # reset comes first

# Time left after a prompt: 10% used, 90% room; 1,000 tokens cost 1% (cap 100k).
q = runway.quota_runway(flat_calls, NOW, 1000, 1000.0, capped, {})
assert abs(q["minutes_left"] - 90) < 1e-6 and q["pace_source"] == "recent"
a = runway.after(q, 1000)
assert a["status"] == "time" and abs(a["minutes"] - 89) < 1e-6 and abs(a["pct_after"] - 11) < 1e-9
assert runway.after(runway.quota_runway(flat_calls, NOW, 1000, 100.0, capped, {}), 1000)["status"] == "reset"
assert runway.after(q, 95_000) == {"status": "limit", "minutes": 0.0, "pct_after": 100.0}  # 95% needed, 90% left
idle = runway.quota_runway(flat_calls, NOW, 1000, 0.0, capped, {})            # after a break: the window's average
# 10,000 tokens since the window opened 10 minutes ago: 1,000/min, the same answer as the fast pace above.
assert idle["pace_source"] == "window" and abs(runway.after(idle, 1000)["minutes"] - 89) < 1e-6
assert runway.after(nothing, 1000)["status"] == "unknown"
scen3 = {"quick": {"steps": 1, "tokens": 1000}, "typical": {"steps": 3, "tokens": 3000},
         "heavy": {"steps": 8, "tokens": 95_000}}
line = runway.summary_line(scen3, {"pct": 12.0}, q)
assert line.startswith("[Runway] after it: ~1h29m left if quick · ~1h27m left if typical · limit hit partway if heavy")

# The step profile and the three outcomes.
prof = estimator.step_profile([(1, 1100, 1000), (1, 1200, 1100), (3, 3600, 1000), (5, 6500, 1200),
                               (20, 30_000, 1300), (2, 2500, 1100)])
assert prof["quick"] == 1 and prof["typical"] == 2 and prof["heavy"] >= 5 and prof["turns"] == 6
assert estimator.step_profile([(1, 10, 5)] * 4) is None                       # too little history
sc = estimator.scenarios(10_000, 100, prof)
assert sc["quick"]["tokens"] == 10_100                                         # floor: one re-read, no extra
assert sc["heavy"]["tokens"] == prof["heavy"] * (10_100 + prof["extra_per_step"])
assert estimator.scenarios(10_000, 100, None)["typical"]["steps"] == estimator.DEFAULT_STEPS["typical"]

expired = {"rate_limits": {"five_hour": {"used_percentage": 99.0, "resets_at": NOW - 1}}, "captured_at": NOW - 9999}
assert runway.quota_runway(flat_calls, NOW, 1000, 100.0, cfg, expired)["source"] == "unknown"

# A window opens at the first call after five idle hours.
H = runway.HOUR
mk = lambda t: transcripts.Call(str(t), t, "m", {})  # noqa: E731
assert runway.window_start([mk(NOW - 9 * H), mk(NOW - 2 * H), mk(NOW - H)], NOW, 5) == NOW - 2 * H
assert runway.window_start([mk(NOW - 9 * H), mk(NOW - 6 * H)], NOW, 5) is None

ctx = runway.context_runway(50_000, {"context_growth": 10_000, "context_after": 60_000}, 200_000, None)
assert ctx["pct"] == 25.0 and ctx["turns_left"] == 15
assert runway.context_runway(250_000, {"context_growth": 1, "context_after": 1}, 200_000, None)["turns_left"] == 0
assert runway.human_tokens(14_200) == "14.2k" and runway.human_minutes(75) == "1h15m"

# -------------------------------------------------- RUN-007 hook, RUN-008 actuals --

SCRIPT = os.path.join(HERE, "claude-runway")


def run_hook(stdin):
    return subprocess.run([sys.executable, SCRIPT, "hook", "user-prompt-submit"], input=stdin,
                          capture_output=True, text=True, env=os.environ, timeout=60)


for bad in ("not json", "[]", "", json.dumps({"prompt": 5, "transcript_path": 7})):
    r = run_hook(bad)
    assert r.returncode == 0 and r.stdout == "", (bad, r)                                # never blocks

payload = {"session_id": "s1", "transcript_path": S1, "cwd": proj, "prompt": "secret plan: add @lib/a.py",
           "prompt_id": "p3", "hook_event_name": "UserPromptSubmit"}
r = run_hook(json.dumps(payload))
assert r.returncode == 0, r.stderr
out = json.loads(r.stdout)                                                               # JSON, not plain text
# The default gate is "always": the first send is held back with its estimate, before it runs.
assert out["decision"] == "block", out
assert out["reason"].startswith("[Runway] Before it runs: 5-hour quota unknown, so no time estimate")
assert "To run it: press Up, then Enter" in out["reason"] and "secret" not in out["reason"]
assert not config.read_jsonl("predictions.jsonl")                                        # nothing ran yet
r = run_hook(json.dumps(dict(payload, prompt_id="p3")))                                  # sent again: runs
out = json.loads(r.stdout)
assert list(out) == ["systemMessage"] and out["systemMessage"].startswith("[Runway] Running it, as you confirmed.")
assert "quota unknown" in out["systemMessage"]
preds = config.read_jsonl("predictions.jsonl")
assert preds[-1]["prompt_id"] == "p3" and "secret" not in json.dumps(preds)              # prompt text not stored

assert run_hook(json.dumps(dict(payload, prompt="/clear", prompt_id="p4"))).stdout == ""  # no model turn

# A prediction for p2 (finished: p3 is now being asked) resolves against the transcript.
config.append_jsonl("predictions.jsonl", {"session_id": "s1", "prompt_id": "p2", "prompt_key": "p2",
                                          "tier": "multi", "tokens": 9000, "calls": 2})
assert hooks.resolve(transcripts.parse_session(S1), current_prompt_id="p3") == 1
assert hooks.resolve(transcripts.parse_session(S1), current_prompt_id="p3") == 0         # once only
a = config.read_jsonl("actuals.jsonl")[-1]
assert a["prompt_key"] == "p2" and a["actual"] == t2.total and a["calls"] == 3
assert a["error_pct"] == round(100 * (9000 - t2.total) / t2.total, 1)
# p3 has no turn in the transcript yet: it stays pending rather than resolving to zero.
assert all(x["prompt_key"] != "p3" for x in config.read_jsonl("actuals.jsonl"))

# ---------------------------------------------------------- RUN-013 status line --

line = hooks.statusline({"session_id": "s1", "rate_limits": {"five_hour": {"used_percentage": 12,
                         "resets_at": NOW + 1800}}, "context_window": {"context_window_size": 1_000_000,
                         "used_percentage": 7}}, NOW)
assert line.startswith("⛽ ctx 7% · 5h 12%"), line
lim = hooks.load_limits()
assert lim["sessions"]["s1"]["context_window_size"] == 1_000_000
assert hooks.context_limit(cfg, lim, "s1") == 1_000_000 and hooks.context_limit(cfg, lim, "zz") == 200_000
assert hooks.statusline({"session_id": "s9"}, NOW).startswith("⛽ 5h 12%")              # keeps the last quota
assert hooks.load_limits()["rate_limits"]["five_hour"]["used_percentage"] == 12

# ------------------------------------------------- RUN-011 backtest, RUN-012 --

rows = cli.history_rows(PROJECTS, 3.5)
# s1 was written just now: its last turn may still be running, so it is left out.
assert [r["session"] for r in rows].count("s1") == 1
for f in (S1, S2):
    os.utime(f, (T0 + 200, T0 + 200))
rows = cli.history_rows(PROJECTS, 3.5)
assert [r["session"] for r in rows].count("s1") == 2

# A tier with fewer than 3 turns keeps its numbers; one with 3 or more is measured.
qa_rows = [("why?", 1000, 1, 1100, 1050)] * 3 + [("refactor it", 1000, 9, 99_000, 30_000)]
fitted, counts = estimator.calibrate(qa_rows, cfg["tiers"], 3.5)
assert counts == {"qa": 3, "edit": 0, "multi": 1}
assert fitted["qa"]["calls"] == 1 and fitted["multi"] == cfg["tiers"]["multi"]
first = cli.walk_forward(rows, cfg)
# Appending a later, wildly different turn must not change any earlier prediction.
extra = dict(rows[-1], ts=rows[-1]["ts"] + 999, total=10**9, calls=50)
assert cli.walk_forward(rows + [extra], cfg)[:len(rows)] == first
with redirect_stdout(io.StringIO()) as buf:
    assert cli.main(["backtest"]) == 0
assert "walk-forward" in buf.getvalue() and "Small sample" in buf.getvalue()

custom = config.load()
custom["tiers"]["qa"]["keywords"] = ["huh"]
config.save(custom)
with redirect_stdout(io.StringIO()):
    assert cli.main(["calibrate"]) == 0
cal = config.load()
assert cal["calibrated"]["turns"] == len(rows) and cal["tiers"]["qa"]["keywords"] == ["huh"]  # keywords kept
assert cal["calibrated"]["first_context"] is not None
with redirect_stdout(io.StringIO()) as buf:
    assert cli.main(["status", "--cwd", "/work/app"]) == 0
assert "Context    8,205 / 1,000,000" in buf.getvalue()  # s1's window size came from the status line
assert "s1" in buf.getvalue()

# --------------------------------------------- RUN-014 the gate, before a prompt runs --

sc = {"quick": {"tokens": 1000}, "heavy": {"tokens": 3000}}
assert runway.verdict(sc, {"room_tokens": 5000})["level"] == runway.FITS          # even heavy fits
assert runway.verdict(sc, {"room_tokens": 2000})["level"] == runway.MAY_NOT_FIT   # quick fits, heavy does not
assert runway.verdict(sc, {"room_tokens": 999})["level"] == runway.WONT_FIT       # not even quick
assert runway.verdict(sc, {})["level"] == runway.UNKNOWN

os.remove(config.path("limits.json"))  # the gate tests set the quota through token_cap


def gate(gate_mode, cap, prompt="add a retry", sid="s1", now=NOW):
    c = config.load()
    c["gate"], c["quota"]["token_cap"] = gate_mode, cap
    config.save(c)
    out = hooks.user_prompt_submit({"session_id": sid, "transcript_path": S1, "cwd": proj, "prompt": prompt,
                                    "prompt_id": f"g{time.time()}"}, now)
    return json.loads(out)


assert config.DEFAULTS["gate"] == "always"                       # the default: decide before every prompt
logged = lambda: len(config.read_jsonl("predictions.jsonl"))  # noqa: E731
n0 = logged()
# The fixture window holds 31,302 tokens. "add a retry" at 8,205 context, with the starting defaults:
# quick 8,208 · typical 40,832 · heavy 81,664 tokens.
ok = gate("risky", 120_000)                                      # 88.7k left: even heavy fits, runs at once
assert "decision" not in ok and ok["systemMessage"].startswith("[Runway] after it: ") and logged() == n0 + 1

blocked = gate("risky", 35_000)                                  # 3.7k left: not even the quick case fits
lines = blocked["reason"].split("\n")
assert blocked["decision"] == "block" and lines[0] == "[Runway] Paused: this prompt is unlikely to finish before your 5-hour limit."
assert lines[1].startswith("  Time left after it, at your pace over the last hour")
assert all("limit hit partway" in l for l in lines[2:5])
assert "starting defaults until you have 5 prompts" in blocked["reason"]
assert "Run it anyway: press Up, then Enter, within 2 min" in blocked["reason"] and logged() == n0 + 1  # not logged

assert gate("risky", 35_000, sid="other")["decision"] == "block"  # same text, other session: not a confirmation
again = gate("risky", 35_000, now=NOW + 30)                      # sent again in time: runs
assert again["systemMessage"].startswith("[Runway] Running it, as you confirmed. after it: limit hit partway")
p = config.read_jsonl("predictions.jsonl")[-1]
assert logged() == n0 + 2 and p["confirmed"] is True and (p["quick_tokens"], p["heavy_tokens"]) == (8208, 81664)
assert gate("risky", 35_000, now=NOW + 40)["decision"] == "block"  # the confirmation is used up
assert gate("risky", 35_000, now=NOW + 40 + 121)["decision"] == "block"  # too late: paused afresh

mnf = gate("risky", 60_000, prompt="add a cache")                 # 28.7k left: quick fits, heavy does not
mlines = mnf["reason"].split("\n")
assert mnf["decision"] == "block" and "may not finish" in mlines[0] and "if it turns out heavy" in mlines[0]
# Quick: (28,698 - 8,208) tokens at 521.9 tokens/min is about 39 minutes.
assert mlines[2].split()[:3] == ["quick", "~39m", "left"] and "limit hit partway" in mlines[4]

assert "decision" not in gate("off", 35_000, prompt="add a test")   # off: never pauses
fits_pause = gate("always", 10**9, prompt="add docs")           # always: pauses even when it fits
assert fits_pause["decision"] == "block"
assert fits_pause["reason"].startswith("[Runway] Before it runs: this prompt should fit, even if it turns out heavy")
assert "To run it: press Up, then Enter" in fits_pause["reason"] and "anyway" not in fits_pause["reason"]
assert fits_pause["reason"].split("\n")[1].startswith("  Time left after it")       # the first thing you read
assert gate("always", 10**9, prompt="add docs")["systemMessage"].startswith("[Runway] Running it")
assert "decision" not in gate("risky", None, prompt="add logs")   # quota unknown: no basis to pause

c = config.load()
c["quota"]["token_cap"] = 35_000
config.save(c)
with redirect_stdout(io.StringIO()) as buf:                     # check: the same estimate, nothing sent
    assert cli.main(["check", "--cwd", "/work/app", "add", "a", "retry"]) == 0
assert buf.getvalue().startswith("[Runway] this prompt is unlikely") and "Run it anyway" not in buf.getvalue()

# ---------------------------------------------------- RUN-010 install-hooks --

settings = os.path.join(TMP, "settings.json")
existing = {"model": "opus", "statusLine": {"type": "command", "command": "my-line.sh"},
            "hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "mine.sh"}]}],
                      "Stop": [{"hooks": [{"type": "command", "command": "stop.sh"}]}]}}
with open(settings, "w") as f:
    json.dump(existing, f)
changes = cli.install(settings, statusline=True)
data = json.load(open(settings))
assert data["model"] == "opus" and data["statusLine"]["command"] == "my-line.sh"         # theirs untouched
assert data["hooks"]["Stop"] == existing["hooks"]["Stop"]
ups = data["hooks"]["UserPromptSubmit"]
assert ups[0] == existing["hooks"]["UserPromptSubmit"][0] and len(ups) == 2
assert ups[1]["hooks"][0]["command"].endswith("hook user-prompt-submit || true")
assert any("backed up" in c for c in changes) and any("left your existing status line" in c for c in changes)
backups = [n for n in os.listdir(TMP) if n.startswith("settings.json.runway-backup-")]
assert json.load(open(os.path.join(TMP, backups[0]))) == existing
assert not any(c.startswith("added") for c in cli.install(settings, statusline=True))     # idempotent
assert len(json.load(open(settings))["hooks"]["UserPromptSubmit"]) == 2

cli.uninstall(settings)
assert json.load(open(settings)) == existing                                             # round trip

fresh = os.path.join(TMP, "fresh", "settings.json")
cli.install(fresh, statusline=True)
assert "claude-runway" in json.load(open(fresh))["statusLine"]["command"]
cli.uninstall(fresh)
assert json.load(open(fresh)) == {}

broken = os.path.join(TMP, "broken.json")
with open(broken, "w") as f:
    f.write('{"model": "opus",,}')
try:
    cli.install(broken)
    raise AssertionError("install wrote over invalid JSON")
except ValueError:
    pass
assert open(broken).read() == '{"model": "opus",,}'                                      # untouched

print("claude-runway: all checks passed")
