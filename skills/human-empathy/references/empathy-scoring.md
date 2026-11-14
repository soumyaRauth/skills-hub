# The empathy evaluation framework

Ten dimensions that apply to products and books alike, a five-level rubric
with anchors, and a documented rule for the overall score. The rubric exists
so that two careful evaluators looking at the same evidence land on the same
level, and so that every score can be argued with.

## Contents

- Principles
- The five levels
- The ten dimensions
- Scoring each dimension
- The overall score
- Confidence
- When not to score
- Presenting scores

## Principles

- **A score is a summary of evidence, not a measurement.** It never has
  decimals, percentages or a weighted formula behind it.
- **Polish earns nothing by itself.** A beautiful product whose core task
  fails scores low.
- **Insufficient evidence is a result.** Mark a dimension
  `INSUFFICIENT EVIDENCE` when inspection cannot establish it, for example
  Emotional Experience with no access to the running product and no user
  research. Never fill the gap with a middle score.
- **The rubric judges the experience against its own intended people.** An
  expert tool is not marked down for not suiting beginners, unless beginners
  are in its audience.

## The five levels

| Level | Name | General anchor |
| --- | --- | --- |
| 1 | Seriously deficient | The intended person cannot get what they came for, is harmed, deceived or excluded, or is made to feel incapable |
| 2 | Significant weaknesses | They can get there, but with failures that many would not survive: lost work, confusion at core steps, missing prerequisites, broken examples |
| 3 | Acceptable but improvable | The core experience works for the primary person; real friction remains, or edge-case people struggle |
| 4 | Strong | Works well for the primary person and the edge cases checked; minor issues only |
| 5 | Exceptional | Anticipates needs, recovers gracefully, and leaves people more capable and confident than they expected, with evidence beyond the creator's own belief |

A 5 needs evidence from or about real people (research, feedback, testing).
Inspection alone can support at most a 4.

## The ten dimensions

| # | Dimension | Product: asks | Book: asks |
| --- | --- | --- | --- |
| 1 | **Human Understanding** | Does the product reflect a real understanding of who its users are, their context and their job? | Does the book know its reader: level, goal, fears, misconceptions? |
| 2 | **Emotional Experience** | Does it create unnecessary frustration, anxiety, confusion, shame or distrust? Does it build confidence and control? | Does the reader feel capable, patient curiosity encouraged, never stupid? |
| 3 | **Cognitive Simplicity** | Is effort limited to what the task truly needs? Are decisions, memory and steps minimized? | Is load managed: concepts paced, prerequisites first, no unnecessary density? |
| 4 | **Clarity and Communication** | Are labels, messages, states and consequences clear to this person? | Are explanations clear, terms defined, writing precise and readable? |
| 5 | **Personal Relevance** | Does it fit the person's situation and goals, with personalization that genuinely helps and respects privacy? | Are examples, pace and outcomes relevant to the reader's world and goal? |
| 6 | **Accessibility and Inclusion** | Can people with different abilities, devices, languages and experience levels complete the core journey? | Can readers with different abilities, devices and backgrounds read, navigate and use it? |
| 7 | **Respect for the User** | No manipulation, deceptive patterns, nagging or condescension; autonomy and consent honoured | No condescension, no padding to look substantial, no manipulation; the reader's time and money honoured |
| 8 | **Practical Value** | Does the person accomplish their real job, and is it worth the effort? | Can the reader do what the book promised, and was it worth reading? |
| 9 | **Experience Consistency** | Does the product behave and speak consistently across journeys and states? | Are terminology, voice, structure, code style and design consistent across chapters? |
| 10 | **Trustworthiness** | Is it honest about costs, data, consequences and failures, and reliable in what it promises? | Is it technically and factually accurate, honest about limits, with verifiable sources? |

### Anchors per dimension

