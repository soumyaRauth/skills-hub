"""Predict what the next turn will cost.

A turn is not one API call. Claude Code calls the API once per step of the
tool loop, and every call re-reads the whole context (mostly as cheap cache
reads). So what a turn costs is driven by how many calls it makes and how big
the context already is; the prompt's own size is a small term. The model is

    turn tokens ~ calls x (context + prompt) + extra_tokens
    context after ~ context + prompt + context_growth

with calls, extra_tokens and context_growth set per tier, from defaults until
`calibrate` replaces them with medians measured from your own history.
"""
import os
import re
from statistics import median

TIER_ORDER = ("multi", "edit", "qa")
# @path mentions as Claude Code writes them: @src/app.py, @"path with spaces".
MENTION = re.compile(r'(?:^|(?<=\s))@(?:"([^"]+)"|([^\s"\'`,;()<>]+))')
LONG_PROMPT_CHARS = 4_000  # a pasted spec or log: treated as multi-step work


def mentions(prompt):
    return [m.group(1) or m.group(2).rstrip(".:!?") for m in MENTION.finditer(prompt or "")]


def mention_chars(prompt, cwd):
    """Characters of every @file the prompt names that exists. Directories and missing paths count 0."""
    total, found = 0, []
    for name in mentions(prompt):
        p = os.path.expanduser(name)
        p = p if os.path.isabs(p) else os.path.join(cwd or os.getcwd(), p)
        try:
            if os.path.isfile(p):
                total += os.path.getsize(p)
                found.append(name)
        except OSError:
            continue
    return total, found


def prompt_tokens(prompt, cwd, chars_per_token):
    extra, found = mention_chars(prompt, cwd)
    return int(round((len(prompt or "") + extra) / chars_per_token)), found


def _has(text, word):
    return re.search(r"(?<![a-z0-9])" + re.escape(word.lower()) + r"(?![a-z0-9])", text) is not None


def classify(prompt, tiers, files=0):
    text = (prompt or "").lower()
    if files >= 2 or len(text) >= LONG_PROMPT_CHARS or any(_has(text, k) for k in tiers["multi"]["keywords"]):
        return "multi"
    if files == 1 or any(_has(text, k) for k in tiers["edit"]["keywords"]):
        return "edit"
    return "qa"


def predict(prompt, context, cfg, cwd=None):
    """Prediction for one prompt at the given context size (None before the session's first call)."""
    tiers = cfg["tiers"]
    p_tok, files = prompt_tokens(prompt, cwd, cfg["chars_per_token"])
    tier = classify(prompt, tiers, len(files))
    t = tiers[tier]
    base = context if context is not None else ((cfg.get("calibrated") or {}).get("first_context") or 0)
    calls = max(1, int(round(t["calls"])))
    return {
        "tier": tier,
        "prompt_tokens": p_tok,
        "files": files,
        "context_before": context,
        "calls": calls,
        "tokens": int(calls * (base + p_tok) + t["extra_tokens"]),
        "context_growth": int(p_tok + t["context_growth"]),
        "context_after": int(base + p_tok + t["context_growth"]),
    }


def calibrate(turns, tiers, chars_per_token):
    """Per-tier medians from completed turns; a tier with fewer than 3 turns keeps its current numbers.

    Borrowing the overall median for a thin tier would erase the difference
    between tiers: a history of mostly multi-step work would predict four calls
    for a one-line question.

    Each turn is (prompt, ctx_before, calls, total, ctx_after). Returns
    (tiers with measured numbers, stats), or (None, stats) with no usable turns.
    """
    rows = {}
    for prompt, before, n_calls, total, after in turns:
        if n_calls == 0 or before is None:
            continue
        p_tok = len(prompt or "") / chars_per_token
        tier = classify(prompt, tiers, len(mentions(prompt)))  # the files may be gone; count the mentions
        base = before + p_tok
        rows.setdefault(tier, []).append((n_calls, total - n_calls * base, after - base))
    every = [r for rs in rows.values() for r in rs]
    if not every:
        return None, {}
    out, counts = {}, {}
    for name, t in tiers.items():
        rs = rows.get(name, [])
        counts[name] = len(rs)
        if len(rs) < 3:
            out[name] = dict(t)
            continue
        out[name] = dict(t, calls=round(median(r[0] for r in rs), 1),
                         extra_tokens=int(median(r[1] for r in rs)),
                         context_growth=int(median(r[2] for r in rs)))
    return out, counts
