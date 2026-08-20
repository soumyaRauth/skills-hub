---
name: Skill improvement
about: Improve an existing skill's methodology, references, examples, or fixtures
title: "[improve] "
labels: improvement
---

## Which skill

<!-- impact-map | production-guard -->

## What does the skill do wrong today?

<!-- Be specific. "It misses X" is actionable; "it could be better" is not. -->

## Reproduction

<!-- Which fixture or repository, what request, and what the agent produced.
     A transcript excerpt is ideal. -->

**Fixture / repository:**

**Request given:**

**What the agent produced:**

**What it should have produced:**

## Why does the current instruction fail?

<!-- Which phase or rule is responsible? Is it missing, ambiguous, or being
     skipped? -->

## Proposed change

<!-- The edit you would make, and where: SKILL.md, a reference, an example, or a
     fixture. Remember that SKILL.md length is a cost — depth belongs in
     references/. -->

## Evidence discipline check

- [ ] The change does not encourage guessing or reporting relationships without evidence
- [ ] The change does not introduce any invented number, count, or score
- [ ] The change does not let reasoning be reported as an executed result
- [ ] A finding this produces would be actionable, not merely plausible

## Verification

- [ ] I ran the skill against at least one fixture before and after
- [ ] I ran `./scripts/validate.sh`

**Observed difference:**
