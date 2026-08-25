# Intent Analysis

The gap between what a developer types and what they want is filled by the
repository, not by a questionnaire. Read first. Ask last. Ask little.

## The intent compiler

From the request, produce:

| Field | Question |
| --- | --- |
| Objective | What outcome does the developer want to exist afterward? |
| Expected behavior | What is observably different once this is done? |
| Constraints | What must not change — API shape, schema, dependencies, budget? |
| Affected areas | Which parts of this repository does that outcome touch? |
| Hidden requirements | What is implied but unsaid — auth, limits, errors, empty states? |
| Likely regressions | What works today that lives close enough to break? |
| Measurable outcomes | Which requirements can be shown true by a command? |
| Ambiguity | What could reasonably be read more than one way? |
| Risk | What is the blast radius if this is wrong? |

The request is the *symptom*. The objective is what the developer would check
before believing the request was satisfied.

## Investigate before asking

"Add bulk upload to the knowledgebase" produces a dozen questions if you read
only the sentence. Most are answered by the code:

| Question | Where the repository answers it |
| --- | --- |
| Which file types? | The existing single-upload validator |
| Size limit? | Upload middleware config, storage client, nginx/body-parser limits |
| Duplicate handling? | The existing create path — unique constraints, upsert logic |
| Who is allowed? | The permission check on the existing upload route |
| Where do files go? | The storage adapter already in use |
| How is progress reported? | Existing async job or streaming pattern, if any |
| What tests exist? | The upload test file, its fixtures, its helpers |

What is left after that is usually one or two genuinely product-level questions —
and often zero.

Read, in order: manifests and scripts; the feature this extends, end to end; its
tests; the CI configuration; recent commits touching the area. That last one is
underrated — `git log` over the target files shows the conventions that survived
review, and the ones that keep getting reverted.

## Ambiguity classes

| Class | Test | Action |
| --- | --- | --- |
| **Resolvable** | The repository shows the answer | Proceed. Do not mention it. |
| **Safe default** | Ambiguous, but one option is conventional, reversible, and non-destructive | Proceed; record it under `assumptions`. |
| **Material** | Two readings produce meaningfully different products, and choosing wrong wastes real work | Ask one compressed question. |
| **Blocking** | Cannot proceed without irreversibly guessing — data loss, security posture, external contracts | Stop and ask. |

The line between safe default and material is **reversibility × visibility**. A
default the developer can change later in one line is safe. A default that
decides how accounts merge is material.

## Asking well

One question. Concrete options. No essay.

```
Decision required:

OAuth sign-in with an email that already has a password account —

  [link automatically]   [require confirmation]   [reject]

Everything else in the contract is ready to implement.
```

Anti-patterns:

- Asking a question the repository already answers.
- Asking four questions when three have safe defaults.
- Asking with no options, forcing the developer to design the answer.
- Explaining the trade-offs at length before the question. Options first; the
  developer will ask if they want the reasoning.
- Asking *after* implementing, when the answer would have changed the code.

## Root-cause reading

Requests often arrive as a mechanism rather than an outcome: *"add caching to
make this endpoint faster."* The objective is the endpoint being fast; caching
is a proposal. If the measurement shows the cost is an N+1 query, caching adds a
new consistency problem on top of the old cost.

State it in one or two sentences and fix the cause:

> The measured cost is 143 queries per request from an unbatched relation load,
> not repeat computation — caching would hide it, not remove it. Fixing the
> query; contract objective is unchanged.

Two limits. Only override the mechanism when you have evidence, not a
preference. And only when the objective still lands — if the developer wants a
cache for a reason outside this request, that is a material question, not a
silent substitution.

## Scope discipline

The contract covers the requested outcome and the behavior that outcome could
break. Not the rest of the repository.

A defect discovered on the way gets one of three treatments:

- **Blocks the outcome** → fix it, and say so in one line.
- **Adjacent, not blocking** → mention once, in the report footer, no fix.
- **Unrelated** → silence, unless it blocked verification.

Handing back a list of everything else wrong with the codebase spends exactly
the attention this skill exists to conserve.
