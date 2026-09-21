---
name: dependency-guard
description: Decide whether a dependency should come into a project before it is installed — a package, SDK, framework, build tool, GitHub Action or container base image, or a major-version upgrade. Checks whether the need is already met by the codebase, the standard library, the platform or an installed dependency; whether the package is the one intended (a name that resolves, the expected publisher, no typosquat or invented name); what it brings in (transitive packages, install scripts, native builds, license); and whether it is maintained, from observed evidence only. Answers USE EXISTING, ADD, ADD WITH CONDITIONS or DON'T ADD in a few lines. Use when a request would install or replace a dependency, upgrade one across a major version, or asks which library to use. Not for routine patch or minor bumps of an existing dependency that add no transitive packages or install scripts, and not for removing one.
---

# Dependency Guard

> **Should this dependency come in — and is it the one we think it is?**

Most dependencies arrive as a side effect. A request's obvious implementation
is `npm install x`, and that is the whole review it gets. Each one is a lasting
grant: code nobody here wrote runs in the build, frequently at install time; its
transitive tree grows without anyone deciding it should; and a mistyped or
invented name installs somebody else's package.

Coding agents sharpen all three. They reach for a library by reflex, including
for eight lines of code. And they occasionally name packages that do not exist,
which is exactly the gap a squatter registers into.

The deliverable is a decision, not an audit:

```
DEPENDENCY  lodash — debounce for the customer search box
DECISION    USE EXISTING
WHY         The need is one function. src/lib/timing.js already holds throttle();
            a 9-line debounce beside it covers this without a new package.
```

## Activation

**Engage when** the work would add a dependency (a package, SDK, framework,
build or CLI tool, GitHub Action, container base image), replace one with
another, or upgrade one across a major version. Also engage when someone asks
*which library should we use* or *should we add X*, or when a diff adds entries
to a manifest or lockfile.

**Stay quiet when** an existing dependency moves by patch or minor with no new
transitive packages, no new install scripts and no breaking note in its
changelog; when a dependency is removed (what still imports it is Impact Map's
question); and when dev tooling is aligned to versions already in use.

**Depth** `CONSULT`: a decision of three to six lines before the install, then
the work. `ACTIVE` for a major upgrade or a choice between candidates. Never
`GATING`: `DON'T ADD` is advice, and the user decides.

**Composes with** `standards-compass` (audits dependency management and supply
chain as control areas; this skill makes the per-change call) · `impact-map`
(the call sites a major upgrade breaks) · `proof-driven-dev` (the build and
tests that prove an upgrade) · `production-guard` (a major upgrade on its way to
release).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. If it is
  not installed, do the smallest version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **Never invent registry facts.** Versions, release dates, maintainers,
   download counts, advisory identifiers, licenses and transitive counts come
   from output actually read: registry metadata, a dry run, the lockfile diff,
   the ecosystem's audit tool. Anything else is `UNVERIFIED`. A plausible number
   is worse than none, because it is the one that gets repeated.
2. **Resolve the name before anything installs it.** Confirm the exact name
   exists in the registry this project uses, from the publisher expected, with a
   repository that matches the project it claims to be. A name that does not
   resolve is `DON'T ADD` until a human confirms it. Names that sound right and
   do not exist are precisely what squatters register.
3. **Necessity first.** Before evaluating any package, climb the ladder:
   already in this codebase → standard library or platform → an installed
   dependency → a few lines of code → only then something new. Say which rung
   held.
4. **Report the install surface.** `preinstall`, `install`, `postinstall` and
   `prepare` scripts, native builds, and binaries fetched at install time run
   with the developer's and CI's privileges. Whenever they are present, they are
   in the decision.
5. **Count from the lockfile, not from memory.** Transitive growth is measured
   from a dry run or the lockfile diff. When the environment cannot produce one,
   say so.
6. **Follow the house policy.** Range style, lockfile presence, CI actions
   pinned by commit SHA, private registries and scopes: a new entry does what the
   repository already does. A mismatch is a finding.
7. **Read-only until the decision.** Registry queries and dry runs only. Never
   install something "to try it", edit a manifest ahead of the decision, or
   install globally. The install is the requested work. It happens after the
   decision, and not after a `DON'T ADD` unless the user says so.
8. **Short.** The decision fits on a screen. Detail is available when asked for.

## Workflow

### 1. Name the need

One sentence: which capability, for which call site. *A debounce for the search
input* is a need, and *lodash* is one possible answer to it. When the request
names a package, the need is still what gets evaluated.

### 2. Climb the ladder

