# Claude Code integration

All of this is optional. The skills work without it: installed with
`npx skills add`, Claude Code shows the model each skill's description, and
the model loads the ones a request needs through its Skill tool. No slash
command is required.

Everything here is specific to Claude Code and kept out of the skills
themselves, so the skills stay portable.

## 1. A standing instruction (recommended)

[`CLAUDE.md`](CLAUDE.md) is ten lines telling Claude to consider the installed
skills without being asked, to load several when several apply, to announce
them with the `⚡` line, and to treat engagement as per-request. Add it to
whichever memory file fits:

- `~/.claude/CLAUDE.md` for every project on this machine
- `./CLAUDE.md` or `./.claude/CLAUDE.md` for one repository, shared with the team

Copy the text, or import it with `@path/to/CLAUDE.md`. Claude Code resolves
`@` imports and asks once before importing a file outside the project.

It helps because a description only says what a skill is for. Nothing in the
description tells the model it may load two skills for one request, or that
it should reach for one before it is named.

The difference is measured. On the [activation suite](../../evals/activation/README.md#results),
the skills alone passed 30 of 38 cases, and the skills with this instruction
passed 37 of 38. Neither setup loaded a skill on any of the 15 cases where the
right answer was to stay quiet.

## 2. Active skills in the status line, in color

The status line is the one Claude Code surface where color is documented. Model
replies render Markdown, and ANSI color in them is not documented, so the `⚡`
line in a reply stays plain text. [`statusline-skills.py`](statusline-skills.py)
reads the transcript Claude Code points it at and prints the skills invoked
since your last prompt:

```
⚡ impact-map · standards-compass
```

It prints nothing on turns where no skill was invoked, so it clears on the next
prompt. Set `NO_COLOR` to drop the color.

In `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 /path/to/skills-hub/integrations/claude-code/statusline-skills.py"
  }
}
```

If you already have a status line, print both. Claude Code shows every line
your command prints:

```bash
#!/usr/bin/env bash
input=$(cat)
echo "$input" | ~/.claude/your-statusline.sh
echo "$input" | python3 /path/to/skills-hub/integrations/claude-code/statusline-skills.py
```

It shows skills the model chose. A skill you invoke by typing `/name` is not
repeated there, because your prompt already names it. The script reads only the
last few megabytes of the transcript, so a single turn longer than that shows
its most recent part. Check it with
`python3 integrations/claude-code/test_statusline_skills.py`.

## 3. The repository as a plugin

`.claude-plugin/plugin.json` makes this repository a Claude Code plugin, and
`.claude-plugin/marketplace.json` makes it installable as one. That serves
three purposes:

- **Installing all twelve skills in one step**, and updating them in one step
  later:

  ```
  /plugin marketplace add soumyaRauth/skills-hub
  /plugin install skills-hub@skills-hub
  ```

- **Trying all twelve skills at once**, without installing anything:
  `claude --plugin-dir /path/to/skills-hub`. Skills then appear namespaced, as
  `skills-hub:impact-map`.
- **Testing activation.** `claude plugin eval` needs a plugin to load. See
  [`evals/activation/`](../../evals/activation/README.md).

None of this changes `npx skills add`, which installs the skills from `skills/`
individually or all at once with `--skill '*'`. Install a skill one way or the
other, not both — the same skill installed twice shows up twice.

## 4. Hold the ⚡ line to its word (recommended)

The ⚡ line is written before the work, so it is a promise. Claude can break it:
it announces `⚡ Deployment Compatibility · Production Guard`, runs the first,
writes `HANDOFF → production-guard` and stops, and the ship verdict never
arrives. The shared protocol says an announced skill must load. This hook makes
that deterministic.

[`stop-announced-skills.py`](stop-announced-skills.py) runs when Claude tries to
end a turn. It reads the turn from the transcript, collects the Skills Hub
skills named in any ⚡ line, and compares them with the skills that actually
loaded. If one is missing, it exits with code 2, which blocks the stop and
tells Claude to load it, or to drop it in one line (`<Skill> dropped:
<reason>`). It never blocks twice in a row, so it cannot loop.

In `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 /path/to/skills-hub/integrations/claude-code/stop-announced-skills.py" }
        ]
      }
    ]
  }
}
```

It reads skill names from this repository's `skills/`, so run it from a clone.
Check it with `python3 integrations/claude-code/test_stop_announced_skills.py`.

This does not make selection deterministic, and nothing here tries to. The
model still decides which skills a request needs. The hook enforces only what
the model already announced.

## What is not here, and why

- **No hook decides which skill to load.** Hooks match strings, and choosing a
  discipline is a judgment about the request and the repository. A keyword hook
  would load Standards Compass for a comment that mentions Stripe, which is
  exactly what the activation suite checks does not happen.
- **No `systemMessage` announcement.** Claude Code already shows each skill load
  in the transcript. A second line per load would be noise.
