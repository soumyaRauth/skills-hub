"""Read Claude Code transcripts (~/.claude/projects/<project>/<session>.jsonl).

Three facts about the format shape everything here:

- One API response is written as several entries, one per content block, each
  repeating the same message.id and the same usage. Usage is counted once per
  message.id, or a turn is counted two or three times over.
- A turn is everything from one human prompt to the next. Tool results, skill
  bodies, task notifications and agent messages arrive as "user" entries too,
  and do not start a turn. Newer transcripts tag each entry of a turn with the
  prompt's promptId, which is also what hooks receive as prompt_id.
- Subagents write to <session>/subagents/*.jsonl. Their calls count toward the
  quota and toward the turn that spawned them, never toward the main context.
"""
import glob
import json
import os
import re
from datetime import datetime

USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
DELIVERED = ("<task-notification>", "Another Claude session sent a message:", "<agent-message",
             "<cross-session-message", "<local-command-stdout>", "<local-command-stderr>",
             "<local-command-caveat>", "<bash-stdout>", "<bash-stderr>")


def parse_ts(value):
    """ISO-8601 (with Z) to epoch seconds, or None."""
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


class Call:
    """One API response, with its usage counted once."""
    __slots__ = ("id", "ts", "model", "input", "cache_creation", "cache_read", "output", "sidechain")

    def __init__(self, id, ts, model, usage, sidechain=False):
        self.id, self.ts, self.model, self.sidechain = id, ts, model, sidechain
        self.input, self.cache_creation, self.cache_read, self.output = (int(usage.get(k) or 0) for k in USAGE_KEYS)

    @property
    def context(self):
        """Tokens of context this call read: what Claude Code's used_percentage counts."""
        return self.input + self.cache_creation + self.cache_read

    @property
    def total(self):
        return self.context + self.output


class Turn:
    __slots__ = ("prompt_id", "text", "ts", "cwd", "calls", "sub_calls", "ctx_before")

    def __init__(self, prompt_id, text, ts, cwd, ctx_before):
        self.prompt_id, self.text, self.ts, self.cwd, self.ctx_before = prompt_id, text, ts, cwd, ctx_before
        self.calls, self.sub_calls = [], []

    @property
    def total(self):
        return sum(c.total for c in self.calls) + sum(c.total for c in self.sub_calls)

    @property
    def ctx_after(self):
        return self.calls[-1].context if self.calls else self.ctx_before


class Session:
    def __init__(self, path):
        self.path = path
        self.session_id = os.path.splitext(os.path.basename(path))[0]
        self.turns = []
        self.calls = []  # main-chain calls, in order
        self.cwd = None

    @property
    def context(self):
        """Current context: the latest main-chain call's input side, or None before any call."""
        return self.calls[-1].context if self.calls else None


def _content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text"
                         and not str(b.get("text", "")).lstrip().startswith("<system-reminder>"))
    return ""


def is_human_prompt(entry):
    """A prompt the person typed (or a slash command they ran), not something delivered on their behalf."""
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSynthetic") or entry.get("isSidechain"):
        return False
    if "toolUseResult" in entry or "tool_use_result" in entry or entry.get("isCompactSummary"):
        return False
    if (entry.get("origin") or {}).get("kind") not in (None, "human"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list) and not all(isinstance(b, dict) and b.get("type") == "text" for b in content):
        return False  # tool results
    text = _content_text(content)
    return bool(text.strip()) and not text.lstrip().startswith(DELIVERED)


def _usage_call(entry):
    if entry.get("type") != "assistant":
        return None
    msg = entry.get("message") or {}
    usage = msg.get("usage")
    if not isinstance(usage, dict) or msg.get("model") == "<synthetic>":
        return None
    mid = msg.get("id") or entry.get("requestId") or entry.get("uuid")
    return Call(mid, parse_ts(entry.get("timestamp")), msg.get("model"), usage, bool(entry.get("isSidechain")))


