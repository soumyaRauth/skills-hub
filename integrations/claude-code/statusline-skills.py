#!/usr/bin/env python3
"""Claude Code status line segment: the skills engaged in the current turn.

Claude Code pipes session JSON to the status line command on stdin, including
`transcript_path`. This reads the transcript and prints the skills the model
invoked (Skill tool) since the user's last prompt, e.g.

    ⚡ impact-map · standards-compass

It prints nothing when no skill was invoked, so the segment disappears on
ordinary turns and clears on the next prompt. Color is ANSI, which the status
line documents; set NO_COLOR to turn it off.

A skill the user invoked by typing /name is not shown: the prompt already says so.
"""
import json
import os
import sys

TAIL_BYTES = 4 * 1024 * 1024  # ponytail: tail window; a turn larger than this shows its latest part only


def is_human_prompt(entry):
    # A skill's body arrives as a user text entry right after the Skill call,
    # flagged isMeta or isSynthetic depending on the transcript writer.
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSynthetic") or entry.get("isSidechain"):
        return False
    if "toolUseResult" in entry or "tool_use_result" in entry or entry.get("isCompactSummary"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and all(b.get("type") == "text" for b in content)


def turn_skills(lines):
    skills = []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue  # a partially written last line, or the cut edge of the tail window
        if not isinstance(entry, dict):
            continue
        if is_human_prompt(entry):
            skills = []
            continue
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        for block in (entry.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                name = str((block.get("input") or {}).get("skill", "")).split(":")[-1]
                if name and name not in skills:
                    skills.append(name)
    return skills


def render(skills, color):
    if not skills:
        return ""
    if not color:
        return "⚡ " + " · ".join(skills)
    return "\033[1;33m⚡\033[0m " + " \033[2m·\033[0m ".join(f"\033[32m{s}\033[0m" for s in skills)


def main():
    try:
        path = json.load(sys.stdin).get("transcript_path") or ""
        with open(path, "rb") as f:
            f.seek(max(0, os.path.getsize(path) - TAIL_BYTES))
            lines = f.read().decode("utf-8", "replace").splitlines()
    except (ValueError, OSError, AttributeError):
        return  # no session data or transcript yet: print nothing
    out = render(turn_skills(lines), color="NO_COLOR" not in os.environ)
    if out:
        print(out)


if __name__ == "__main__":
    main()
