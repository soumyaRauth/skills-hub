# Example — A clear request is not an incident

The failure this example exists to prevent is the opposite of the usual one. The
usual failure is answering a mystery with a guess. This one is answering a
*non*-mystery with an investigation, and then reporting the investigation.

---

**Request:**

> Only csv upload is allowed at the moment. I need xlsx upload as well.

---

## Route

There is no symptom, no scope question, and nothing competing. The user has
named the change: the upload path accepts CSV, it should also accept XLSX. One
explanation is live — *the feature was never built* — and no experiment could
eliminate anything.

Lane: **DIRECT**. No hypothesis ledger. No `.agent-investigation/`. Manufacturing

```
H1  The parser rejects the mime type
H2  The UI filter excludes it
H3  The storage layer is format-aware
```

would be theatre: every one of them is answered by reading the upload path once,
and none of them is a competing explanation for anything.

## Phase 0 — What can be seen

```
Available      the repository, its test suite, the upload path end to end
Not available  a production environment, real customer workbooks
```

This still matters. It sets what "verified" is allowed to mean at the end.

## The work

Read the path that exists before writing a new one — from the file input to the
persisted rows — and note the three things that decide the change: where the
format is gated, what row shape the CSV parser produces, and what helpers are
already there. The XLSX reader lands beside the CSV one and produces the *same*
row shape, so validation, persistence, and error handling are untouched.

Then verify: the new parser against a real workbook, and the full upload flow
through the route. A check that did not run is not reported as passing.

None of the above appears in the answer. It is how the work is done, not what
the user asked.

## What the user must not receive

```
Searched for 2 patterns, read 4 files, listed 1 directory, ran 4 shell commands

A toBase64 helper already exists in api.ts — reusing it. Writing the backend
reader:

Read 1 file, ran 5 shell commands
Loaded apps/backend/CLAUDE.md

Now the test — a real zip fixture built with stdlib deflate:

Ran 12 shell commands

xlsx upload works end to end. Files:
- planXlsx.ts …
```

Every line of that is activity, not result. The counts tell the reader how busy
the agent was. The file list is already in the diff. The one genuinely useful
sentence — *the format is now accepted end to end, and here is what it does not
cover* — is buried under the transcript.

## Phase 9 — The gate

| | |
| --- | --- |
| What was established? | XLSX uploads work alongside CSV, end to end |
| What evidence supports it? | The parser tests, and the upload-flow test through the route |
| How confident? | High — the checks ran |
| What next? | It is usable; the format edges are not covered |
| Implementation detail needed? | One clause: it reuses the CSV path's row shape. The rest, on request |

Client response: **no**. An engineer asked for a feature; nobody outside the team
is waiting on an explanation.

## The answer

```markdown
## Result

XLSX uploads now work alongside CSV, end to end.

**Cause:** The upload pipeline parsed CSV only.
**Confidence:** High

**Why:** The new reader produces the same row shape the CSV parser already
returned, so validation and persistence were untouched; the parser tests and the
full upload-flow test pass.

**Action:** Ready to use. Formulas, date cells, ZIP64 archives, and choosing
between multiple sheets are not covered — worth deciding whether any of those
matter before this reaches customers.
```

Nine lines. The diff carries the file list; the tests carry the proof.

## If asked *"how exactly did you implement XLSX?"*

Then the mechanism is the answer, and it is given in full: how sheets are
resolved, why the first tab is not always `sheet1.xml`, how the fixture was
built, what the shared-strings handling assumes, which edge cases are deliberate
gaps. That is the same work at higher resolution — not a replay of deliberation,
and not the short answer stretched.

## What this example demonstrates

- **Routing is a decision made before the work**, and the wrong route costs the
  user either rigour or their attention.
- Investigation methodology exists to discriminate between competing
  explanations. With one explanation live, it has nothing to do.
- The discipline that survives DIRECT is the part that matters: read the real
  path, reuse what exists, verify, and never claim a check that did not run.
- The finalization gate is what separates a nine-line answer from a diary — the
  work was identical.
- `### Client response` was omitted because nobody was waiting on one. The
  template is a shape, not a checklist to fill.
