"""Check for stop-announced-skills.py. Run: python3 integrations/claude-code/test_stop_announced_skills.py"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "stop-announced-skills.py")
spec = importlib.util.spec_from_file_location("stop_announced", SCRIPT)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)
NAMES = hook.hub_names()


def prompt(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def say(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def skill(name):
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": name}}]}}


def check(*entries):
    return hook.check([json.dumps(e) for e in entries], NAMES)


# Names resolve from slug, title, a shortened title and the ProofBuild alias.
assert hook.resolve("Production Guard", NAMES) == "production-guard"
assert hook.resolve("Deployment Compatibility", NAMES) == "deployment-compatibility"
assert hook.resolve("ProofBuild", NAMES) == "proof-driven-dev"
assert hook.resolve("impact-map", NAMES) == "impact-map"
assert hook.resolve("Ponytail", NAMES) is None

# The incident: two announced, one loaded, a HANDOFF line in text only.
line = "⚡ Deployment Compatibility · Production Guard — readiness verdict against a real target"
assert check(prompt("is this production deployment ready?"), say(line), skill("deployment-compatibility"),
             say("HANDOFF → production-guard: a ship decision")) == ["production-guard"]

# Both loaded (one plugin-namespaced): nothing missing.
assert check(prompt("x"), say(line), skill("deployment-compatibility"), skill("skills-hub:production-guard")) == []

# An explicit drop line satisfies it.
assert check(prompt("x"), say(line), skill("deployment-compatibility"),
             say("Production Guard dropped: nothing ships from this branch")) == []

# A skill the user typed as /name counts as loaded; stage names after the dash are ignored.
typed = prompt("<command-message>skills-pipeline</command-message>\n<command-name>/skills-pipeline</command-name>")
assert check(typed, say("⚡ Skills Pipeline — Frame → Impact → Ship gate")) == []

# Engagement is per request: an earlier turn's announcement does not carry over.
assert check(prompt("a"), say("⚡ Impact Map — rename reaches SQL"), prompt("b"), say("done")) == []

# A finished background task or an agent's report is not a new prompt: skills
# loaded before it arrived still count for the turn's ⚡ line.
notice = {"type": "user", "origin": {"kind": "task-notification"}, "promptSource": "system",
          "message": {"role": "user", "content": "<task-notification>\n<task-id>a1</task-id>"}}
old_notice = prompt("<task-notification>\n<task-id>a1</task-id>")
peer = {"type": "user", "origin": {"kind": "peer"},
        "message": {"role": "user", "content": "Another Claude session sent a message: <agent-message from=\"a1\">"}}
pb = "⚡ ProofBuild · Project Compass — build and record direction"
for arrived in (notice, old_notice, peer):
    # As it happened: skills loaded, a notice arrived, then the final reply's ⚡ line.
    assert check(prompt("finish these"), skill("proof-driven-dev"), skill("project-compass"),
                 arrived, say(pb + "\nall five skills are in")) == [], arrived
# A real prompt from the human still starts a new turn.
human = {"type": "user", "origin": {"kind": "human"}, "promptSource": "typed",
         "message": {"role": "user", "content": "next"}}
assert check(prompt("a"), skill("impact-map"), human, say("⚡ Impact Map — x")) == ["impact-map"]

# Non-hub names in the line are ignored.
assert check(prompt("x"), say("⚡ Ponytail — lazy mode")) == []

# A colon also ends the names: "⚡ A · B: reason" names both.
assert check(prompt("x"), say("⚡ Standards Compass · Proof Driven Dev: the timeout needs proof"),
             skill("standards-compass")) == ["proof-driven-dev"]

# A /name typed mid-prompt is never expanded, so it must load; paths and URLs are not names.
assert check(prompt("two taps? /engineering-investigator"), say("⚡ Engineering Investigator — tracing")) \
    == ["engineering-investigator"]
assert check(prompt("two taps? /engineering-investigator"), skill("engineering-investigator")) == []
assert check(prompt("see skills/impact-map/SKILL.md and https://x.io/impact-map"), say("ok")) == []
# A second /name in a command's arguments must load too; the command itself counts as loaded.
cmd = prompt("<command-name>/standards-compass</command-name>\n<command-args>add a modal /proof-driven-dev</command-args>")
assert check(cmd, say("done")) == ["proof-driven-dev"]

# End to end: blocks once with a reason, never when stop_hook_active, tolerates bad input.
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as t:
    t.write("\n".join(json.dumps(e) for e in (prompt("x"), say(line), skill("deployment-compatibility"))) + "\n")
run = lambda stdin: subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True)
blocked = run(json.dumps({"transcript_path": t.name}))
assert blocked.returncode == 2 and "production-guard" in blocked.stderr
assert run(json.dumps({"transcript_path": t.name, "stop_hook_active": True})).returncode == 0
# The final reply may not be in the file yet; the hook input carries it.
with open(t.name, "w") as f:
    f.write(json.dumps(prompt("x")) + "\n")
late = run(json.dumps({"transcript_path": t.name, "last_assistant_message": "⚡ Impact Map — rename reaches SQL"}))
assert late.returncode == 2 and "impact-map" in late.stderr
assert run("not json").returncode == 0
assert run(json.dumps({"transcript_path": "/nonexistent"})).returncode == 0
os.unlink(t.name)

print("stop-announced-skills: all checks passed")
