"""Check for statusline-skills.py. Run: python3 integrations/claude-code/test_statusline_skills.py"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "statusline-skills.py")
spec = importlib.util.spec_from_file_location("statusline_skills", SCRIPT)
sl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sl)


def prompt(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def skill(name):
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": name}}]}}


def tool_result():
    return {"type": "user", "toolUseResult": {}, "message": {"role": "user", "content": [
        {"type": "tool_result", "content": "ok"}]}}


def lines(*entries):
    return [json.dumps(e) for e in entries]


# Skills invoked this turn are listed once each, namespace stripped, in order.
assert sl.turn_skills(lines(
    prompt("add export"), skill("skills-hub:impact-map"), tool_result(),
    skill("standards-compass"), skill("impact-map"),
)) == ["impact-map", "standards-compass"]

# A new prompt resets: engagement is per request.
assert sl.turn_skills(lines(prompt("add payment"), skill("standards-compass"), prompt("rename button"))) == []

# Skill-body injections and tool results are not new prompts, in either
# transcript flavor (isMeta, or isSynthetic with snake_case tool results).
meta = dict(prompt("<skill body>"), isMeta=True)
assert sl.turn_skills(lines(prompt("x"), skill("impact-map"), tool_result(), meta)) == ["impact-map"]
synthetic = {"type": "user", "isSynthetic": True, "message": {"role": "user", "content": [{"type": "text", "text": "<skill body>"}]}}
snake_result = {"type": "user", "tool_use_result": {}, "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}
assert sl.turn_skills(lines(prompt("x"), skill("standards-compass"), snake_result, synthetic)) == ["standards-compass"]

# Subagent (sidechain) skill calls do not count; garbage lines are skipped.
side = dict(skill("production-guard"), isSidechain=True)
assert sl.turn_skills(["{not json", *lines(prompt("x"), side)]) == []

# Rendering: nothing, plain, colored.
assert sl.render([], color=True) == ""
assert sl.render(["impact-map", "proof-driven-dev"], color=False) == "⚡ impact-map · proof-driven-dev"
assert "\033[32mimpact-map\033[0m" in sl.render(["impact-map"], color=True)

# End to end through stdin, with NO_COLOR honored and bad input tolerated.
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as t:
    t.write("\n".join(lines(prompt("x"), skill("impact-map"))) + "\n")
env = dict(os.environ, NO_COLOR="1")
run = lambda stdin: subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True, env=env)
assert run(json.dumps({"transcript_path": t.name})).stdout == "⚡ impact-map\n"
assert run("not json").stdout == "" and run("not json").returncode == 0
assert run(json.dumps({"transcript_path": "/nonexistent"})).stdout == ""
os.unlink(t.name)

print("statusline-skills: all checks passed")
