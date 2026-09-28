#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook: a /skill typed mid-prompt is a request to load it.

Claude Code expands a slash command only at the start of a prompt. In
"does QC need two taps? /engineering-investigator" the skill never loads, and
Claude may still announce it. This hook names every Skills Hub /name in the
prompt so Claude loads it with the Skill tool; stop-announced-skills.py then
holds the turn to that. It only relays what the user typed, and never picks a
skill itself.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("stop_announced", os.path.join(HERE, "stop-announced-skills.py"))
stop = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stop)


def main():
    try:
        data = json.load(sys.stdin)
        prompt = str(data.get("prompt") or "")
        # A task notice or an agent's report is not the user asking for anything.
        if (data.get("origin") or {}).get("kind") not in (None, "human") or stop.statusline.is_delivered(prompt):
            return
        named = stop.typed_in(prompt, stop.hub_names())
    except (ValueError, OSError, AttributeError):
        return
    if named:
        # Plain stdout on UserPromptSubmit is added to Claude's context.
        print("The user asked for " + ", ".join(named) + " by name in this prompt. Load "
              + ("it" if len(named) == 1 else "each") + " with the Skill tool this turn unless it is "
              "already loaded as the prompt's command, and name it in the ⚡ line.")


if __name__ == "__main__":
    main()
