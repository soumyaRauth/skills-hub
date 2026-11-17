# Claude Code integration

All of this is optional. The skills work without it: installed with
`npx skills add`, Claude Code shows the model each skill's description, and
the model loads the ones a request needs through its Skill tool. No slash
command is required.

Everything here is specific to Claude Code and kept out of the skills
themselves, so the skills stay portable.

## 1. A standing instruction (recommended)

[`CLAUDE.md`](CLAUDE.md) is a short instruction telling Claude to consider the installed
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

- **Installing all nineteen skills in one step**, and updating them in one step
  later:

  ```
  /plugin marketplace add soumyaRauth/skills-hub
  /plugin install skills-hub@skills-hub
  ```

- **Trying all nineteen skills at once**, without installing anything:
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

It reads the final reply from the hook input as well as the transcript, because
the reply can reach the hook a moment before it reaches the transcript file.
Without that, the hook ran on the turns that needed it and found no ⚡ line to
check.

### A /skill typed anywhere in the prompt

Claude Code expands a slash command only at the start of a prompt. In *"does QC
need two taps? /engineering-investigator"* the skill never loads, and Claude
may announce it anyway. [`prompt-named-skills.py`](prompt-named-skills.py), a
UserPromptSubmit hook, tells Claude which Skills Hub skills the prompt names so
it loads them. The Stop hook above treats those names as announced, so a turn
cannot end without them. A path or URL that contains a skill's name does not
count.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "python3 /path/to/skills-hub/integrations/claude-code/prompt-named-skills.py || true" }
        ]
      }
    ]
  }
}
```

`|| true` matters. Python exits with code 2 when the script is missing (the
clone moved, or an older commit is checked out), and a UserPromptSubmit hook
that exits 2 blocks every prompt. The hook never needs to block, so nothing is
lost. For the Stop hook, whose exit 2 is its signal, guard with
`test -f <path> && python3 <path>` instead.

Check it with `python3 integrations/claude-code/test_prompt_named_skills.py`.

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

## 5. Keep project knowledge current

[`knowledge-check.sh`](knowledge-check.sh) is the Stop hook behind the
[`project-knowledge`](../../skills/project-knowledge/README.md) skill. It is
bash, git and grep: when `.agents/knowledge/` is `LEARN_EVERY` (default 5)
commits behind `HEAD`, it blocks the stop once and asks Claude to run the
skill. It does nothing in a repository without `.agents/knowledge/`.

You don't normally install it by hand. `npx -y github:soumyaRauth/skills-hub
knowledge init` copies it into the repository and registers it in
`.claude/settings.json`, beside the MCP server in `.mcp.json`. See
[setup](../../skills/project-knowledge/references/setup.md).

## 6. Runway: how much room is left

[`runway/`](runway/) answers *can I afford the next prompt?* It is a small
Python tool (standard library only) that reads your transcripts in
`~/.claude/projects/` and reports three things:

- **Context**: tokens in this session's window, the percentage used, and
  roughly how many turns are left before it is full.
- **The 5-hour window**: the percentage used, when it resets, and how many
  minutes and typical turns are left at your current pace.
- **The next turn, before it runs**: what the prompt you just typed will
  cost, and whether it is likely to finish before the 5-hour limit. Runway
  **holds the prompt back** and shows this, so you decide whether to run it.

### Decide before a prompt runs

When you press Enter, Runway estimates the prompt before Claude sees it,
and holds it back. It answers the question that matters most: **how long you
can keep working once this prompt has run**, at your pace, if it turns out
quick, typical or heavy. Nothing has been sent and nothing is spent:

```
⛽ Runway · waiting for you to confirm this prompt

⏳ TIME LEFT after this prompt: ~1h05m of quota at this pace
   if it turns out typical, at your pace over the last 40m · ~1h07m left right now

✅ Should fit, even if it turns out heavy.

   If it turns out  Steps   Tokens   Time left after
   quick                1   360.7k   ~1h06m
 ▸ typical              3     1.1M   ~1h05m
   heavy               19     6.9M   ~55m

   5h window   46% used · resets in 3h53m
   Context     36% used
   Based on    your last 20 prompts · 13 of 15 landed in this range

