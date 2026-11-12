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
from statistics import median, quantiles

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


# Before there is history: a quick answer, a few steps of editing, a long multi-step task.
DEFAULT_STEPS = {"quick": 1, "typical": 4, "heavy": 8}
DEFAULT_EXTRA_PER_STEP = 2_000
MIN_STEP_HISTORY = 5


def step_profile(turns):
    """How many API calls your prompts take: quick (10th percentile), typical (median), heavy (90th).

    Measured, not guessed: on real history the number of steps did not follow
    from a prompt's wording or from the prompts before it, but once the steps
    are known the cost is close to exact. So the honest estimate is a range of
    step counts, taken from your own turns. `turns` is a list of
    (calls, total, before). Returns None with fewer than MIN_STEP_HISTORY turns.
    """
    turns = [t for t in turns if t[0] > 0 and t[2] is not None]
    if len(turns) < MIN_STEP_HISTORY:
        return None
    steps = sorted(t[0] for t in turns)
    cuts = quantiles(steps, n=10, method="inclusive")
    extra = median((total - calls * before) / calls for calls, total, before in turns)
    return {"quick": max(1, round(cuts[0])), "typical": max(1, round(median(steps))),
            "heavy": max(1, round(cuts[-1])), "extra_per_step": max(0, int(extra)), "turns": len(turns)}


def scenarios(context, prompt_tokens, profile):
    """Tokens for a quick, typical and heavy outcome.

    Every step re-reads the whole context, so N steps cost at least N x context:
    that floor is the quick case. Typical and heavy add the measured extra per
    step (outputs, tool results). Adding the extra to the quick case too put
    six of seven one-step answers just below the range, by 0.2% to 7%.
    """
    p = profile or dict(DEFAULT_STEPS, extra_per_step=DEFAULT_EXTRA_PER_STEP)
    base = (context or 0) + prompt_tokens
    return {name: {"steps": p[name], "tokens": int(p[name] * (base + (0 if name == "quick" else p["extra_per_step"])))}
            for name in ("quick", "typical", "heavy")}


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