def _entries(path):
    try:
        with open(path, "rb") as f:
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return
    for line in data.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue  # a partially written last line
        if isinstance(entry, dict):
            yield entry


def subagent_files(path):
    base = os.path.splitext(path)[0]
    return sorted(glob.glob(os.path.join(base, "subagents", "*.jsonl")))


def parse_session(path, seen=None):
    """Turns and calls of one transcript, subagent calls attributed to the turn they ran in.

    `seen` is a set of message ids already counted elsewhere (a resumed session
    copies earlier history into its new file); those calls are skipped.
    """
    seen = set() if seen is None else seen
    s = Session(path)
    turn, ctx = None, None
    for e in _entries(path):
        s.cwd = s.cwd or e.get("cwd")
        if is_human_prompt(e):
            pid = e.get("promptId")
            if turn is not None and pid and pid == turn.prompt_id:
                continue  # a second entry of the same prompt
            turn = Turn(pid, _content_text((e.get("message") or {}).get("content")).strip(),
                        parse_ts(e.get("timestamp")), e.get("cwd"), ctx)
            s.turns.append(turn)
            continue
        call = _usage_call(e)
        if call is None or call.id in seen:
            continue
        seen.add(call.id)
        if call.sidechain:
            if turn is not None:
                turn.sub_calls.append(call)
            continue
        s.calls.append(call)
        ctx = call.context
        if turn is not None:
            turn.calls.append(call)
    starts = [t.ts for t in s.turns]
    for sub in subagent_files(path):
        for e in _entries(sub):
            call = _usage_call(e)
            if call is None or call.id in seen or call.ts is None:
                continue
            seen.add(call.id)
            idx = max((i for i, t in enumerate(starts) if t is not None and t <= call.ts), default=None)
            if idx is not None:
                s.turns[idx].sub_calls.append(call)
    return s


def main_transcripts(root):
    """Session transcripts under root, oldest first, excluding subagent files."""
    files = [p for p in glob.glob(os.path.join(root, "*", "*.jsonl"))]
    return sorted(files, key=lambda p: (os.path.getmtime(p), p))


def project_dir_for(cwd, root):
    """Claude Code names a project's folder after its path, every non-alphanumeric replaced with '-'."""
    return os.path.join(root, re.sub(r"[^A-Za-z0-9]", "-", cwd))


def find_transcript(root, cwd=None, session_id=None):
    if session_id:
        hits = glob.glob(os.path.join(root, "*", f"{session_id}.jsonl"))
        return hits[0] if hits else None
    if cwd:
        local = glob.glob(os.path.join(project_dir_for(cwd, root), "*.jsonl"))
        if local:
            return max(local, key=os.path.getmtime)
    files = main_transcripts(root)
    return files[-1] if files else None


def scan_calls(root, since, until=None):
    """Every API call (main, sidechain, subagent) in any transcript between since and until, counted once."""
    seen, out = set(), []
    for p in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
        try:
            if os.path.getmtime(p) < since:
                continue
            with open(p, "rb") as f:
                data = f.read().decode("utf-8", "replace")
        except OSError:
            continue
        for line in data.splitlines():
            if '"usage"' not in line:
                continue  # cheap skip: most lines are not API responses
            try:
                e = json.loads(line)
            except ValueError:
                continue
            call = _usage_call(e) if isinstance(e, dict) else None
            if call is None or call.ts is None or call.id in seen:
                continue
            if call.ts < since or (until is not None and call.ts > until):
                continue
            seen.add(call.id)
            out.append(call)
    out.sort(key=lambda c: c.ts)
    return out


def burn_rate(calls, now, minutes):
    """Tokens per minute over the last `minutes`, measured from the first call in that span.

    The span is at least five minutes so one call just now does not read as an
    enormous rate. Returns 0.0 when nothing ran in the span.
    """
    since = now - minutes * 60
    recent = [c for c in calls if c.ts >= since]
    if not recent:
        return 0.0
    span = max(now - recent[0].ts, 300.0)
    return sum(c.total for c in recent) / (span / 60.0)
