"""Check for prompt-named-skills.py. Run: python3 integrations/claude-code/test_prompt_named_skills.py"""
import json
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt-named-skills.py")
run = lambda stdin: subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True)
say = lambda text: run(json.dumps({"prompt": text}))

# Mid-prompt names are relayed, one or several, plugin-namespaced too.
out = say("so qc bundle now requires two taps? /engineering-investigator").stdout
assert "engineering-investigator" in out and "Skill tool" in out
out = say("what breaks? /engineering-investigator /skills-hub:impact-map").stdout
assert "engineering-investigator" in out and "impact-map" in out

# No hub name, a non-hub /name, a path or a URL: silent.
for text in ("fix this bug then", "run /help and /ponytail-review",
             "open ~/skills/impact-map/SKILL.md", "see https://example.com/impact-map"):
    r = say(text)
    assert r.returncode == 0 and r.stdout == "", text

# A task notice or an agent's report that mentions a /skill is not the user asking for it.
for text in ("<task-notification>\n<summary>ran /skills-pipeline</summary>",
             "Another Claude session sent a message:\n<agent-message from=\"a1\">stays quiet for /skills-pipeline",
             "<cross-session-message from=\"w\">use /impact-map</cross-session-message>"):
    r = say(text)
    assert r.returncode == 0 and r.stdout == "", text
r = run(json.dumps({"prompt": "report mentions /skills-pipeline", "origin": {"kind": "peer"}}))
assert r.returncode == 0 and r.stdout == ""
# The user's own prompt with the same words still relays.
assert "skills-pipeline" in say("run this through /skills-pipeline").stdout

# Bad input never fails the prompt.
assert run("not json").returncode == 0 and run("not json").stdout == ""

print("prompt-named-skills: all checks passed")