Use these with the general anchors. They describe typical evidence for levels
1, 3 and 5; levels 2 and 4 sit between.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Human Understanding | Built for the creator; the intended person is undefined or contradicted by the design | The person is defined; the design fits the centre of the audience and misses the edges | Grounded in research about real people; edges anticipated |
| Emotional Experience | Core steps punish (lost work, blame, fear about money or data) | Mostly calm; friction at some steps | Confidence-building at every step, confirmed by feedback or testing |
| Cognitive Simplicity | Core task or chapter overloads the intended person | Workable with effort; some avoidable load | Effort matches the task's real difficulty; nothing unnecessary |
| Clarity and Communication | Core labels, errors or explanations misleading or missing | Clear in the main path; vague in errors or advanced sections | Clear everywhere, including failure paths and hard concepts |
| Personal Relevance | Generic or wrong for the audience | Relevant to the main person; examples or defaults sometimes off | Feels made for each person, without intruding on privacy |
| Accessibility and Inclusion | Part of the intended audience cannot complete the core journey or read the material | Usable with workarounds; known barriers outside the core | Core journey and material usable by the edge cases checked, confirmed with assistive-technology users |
| Respect for the User | Deceptive patterns, manipulation, or condescension in the core experience | Respectful, with nags or minor condescension | Autonomy, consent and time actively protected |
| Practical Value | The core job or promised outcome is not achievable | Achievable with effort or outside help | Achieved efficiently, and people come away more capable |
| Experience Consistency | Contradictory behaviour or terminology that causes errors | Mostly consistent; drift in places | Consistent throughout |
| Trustworthiness | Dishonest, inaccurate in ways people act on, or unreliable in core promises | Accurate in the core; unverified or dated in places | Verified, honest about limits, sources checkable |

## Scoring each dimension

Record, for every scored dimension:

```
Clarity and Communication     2 · Significant weaknesses        Confidence: HIGH
  Evidence      VERIFIED: every server failure renders "Something went wrong"
                (api.js:31); password rules appear only after a failed attempt
                (SignupForm.jsx:64)
  Reasoning     The person cannot tell what failed or what to do at the two
                most likely failure points of the core journey
  Weaknesses    Generic errors; rules hidden until failure; "Submit" label
  Assumptions   Running product not seen; copy taken from source
```

## The overall score

The overall score is derived by a fixed rule, so it can be reproduced and
challenged:

1. At least **six** dimensions must be scored. Otherwise the overall is
   `INSUFFICIENT EVIDENCE`.
2. Take the **median** of the scored dimensions. When the median falls
   between two levels, take the **lower**.
3. **Cap:** if Practical Value, Accessibility and Inclusion, Respect for the
   User or Trustworthiness scores 1, the overall cannot exceed 2. A product
   that deceives people, or a book that cannot deliver its promise, is not
   "acceptable" on average.
4. The overall carries the **lowest confidence** among the dimensions that
   determined it.

Write it as `Overall 2 · Significant weaknesses (median 2.5 of 9 scored,
rounded down; cap not triggered) · Confidence MEDIUM`. Never present it as a
percentage or with decimals of its own.

## Confidence

| Level | When |
| --- | --- |
| HIGH | Based on direct observation of the running product or rendered document, or supplied research, covering the scope |
| MEDIUM | Based on source inspection or sampling, with reasonable inference |
| LOW | Based on partial access, inference from conventions, or a small sample |

Confidence describes the evidence, not how strongly you feel.

## When not to score

- Narrow requests (one error message, one paragraph, one page's layout):
  give findings without scores, and say scores were not produced because the
  scope was too narrow to support them.
- When the person asked for implementation, not evaluation: score only if
  asked.
- Before-and-after scoring of changes you made yourself is allowed, but the
  "after" is a hypothesis until people use it; mark it so.

## Presenting scores

```
EMPATHY SCORES (rubric: references/empathy-scoring.md)
  Human Understanding         3   MEDIUM
  Emotional Experience        2   MEDIUM
  Cognitive Simplicity        2   HIGH
  Clarity and Communication   2   HIGH
  Personal Relevance          3   LOW
  Accessibility & Inclusion   2   HIGH
  Respect for the User        1   HIGH   ← cap applies
  Practical Value             3   MEDIUM
  Experience Consistency      —   INSUFFICIENT EVIDENCE (one journey only)
  Trustworthiness             2   MEDIUM
  Overall                     2 · Significant weaknesses (median 2 of 9; capped at 2) · MEDIUM
```

Each line above must be backed by the per-dimension record in the report.
