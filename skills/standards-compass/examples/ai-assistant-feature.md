# Guardrail mode — "add an AI assistant that can access customer data"

The highest-risk shape of ordinary request. The failure mode is building
`POST /chat`, forwarding the customer's whole record to a model, and rendering
whatever comes back.

---

**Request:** *"Add an AI assistant to the support console. It should be able to
look up customer details and draft replies."*

## Before

```markdown
### Standards consideration

This one has more surface than it looks, because the model will read customer
data and produce text that gets acted on. I'll build it with:

- retrieval scoped to the tenant *in the query*, not filtered afterwards
- the tool layer enforcing the agent's authorization independently — the model
  will never be the thing deciding what it may read
- drafted replies rendered as plain text, not HTML, and never auto-sent
- prompts and completions logged with customer identifiers redacted, since a
  transcript store is a second copy of everything the model saw
- a token ceiling and per-user rate limit, because an unbounded assistant is an
  outage with a bill attached

Two things I can't settle from the code, worth checking before this ships:
whether your model provider account excludes this data from training, and
whether support transcripts fall under your retention commitments to customers.

Implementing now.
```

## During

The retrieval layer is being written as a vector search over all cases with a
post-filter on tenant:

> Moving the tenant filter into the search query rather than filtering results
> afterwards. Post-filtering means the model's context can be assembled from
> other customers' cases before anything is dropped, and the ranking itself
> leaks — a nearest-neighbour hit tells you a similar case exists elsewhere.

## After

```markdown
### Standards check — support assistant

✓ Retrieval scoped by tenant at the query — src/ai/retrieve.ts:22
✓ Tools re-check the agent's permissions per call — src/ai/tools/*.ts
✓ Output rendered as text; drafts require an agent to send
✓ Per-user rate limit and 8k token ceiling
✓ Transcripts stored with customer identifiers redacted — src/ai/log.ts
⚠ Prompt injection: case notes and uploaded document text enter the prompt.
  The tools are read-only and scoped, so the worst case I can see is a
  misleading draft rather than data movement — but if a write tool is added
  later, that changes and this should be re-reviewed
⚠ Model and provider are configured but unpinned — src/ai/client.ts:8.
  Behaviour will change under you when the provider updates the default
✕ Provider data handling: not verifiable from the repository. Confirm the
  account's training and retention settings
```

The first warning is doing real work: it states the current blast radius, why
it is currently bounded, and the exact future change that unbounds it.

---

## Where governance comes in — and where it does not

This feature is a **security and privacy** problem. It is not, by itself, an AI
governance programme:

> On the governance side — ISO/IEC 42001 and the EU AI Act come up whenever AI
> touches customers, so worth saying where I think this lands. This assistant
> drafts text for a human to send; it doesn't decide anything about a customer,
> so it reads as low-risk and the obligation most likely to matter is telling
> people they're interacting with AI output. That's a legal determination, not
> mine. If it ever starts deciding — refunds, eligibility, prioritization —
> that changes, and it's worth re-asking then.

Naming the boundary is more useful than either ignoring governance or
manufacturing a compliance project out of a drafting feature.
