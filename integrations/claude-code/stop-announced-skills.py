#!/usr/bin/env python3
"""Claude Code Stop hook: a skill named in the ⚡ line must actually load.

The ⚡ line is written before the work, so it is a promise. This hook holds the
turn to it. When Claude tries to stop, it reads the transcript since the user's
last prompt, collects the Skills Hub skills named in any ⚡ line, and compares
them with the skills actually loaded (Skill tool calls, or a /name the user
typed). If one is missing, it exits 2, which blocks the stop and tells Claude
to load it, or to drop it in one line: `<Skill> dropped: <reason>`.

It never chooses a skill. It only enforces the choice Claude already announced.
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(HERE, "..", "..", "skills")
ALIASES = {"proofbuild": "proof-driven-dev"}  # the name ECOSYSTEM.md and the ⚡ examples use

_spec = importlib.util.spec_from_file_location("statusline", os.path.join(HERE, "statusline-skills.py"))
statusline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(statusline)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def hub_names(skills_dir=SKILLS_DIR):
    """Map every normalized way of writing a skill's name to its slug."""
    names = dict(ALIASES)
    for slug in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, slug, "SKILL.md")
        if not os.path.isfile(path):
            continue
        names[norm(slug)] = slug
        with open(path, encoding="utf-8") as f:
            title = next((l[2:] for l in f if l.startswith("# ")), "")
        if title:
            names[norm(title)] = slug
    return names


def resolve(name, names):
    n = norm(name)
    if n in names:
        return names[n]
    # "Deployment Compatibility" for "Deployment Compatibility Engineer"
    hits = {slug for key, slug in names.items() if key.startswith(n) and len(n) >= 6}
    return hits.pop() if len(hits) == 1 else None


def announced_in(text, names):
    out = []
    for line in text.splitlines():
        line = line.strip().strip("`*>").strip()
        if not line.startswith("⚡"):
            continue
        head = re.split(r"\s[—–-]\s", line[1:], maxsplit=1)[0]
        for part in head.split("·"):
            slug = resolve(part, names)
            if slug and slug not in out:
                out.append(slug)
    return out


def check(lines, names):
    """Return the announced skills that neither loaded nor were dropped."""
    announced, loaded, texts = [], set(), []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if not isinstance(entry, dict):
            continue
        content = (entry.get("message") or {}).get("content")
        if statusline.is_human_prompt(entry):
            announced, loaded, texts = [], set(), []
            raw = content if isinstance(content, str) else " ".join(b.get("text", "") for b in content)
            loaded |= {m.split(":")[-1] for m in re.findall(r"<command-name>/?([\w:-]+)</command-name>", raw)}
            continue
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        for block in content or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                loaded.add(str((block.get("input") or {}).get("skill", "")).split(":")[-1])
            elif block.get("type") == "text":
                texts.append(block.get("text", ""))
                announced += [s for s in announced_in(block.get("text", ""), names) if s not in announced]
    dropped = {resolve(l.split("dropped:")[0], names)
               for t in texts for l in t.splitlines() if "dropped:" in l}
    return [s for s in announced if s not in loaded and s not in dropped]


def main():
    try:
        data = json.load(sys.stdin)
        if data.get("stop_hook_active"):
            return  # already blocked once this turn: never loop
        path = data.get("transcript_path") or ""
        with open(path, "rb") as f:
            f.seek(max(0, os.path.getsize(path) - statusline.TAIL_BYTES))
            lines = f.read().decode("utf-8", "replace").splitlines()
        missing = check(lines, hub_names())
    except (ValueError, OSError, AttributeError):
        return  # no transcript or no skills directory: allow the stop
    if missing:
        # Exit 2 blocks the stop and hands stderr to Claude as the reason.
        print("The ⚡ line announced " + ", ".join(missing) + " but this turn never loaded "
              + ("it" if len(missing) == 1 else "them") + ". Load each with the Skill tool and "
              "pass it what it needs, or, if it no longer applies, write one line: "
              "`<Skill> dropped: <reason>`.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
