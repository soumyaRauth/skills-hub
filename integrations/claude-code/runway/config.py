"""Paths and configuration for claude-runway.

Everything lives under one directory, ~/.claude/runway/ by default:

    config.json        your settings (written by `claude-runway init`)
    predictions.jsonl  one line per prompt the hook predicted
    actuals.jsonl      the measured result for each predicted prompt
    limits.json        the latest quota and context-window size Claude Code
                       reported to the status line

CLAUDE_CONFIG_DIR moves the Claude directory, as it does for Claude Code.
CLAUDE_RUNWAY_HOME moves only runway's own files.
"""
import copy
import json
import os

DEFAULT_CONTEXT_LIMIT = 200_000  # Claude Code's context_window_size default when no larger window is in use

# Starting points used until `claude-runway calibrate` measures your own
# history. They are not measurements: `calibrated` stays null until then, and
# every report says so.
DEFAULT_TIERS = {
    "qa": {
        "keywords": ["what", "why", "how", "explain", "where", "which", "does", "is there", "can you tell",
                     "summarize", "describe", "compare", "should i", "difference"],
        "calls": 1, "extra_tokens": 1_000, "context_growth": 1_000,
    },
    "edit": {
        "keywords": ["add", "change", "fix", "rename", "update", "edit", "remove", "delete", "replace",
                     "write", "create", "tweak", "adjust", "move", "bump", "format"],
        "calls": 4, "extra_tokens": 8_000, "context_growth": 6_000,
    },
    "multi": {
        "keywords": ["refactor", "debug", "investigate", "migrate", "implement", "build", "rewrite",
                     "across", "every file", "all files", "whole", "codebase", "architecture",
                     "end to end", "end-to-end", "set up", "integrate", "failing tests", "root cause"],
        "calls": 8, "extra_tokens": 20_000, "context_growth": 20_000,
    },
}

DEFAULTS = {
    "_doc": ("claude-runway settings. Every key is optional; delete one to get its default back. "
             "Keys starting with _doc are notes and are ignored."),
    "context_limit": None,
    "_doc_context_limit": ("Tokens the context window holds. null uses the size Claude Code reports to the "
                           "status line (200000, or 1000000 for extended context), then 200000."),
    "quota": {
        "_doc": ("The 5-hour window. When the runway status line is installed, Claude Code reports the real "
                 "percentage used and the reset time, and token_cap is not needed. Without it (an API key, or "
                 "no status line), set token_cap to the raw tokens a window allows you, counted the way runway "
                 "counts them: input + cache creation + cache read + output. Anthropic does not publish plan "
                 "limits as token counts, so there is no default."),
        "token_cap": None,
        "window_hours": 5,
    },
    "gate": "always",
    "_doc_gate": ("When to pause a prompt before it runs and show its estimate. \"always\" (the default): every "
                  "prompt, so you decide each time. \"risky\": only when it may not finish before the 5-hour limit; "
                  "the rest run at once with one line. \"off\": never pause, just show one line. To run a paused "
                  "prompt, send it again (Up, Enter) within confirm_seconds."),
    "confirm_seconds": 120,
    "color": True,
    "_doc_color": ("Highlight the time left (and the verdict) in color in Runway's messages. Set false if your "
                   "terminal shows stray codes. The NO_COLOR environment variable also turns it off."),
    "burn_window_minutes": 60,
    "_doc_burn_window_minutes": "Burn rate is measured over this many recent minutes of activity.",
    "chars_per_token": 3.5,
    "_doc_chars_per_token": ("Approximation used to size the prompt and any @file it mentions. The prompt is "
                             "usually a small share of a turn, which re-reads the whole context on every call."),
    "tiers": copy.deepcopy(DEFAULT_TIERS),
    "_doc_tiers": ("A prompt is classified multi, then edit, then qa by its keywords (whole words), and by the "
                   "number of @files it mentions. A turn is predicted as calls x (context + prompt) + extra_tokens; "
                   "the context grows by context_growth. Edit the keywords freely. `claude-runway calibrate` "
                   "replaces calls, extra_tokens and context_growth with medians from your history."),
    "calibrated": None,
}


def claude_dir():
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude")


def projects_dir():
    return os.path.join(claude_dir(), "projects")


def home():
    return os.path.expanduser(os.environ.get("CLAUDE_RUNWAY_HOME") or os.path.join(claude_dir(), "runway"))


def path(name):
    return os.path.join(home(), name)


def _merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load():
    """Defaults overlaid with config.json. A missing or unreadable file means defaults."""
    try:
        with open(path("config.json")) as f:
            user = json.load(f)
    except (OSError, ValueError):
        user = {}
    return _merge(DEFAULTS, user if isinstance(user, dict) else {})


def write_atomic(target, data):
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    tmp = f"{target}.tmp-{os.getpid()}"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp, target)


def init():
    """Write config.json with defaults and notes if it does not exist. Returns (path, created)."""
    target = path("config.json")
    if os.path.exists(target):
        return target, False
    write_atomic(target, DEFAULTS)
    return target, True


def save(cfg):
    write_atomic(path("config.json"), cfg)


def append_jsonl(name, record):
    os.makedirs(home(), exist_ok=True)
    with open(path(name), "a") as f:
        f.write(json.dumps(record, separators=(",", ":")) + "\n")


def read_jsonl(name):
    try:
        with open(path(name)) as f:
            lines = f.readlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out
