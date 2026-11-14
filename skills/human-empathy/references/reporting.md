# Reporting

Report formats for evaluations, the format for each significant finding, and
the rules that keep a report decision-ready rather than long.

## Contents

- Sizing the report
- The full evaluation report
- The finding format
- Severity
- Root causes
- The short report
- Verdicts
- What a report must never contain

## Sizing the report

Detailed enough to support decisions; no longer. A focused request (one
screen, one chapter, one question) gets a short report. A whole product,
whole book or readiness decision gets the full report. Omit any section that
would be empty rather than padding it.

## The full evaluation report

```
HUMAN EMPATHY — <mode>
────────────────────────────────────────
1  EXECUTIVE ASSESSMENT
   Three to six sentences: who this is for, whether it serves them, the one or
   two things that matter most, and the overall score with confidence.

2  INTENDED USER OR READER
   The empathy statement and the person profile, with evidence levels and the
   Unknown line.

3  SCOPE OF EVALUATION
   What was inspected and how (running product, source, rendered pages, code
   executed). What was not inspected, and what that limits.

4  OVERALL EMPATHY SCORE
   Derived by the rule in empathy-scoring.md, with confidence.

5  DIMENSION-LEVEL SCORES
   The table, then the per-dimension records.

6  CRITICAL FINDINGS
   Ordered by priority, in the finding format. Verified findings first; a
   separate block for hypotheses.

7  ROOT CAUSES
   The few causes behind the findings, each naming the findings it explains.

8  EVIDENCE AND ASSUMPTIONS
   What the conclusions rest on; assumptions that would change them if wrong.

9  RECOMMENDED IMPROVEMENTS
   Prioritized, each with the finding it fixes, effort, risk, and owner skill
   if another discipline is needed.

10 IMPLEMENTED CHANGES
   Only if changes were made: what, where, how verified.

11 REMAINING RISKS
   What could still fail people, including what was not inspected.

12 RECOMMENDED VALIDATION
   The research that would turn the most important hypotheses into evidence:
   method, who, what question it answers, what result would change course.
```

## The finding format

```
F<n>  <one-line title in the person's terms>
  Finding              What is wrong, specifically
  Affected person      Who, in which situation ("a returning user whose session expired mid-form")
  Evidence             LEVEL: location and observation (file:line, chapter §, page, screenshot)
  Underlying need      The human need this fails (to recover without loss; to know what a term means)
  Root cause           Why it happens (design, content, structure, technical, organizational)
  Impact               What it costs the person: task or learning failure, effort, emotion, trust, exclusion
  Severity             Critical · High · Medium · Low (see below), with frequency if evidenced
  Confidence           HIGH · MEDIUM · LOW
  Recommended solution The specific change, and why it is better for the person
  Validation           How anyone would know it worked
  Status               Proposed · Implemented · Needs decision · Handed off → <skill>
```

Write titles from the person's side: "People lose everything they typed when
sign-up fails", not "Form state reset in catch block".

## Severity

| Severity | When |
| --- | --- |
| Critical | The intended person cannot complete the core task or learning outcome; loses data or money; is deceived; or part of the audience is excluded from the core journey |
| High | Core task or outcome achievable only with significant struggle, lost work, or outside help; trust is damaged; a widely used path fails |
| Medium | Friction or confusion on a secondary path, or on the core path with an easy recovery |
| Low | Polish, consistency, minor wording, with little effect on completion or understanding |

Frequency and reach raise or lower priority only when evidenced (analytics,
support volume, reader reports). Without evidence, say "frequency unknown".

## Root causes

Group findings under causes. Typical root causes:

- **The person was never defined** (the design serves "users" in general).
- **The creator's knowledge leaked in** (curse of knowledge: jargon, skipped
  steps, assumed context).
- **The organization's needs shaped the experience** (marketing fields in
  sign-up, chapters the author wanted to write).
- **Failure paths were never designed** (only the happy path has a design).
- **No shared terminology or system** (each screen or chapter made
  separately).
- **Wrong medium assumption** (a print layout read on screens; a desktop
  design used on phones).
- **Unverified technical content** (examples never run in sequence).

A root cause should explain several findings and suggest a change in process,
not only a patch.

## The short report

For focused requests:

```
HUMAN EMPATHY — <mode> · <scope>
Person     <empathy statement>, <evidence level>
Inspected  <how> · Not inspected <what>

F1 …  (finding format, compressed to the lines that carry information)
F2 …

Root cause   <one or two sentences>
Next         <the most valuable change> · Validate with <method>
```

## Verdicts

Only when a person asked for a decision:

- Pre-release experience: **READY · READY WITH CONDITIONS · NOT READY**
  (`product-evaluation.md`).
- Publication readiness: **READY TO PUBLISH · READY WITH CONDITIONS ·
  NOT READY** (`book-creation.md`).

A verdict names its conditions and what was not checked. It never replaces
the ship decision of `production-guard` or a conformance verdict of
`standards-compass`.

## What a report must never contain

- Invented research, quotes, personas presented as real, numbers,
  percentages, citations or test results.
- A claim that people feel something, stated as fact, without research.
- "Validated", "users love", "readers will understand", or "accessible"
  without the evidence that would support it.
- A score without evidence, or a score where evidence is insufficient.
- Generic advice that would apply to any product or book ("improve the
  onboarding", "make it more engaging").
- Praise to soften findings that the evidence does not support, or
  agreement with the requester that the evidence contradicts.
- Visual polish findings ranked above task, learning or trust failures.