- **This codebase.** Search for the capability, not the package name. A
  `retry()` in `src/lib/` is a reason not to add a retry library.
- **Standard library or platform.** `fetch`, `AbortController`, `Intl`,
  `structuredClone`, `crypto.randomUUID`, `URL`, `node:test`; `pathlib`,
  `dataclasses`, `zoneinfo`, `tomllib`. Check the runtime version the project
  actually runs (`engines`, `.nvmrc`, `python_requires`, the CI matrix).
- **An installed dependency.** `date-fns` present and the request says
  `moment`. `zod` present and the request says `joi`.
- **A few lines.** When the need is small and well understood (debounce,
  chunk, clamp, a slug), code beats a dependency.

The first rung that holds ends the evaluation: `USE EXISTING`, or a small
implementation.

### 3. Identify the package

Resolve the exact name in the project's registry and read what comes back —
`references/ecosystem-commands.md` has the read-only command for each
ecosystem. Then check identity: a near-miss of a popular name, a scope the
project does not use, a name that also exists on a private registry the project
uses (dependency confusion), or a repository URL that does not match the claimed
project. `references/identity-checks.md` covers each.

With no network, identity is `UNVERIFIED`. The decision is then at most
`ADD WITH CONDITIONS`, and the condition is to confirm the name resolves to the
expected repository before installing.

### 4. Measure what comes with it

- **Install surface:** lifecycle scripts, native addons, downloads during
  install.
- **Transitive growth:** the dry-run or lockfile count, with the command that
  produced it.
- **Where it lands:** runtime or dev; bundle size only when the project has a
  way to measure it, and never estimated.
- **License:** from package metadata, set against the project's own license
  and how it ships. A combination that might not fit is a question for a human,
  never legal advice.

### 5. Read health from evidence

Last release, deprecation notices, an archived repository, the number of
maintainers, advisories reported by the ecosystem's audit tool, a major line the
ecosystem has moved past. Each is a signal with a source, not a score. *Last
published in 2019* is a fact. *Abandoned* is an inference, and it is labeled as
one.

### 6. Decide

| Decision | When |
| --- | --- |
| **USE EXISTING** | A rung below "new dependency" holds |
| **ADD** | The need is real, identity verified, the install surface clean or justified, and health acceptable |
| **ADD WITH CONDITIONS** | Acceptable once stated conditions are met: pin the version, allow its install script explicitly, confirm identity, keep it a dev dependency, vendor it |
| **DON'T ADD** | The name is unresolved or suspicious; the install surface isn't justified by the need; the license conflicts; or a smaller existing option clearly wins |

```
DEPENDENCY  <name@range> — <the need>
DECISION    ADD WITH CONDITIONS
WHY         <one or two lines of the evidence that decided it>
CONDITIONS  <pin · allow-scripts · confirm identity · …>
UNVERIFIED  <what could not be checked in this environment>
```

### 7. After the install, read the diff

The install is the requested work. Afterwards, check the manifest and lockfile
diff:

- only the intended package added at the top level
- the transitive count as measured
- range style consistent with the rest of the manifest
- every `resolved` URL on the expected registry host
- integrity hashes present

Report it in one line: `lockfile: +1 direct, +0 transitive, all from
registry.npmjs.org, integrity present`.

## Major upgrades

A major upgrade is a change to every call site. Read the migration guide or
changelog for each major version crossed, from the project's own repository or
documentation. Then grep for the APIs it removes or changes, and list only the
breaking changes this codebase actually hits. Check peer dependencies and
runtime floors against what the project runs. When the call-site list is
non-trivial, hand it to Impact Map:

```
HANDOFF → impact-map: express 4 → 5 breaks 6 call sites across 3 route files
```

## What this skill is not

- **Not a vulnerability scanner.** It runs the ecosystem's audit tool when one
  is available, and treats the output as evidence, not as the decision.
- **Not a license lawyer.** It reports license facts and flags combinations
  that need a person.
- **Not a supply-chain audit.** Standards Compass assesses dependency management
  and supply-chain integrity for the whole project. This skill decides one
  dependency at a time, at the moment it arrives.

## References

- `references/ecosystem-commands.md` — read-only commands per ecosystem: metadata, dry run, audit, install scripts
- `references/identity-checks.md` — unresolved and invented names, typosquats, dependency confusion, repository mismatch

## Worked examples

`examples/use-existing.md` — lodash for one debounce ·
`examples/unresolved-name.md` — a suggested package that does not resolve ·
`examples/major-upgrade.md` — Express 4 to 5, measured against the call sites ·
`examples/patch-bump.md` — the bump that gets no commentary at all.
