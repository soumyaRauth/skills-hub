# The Hypothesis Ledger

A hypothesis is not a guess about what is wrong. It is a **claim that can be
killed**, paired with the observation that would kill it. The ledger is where
those claims live, how they die, and why nobody re-tests them next session.

## Generating hypotheses

Three to six. Fewer and you are committing early; more and each gets no real
test.

Generate them from the symptom and the actual system, never from a stock list.
The generator that works: walk the layers the scope implicates
(`system-boundaries.md`) and ask, at each, *what mechanism here would produce
exactly this pattern, including its scope and its intermittency?*

A pattern the hypothesis cannot explain is a hypothesis that is already in
trouble — write that down when you create it:

```
Symptom: checkout fails for ~5% of attempts, all tenants, since Tuesday.

H1  Bad instance in the pool          explains the 5% and the "all tenants"
H2  Deploy on Tuesday                 explains the start; must also explain why 95% succeed
H3  Payment provider errors           explains intermittency; must explain the Tuesday start
H4  Data-dependent failure            explains a stable fraction if ~5% of carts share a trait
```

Two hypotheses that would be eliminated by the same observation are one
hypothesis for planning purposes. Keep them separate only if their *fixes*
differ.

### Include the uncomfortable ones

Two hypotheses go missing most often, and both are load-bearing:

- **"Our most recent change did this."** Nobody wants it; it is frequently true.
- **"Nothing is wrong with the application."** External, client-side, and
  environmental causes must be in the ledger from the start, or the
  investigation can only ever conclude that the code is guilty.

## Ledger entry

```
H2  Database regression on the checkout path

Plausible     Checkout p95 rose 6× with flat traffic; the endpoint is DB-heavy
              and Tuesday's deploy touched the cart serializer.
Kill          DB time flat across the window, OR the slow requests never
              execute the suspected query, OR the previous version is equally
              slow on the same input.
Evidence for  E4 (trace: 82% of request time inside DB calls)
Evidence vs   —
Status        Investigating          Confidence  Medium
Next          Compare query count for POST /checkout across v1.8 and v1.9 (E-exp2)
```

The `Kill` line is mandatory and is written **before** any evidence is
collected. Writing it first is what prevents the investigation from drifting
into collecting whatever happens to be convenient.

## Statuses

| Status | Meaning | Requires |
| --- | --- | --- |
| `Investigating` | Live, no decisive evidence yet | — |
| `Weakly supported` | Indirect or circumstantial evidence only | Named evidence |
| `Supported` | Direct evidence, alternatives not yet excluded | Named evidence |
| `Confirmed` | Reproduction, controlled comparison, or revert establishes causality | The experiment |
| `Disproven` | Its kill condition was observed | The eliminating evidence |
| `Blocked` | Cannot be tested with available access | What is missing |

`Blocked` is not a soft `Disproven`. A hypothesis nobody could test stays alive
in the conclusion as unresolved uncertainty, and it belongs in the "what is
missing" line of the answer.

Confidence is High / Medium / Low. No percentages unless a real measurement
produced one — "5% of requests" is a rate, "70% confident" is decoration.

## Elimination discipline

- When evidence kills a hypothesis, write the evidence id next to it and set
  `Disproven` in the same edit. An unrecorded elimination gets re-investigated.
- **Disproven stays disproven.** Reopening requires new evidence, named in the
  entry — a corrected symptom statement, a wider window, a flaw found in the
  eliminating experiment. "It still feels likely" is not new evidence.
- Killing the leading hypothesis is the most valuable outcome available and
  should be treated as progress, not as a setback.
- If every hypothesis dies, the symptom statement is wrong. Re-normalize
  (`symptom-normalization.md`) rather than resurrecting the least-dead one.

## Working against confirmation bias

The default failure of a competent investigator is finding a plausible cause
early and spending the rest of the investigation decorating it.

Concrete defenses, in order of usefulness:

1. **Kill conditions written first.** A test designed after the belief tends to
   confirm the belief.
2. **Ask what the leading hypothesis fails to explain.** Every symptom detail it
   cannot account for — the timing, the fraction, the tenants, the unaffected
   comparison — is a crack. Chase the biggest crack.
3. **Run the disconfirming experiment before writing the conclusion.** If the
   database is the suspect, look for requests that are slow *without* touching
   it, not for more requests that touch it.
4. **State the strongest alternative in the conclusion**, and what excluded it.
   An alternative you cannot exclude belongs in the confidence level.
5. **Beware evidence that fits everything.** "The server is under load" is
   consistent with almost any hypothesis and therefore discriminates between
   none.

## Multiple causes

Incidents are sometimes two things at once — a latent bug plus a traffic change,
a slow dependency plus a retry policy that multiplies it. Signs: the leading
hypothesis explains the failures but not their magnitude; or fixing the
identified cause improves things without restoring normal.

Track them as separate hypotheses that are both `Supported`, and say so in the
conclusion. One cause is not a requirement — an incident with two contributing
causes and a stated interaction is a better answer than a tidy single cause that
does not account for the numbers.
