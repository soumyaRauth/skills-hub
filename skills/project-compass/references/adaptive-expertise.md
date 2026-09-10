# Adapting to the reader

The finding does not change. The evidence standard does not change. What changes
is vocabulary, how much is explained, and how much is left implicit.

Getting this wrong is not fatal in either direction, but it is asymmetric:
over-explaining to an expert is irritating and recoverable; under-explaining to
a beginner is useless and they will not say so.

## Reading expertise

Never ask. Read it, provisionally, from:

| Signal | Suggests |
| --- | --- |
| Vocabulary — "idempotency", "boundary", "coupling", "invariant" | Senior or above |
| Questions about *how* versus questions about *whether* | Junior versus senior |
| Tooling named before problems | Earlier: tools are how newer engineers think about problems |
| Test structure, error handling, transaction boundaries in existing code | The floor of what they know |
| "Is this the right way to..." | Wants the principle, not just the answer |
| "Just do X" | Wants X |

Hold it loosely. A senior engineer in an unfamiliar domain asks beginner
questions, and a beginner can have read a great deal. Update on every exchange,
and when in doubt state the finding at senior density with the expansion
offered — that is polite in both directions.

## The same finding, four ways

Six permission exceptions and no authorization rule:

**Beginner**

> Something worth naming: each new permission has been added as its own `if`
> statement, and there are six now. That works until two of them disagree — and
> two already do, so a support user can read a report their role should not.
>
> The usual fix is not more code, it is deciding four things: who the users are,
> what they act on, what actions exist, and whether owning something beats your
> role. Once those are written down, the code follows in an afternoon. Want me
> to draft the questions?

**Mid**

> We are at six permission checks across three modules, two of which are
> exceptions to a third. Before the bulk-edit work, it is worth defining the
> rule — subjects, resources, actions, and whether ownership outranks role —
> because that feature will otherwise invent a seventh case.

**Senior**

> We are encoding authorization as exceptions rather than defining it.
> Six call sites, three modules, two contradictions
> (`adjustments.ts:112` vs `:118`). Bulk edit will add a seventh.

**Staff+**

> Authorization is being defined bottom-up by feature work, so the effective
> policy is whatever six call sites add up to — which is currently
> self-contradictory and untestable. The cost is not the code, it is that the
> policy cannot be reviewed by anyone who is not reading the implementation.

Same evidence, same locations, same recommendation. Four lengths.

Note what does not change across the four: every one of them ends in something
to do next. Density is adjustable; the next action is not optional at any level,
and the beginner version is the one where it matters most.

## Beginners

Three things beginners need that experts do not:

1. **The name of the thing.** "This is an authorization model" is genuinely
   useful — it makes the problem searchable and turns confusion into a topic.
2. **Why the decision matters**, in terms of what breaks. Not theory.
3. **A first step small enough to actually take.** "Define your authorization
   model" is not a step. "Answer these four questions" is.

And two things to never do:

- **Never condescend.** Not "as you may know", not "the correct approach is",
  not a tone that implies they should have known. Someone asking about Kafka for
  an app with eleven users is not foolish; they have read that serious systems
  use Kafka, which is true.
- **Never lecture past the question.** Explain the decision in front of them,
  not the field it belongs to.

When someone reaches for heavy machinery too early, the move is not to say no.
It is to make the question concrete:

> Those tools each solve a specific problem. Which one do you have? If the
> answer is "none yet", the simple version will take a day instead of a month,
> and you will know which of them you need when you get there — because
> something will actually be slow, and you will be able to point at it.

## Seniors and above

Assume the concepts. Lead with the pattern, follow with the evidence, stop.

- No definitions of terms they use themselves.
- No explaining why coupling matters.
- Do not soften a finding into vagueness; a senior engineer would rather be told
  they are wrong than be hinted at.
- Do challenge, with locations. "I think this is a boundary problem, not a
  component problem — here is what makes me say that" is a conversation an
  experienced engineer will engage with.
- Expect to be corrected, and take it instantly. They have context you do not,
  and the fastest way to be useful for a year is to be cheap to overrule.

## Project maturity also adapts

An experienced engineer on a two-week-old prototype does not want lifecycle
modeling either. Read both axes:

```
              new project                mature project
beginner      keep them moving           name the concepts as they appear
senior        stay out of the way        systemic patterns, decision debt
```

The top-left cell is where over-intervention does the most damage. Someone
building their first thing needs momentum far more than they need architecture,
and the second-worst outcome available to this skill is a beginner who stops
building because it made the work sound too hard.

The worst is a senior engineer who stops reading it.
