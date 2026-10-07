# Answer Shape

## The shape

```markdown
# Result

[One-sentence conclusion.]

**Cause:** [short cause]
**Confidence:** [High / Medium / Low]

**Why:** [one or two sentences of the evidence that decided it]

**Action:** [what should happen next]
```

The confidence word comes from Phase 7: `CONFIRMED` and `HIGHLY LIKELY` →
**High** · `LIKELY` → **Medium** · `POSSIBLE` → **Low** · `UNKNOWN` → no cause
line at all, use the form below. Say the stronger word in the body when it earns
it — "reproduced on both versions" is worth more to an engineer than the label.

Adapt the shape to the lane. A DIRECT result leads with what now works and what
it was verified against; `Cause` shrinks to a clause about what was missing, or
drops entirely. Never leave a section standing with nothing in it, and never pad
one to make the work look larger.

When nothing is established:

```markdown
# Result

We cannot reliably determine the cause yet.

**What we know:** …
**What is missing:** …
**Next step:** …
```

## Audience

Read the audience from the request, and add a section only when someone is
actually waiting on it:

| The request | What it gets |
| --- | --- |
| An engineer asking for a change, or for a cause | The result in concise technical language. No client paragraph. |
| A customer complaint, support escalation, or a stakeholder waiting | The result **plus** `### Client response` — two or three plain sentences, sendable as written |
| *"How exactly did you implement it?"* | The mechanism, at the depth asked for |
| *"Write it up"* / *"I need a report"* | A report |

`### Client response` is not ceremony every invocation earns. *"Why is this API
returning 500?"* does not need one; *"the customer says the app is slow"* does;
*"add XLSX upload"* does not, unless a customer is waiting on the answer. When in
doubt, leave it out — it is one question away.

## Detail on demand

The compression is only honest because the detail is retrievable. Answer these
fully, reading from the workspace and the evidence rather than re-deriving:

```
show the evidence        show the hypotheses      what did you rule out?
how do you know?         what would change this?  show the experiments
what did you not check?  how exactly did you implement it?
```

An expanded answer is the same case at higher resolution — evidence,
eliminations, mechanism, code. It is never a replay of internal deliberation,
and never a restatement of the short answer at greater length. Never include the
transcript, the ledger, or the commands you ran unless they were asked for.
Translate every technical term for a non-technical reader. See
`references/communication.md`.