👉 To run it: press ↑ then Enter within 2 min. To drop it, do nothing; it was not sent.
```

To run it, send the same text again within two minutes (Up, then Enter). To
drop it, do nothing. When the prompt could run out partway, the message says
so (here with the quota set to 92% used, to show it):

```
⛽ Runway · waiting for you to confirm this prompt

⏳ TIME LEFT after this prompt: ~3m of quota at this pace
   if it turns out typical, at your pace over the last 40m · ~5m left right now

⚠️  May not finish before your 5-hour limit if it turns out heavy.

   If it turns out  Steps   Tokens   Time left after
   quick                1   360.7k   ~4m
 ▸ typical              3     1.1M   ~3m
   heavy               19     6.9M   limit hit partway

   5h window   92% used · resets in 2h00m
   Context     36% used
   Based on    your last 20 prompts · 13 of 15 landed in this range

👉 Run it anyway: press ↑ then Enter within 2 min. To drop it, do nothing; it was not sent.
```

`gate` in `config.json` sets when Runway holds a prompt back: `"always"`
(the default) before every prompt, so you decide each time; `"risky"` only
when a prompt may not fit, while the rest run at once with one line; `"off"`
never.

**Why three numbers, not one.** What a prompt costs depends almost entirely
on how many steps Claude takes, and that is decided while it works. On real
history, neither the prompt's wording nor the prompts before it predicted the
number of steps. Once the steps are known, though, the cost is close to
exact. So Runway shows the time left after a quick, a typical and a heavy
outcome, with step counts from your own prompts (10th percentile, median, 90th
percentile), and says how often past prompts landed inside that range. *Fits*
means even the heavy case fits, *won't fit* means not even the quick case
does, and *may not fit* is everything in between.

*Time left* is the room left after the prompt, divided by your pace. Your
pace is tokens per minute over the stretch you have been working, within the
last hour — so twenty minutes of work after an idle hour reads as a
twenty-minute pace, and the message names the span it measured rather than
claiming an hour of it. After a full idle hour it falls back to your average
since the window opened. It stops at the reset: if you would not run out
before the window resets, it says so instead, and `of quota at this pace`
marks the numbers that are your pace rather than the clock.

Only the quota can stop a turn partway through. A full context does not:
Claude Code compacts it and carries on. So context is shown, but it never
pauses a prompt. With no quota reading (an API key and no `token_cap`),
Runway has nothing to compare against: `"always"` still shows the estimate
and says there is no verdict, and `"risky"` lets everything through.

The step counts, the extra per step and the track record are measured from
your history, and re-measured in the background every six hours, so they stay
current without you running anything (`calibrate` does it by hand). Until you
have five prompts of history, the range uses starting defaults (1, 4 and 8
steps) and says so. On the history Runway was built on, the range held 13 of
15 prompts, each predicted only from the prompts before it. The quick case is
a floor (N steps re-read the context N times), and the misses were prompts
heavier than any before them.

To estimate a prompt without sending it, from any terminal:

```
npx -y github:soumyaRauth/skills-hub runway check "refactor the auth module"
```

Example `status` output (the numbers are illustrative):

```
$ npx -y github:soumyaRauth/skills-hub runway status
Context    151,777 / 1,000,000 tokens (15.2%), ~42 turns to full at ~20.1k/turn
Burn       266.2k tokens/min over the last 17m of work (looking back 60 min)
5h window  33.2% used (Claude Code's rate limits), resets in 4h00m
Time left  ~21m (at your pace over the last 17m); ~2 typical turns
```

Install it with one command. It needs Python 3 and nothing else:

```bash
npx -y github:soumyaRauth/skills-hub runway install-hooks --statusline
npx -y github:soumyaRauth/skills-hub runway calibrate
```

`npx ... runway <command>` copies Runway to `~/.claude/runway/bin/` and runs
it from there, so the hook points at a folder that stays put, not at npx's
cache. Each run refreshes that copy. Every command below works the same way.
From a clone, `python3 integrations/claude-code/runway/claude-runway <command>`
works too, and the hook then points at the clone.

`install-hooks` adds a UserPromptSubmit hook to `~/.claude/settings.json`
and, with `--statusline`, sets the status line if you have none. It keeps
everything already there, backs the file up first, does nothing on a second
run, and refuses to write over a settings file it cannot parse. The hook is
guarded with `|| true`, so a moved clone cannot block your prompts.
`uninstall-hooks` takes it back out. Runway's own files live in
`~/.claude/runway/` (`config.json`, `predictions.jsonl`, `actuals.jsonl`,
`limits.json`, `pending.json`).

If you already have a status line, `--statusline` keeps it and prints this recipe instead.
Wiring it is not cosmetic: Claude Code reports the 5-hour quota to the status line and
nowhere else, so until runway's segment runs, `status` cannot show time left. Add it as a
second line (Claude Code shows every line your command prints):

```bash
#!/usr/bin/env bash
input=$(cat)
printf '%s' "$input" | ~/.claude/your-statusline.sh
printf '%s' "$input" | python3 ~/.claude/runway/bin/claude-runway statusline
```

`printf '%s'` rather than `echo`, because the session JSON arrives with backslashes in it
and `echo` in some shells reads those as escapes.

| Command | What it does |
| --- | --- |
| `status` | Context, 5-hour window, burn rate and time left for the session in the current directory (`--session`, `--json`) |
| `check "<prompt>"` | Estimates a prompt and gives the verdict, without sending it anywhere |
| `backtest` | Replays every transcript turn by turn: how many prompts landed inside the quick-to-heavy range, plus the typical case's error against a naive baseline that repeats the previous turn |
| `calibrate` | Measures your step counts, extra per step and track record and writes them into `config.json` (`--dry-run` to only show them). The hook also does this in the background every six hours |
| `accuracy` | Compares the live predictions the hook logged with what those turns actually cost |
| `init` | Writes `config.json` with every setting and a note on each |

### How it counts

- **Each API response once.** Claude Code writes one response as several
  transcript entries, each repeating the same `usage`. Runway counts it once
  per `message.id`. Summing every entry counts most turns two or three times.
- **A turn is many calls.** One prompt runs the tool loop, and every call
  re-reads the whole context, mostly as cache reads. So the cost of a turn
  depends on how many calls it makes and how big the context already is. The
  prompt's own length matters much less. A prompt of N steps costs
  `N × (context + prompt) + N × extra`, where the extra per step is measured
  from your turns. N is the uncertain part, so Runway uses three values of it
  from your own history: quick, typical and heavy.
- **The quota comes from Claude Code when it can.** The status line receives
  `rate_limits.five_hour` (percentage used and reset time) for Pro, Max and
  Ultra plans. The runway segment saves it, and the hook and `status` use it.
  It covers everything your plan counts, including other devices. Without it
  (an API key, or no status line), set `quota.token_cap` in `config.json`, or
  runway shows usage and burn rate and says that time left is unknown.
  Anthropic does not publish plan limits as token counts, so runway ships no
  cap of its own.
- **The context limit comes from Claude Code too.** It is
  `context_window.context_window_size` from the status line (200k, or 1M for
  extended context), or `context_limit` in `config.json`, or 200k by default.

### Why it is built this way

- **The hook speaks through `systemMessage`.** Plain stdout from a
  UserPromptSubmit hook is added to Claude's context, so printing the
  summary there would spend tokens on every prompt to report on tokens.
  `systemMessage` is shown to you, not to the model.
- **No Stop hook.** Claude Code writes the transcript asynchronously, so at
  Stop the last calls of the turn may not be on disk yet. Instead, each prompt
  resolves the earlier, finished turns of its session against their
  predictions, matched by `prompt_id`, and `accuracy` resolves the rest.
- **No tokenizer and no network.** `tiktoken` is OpenAI's tokenizer, not
  Claude's. Calling `count_tokens` would send every prompt over the network
  before it runs. The prompt is a small share of a turn, so a
  characters-per-token approximation is enough.
- **The prompt text is not stored.** A prediction records a hash, the length
  and the tier.
- **The backtest is honest about its sample.** Each turn is predicted using
  only turns that finished before it. A short history says so in the report.

### What it does not know

- Plan limits weight models differently, and runway counts raw tokens. Turns
  left in the window are converted at the percent-per-token the last snapshot
  implies. When other devices used the same window, that rate is higher than
  local usage alone, so the estimate errs toward less runway.
- Claude Code compacts the context automatically before the window is full,
  at a threshold runway does not read, so *turns to full* is an upper bound.
- Background calls that never reach the transcript, such as title generation
  on a small model, are not counted.

Check it with `python3 integrations/claude-code/runway/test_runway.py`.
