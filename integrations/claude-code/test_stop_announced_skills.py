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

# Non-hub names in the line are ignored.
assert check(prompt("x"), say("⚡ Ponytail — lazy mode")) == []

# End to end: blocks once with a reason, never when stop_hook_active, tolerates bad input.
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as t:
    t.write("\n".join(json.dumps(e) for e in (prompt("x"), say(line), skill("deployment-compatibility"))) + "\n")
run = lambda stdin: subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True)
blocked = run(json.dumps({"transcript_path": t.name}))
assert blocked.returncode == 2 and "production-guard" in blocked.stderr
assert run(json.dumps({"transcript_path": t.name, "stop_hook_active": True})).returncode == 0
assert run("not json").returncode == 0
assert run(json.dumps({"transcript_path": "/nonexistent"})).returncode == 0
os.unlink(t.name)

print("stop-announced-skills: all checks passed")
