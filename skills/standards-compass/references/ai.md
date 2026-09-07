# AI assessment

The `/standards ai` focus. Two questions, and confusing them produces either
paranoia or negligence:

```
Is this an AI security problem?     — almost always, if a model reads or writes
                                      anything a user can influence
Is this an AI governance problem?   — only when the AI affects people, decisions,
                                      or an obligation someone must demonstrate
```

A summarize button is the first. An assistant that reads customer records and
takes actions is both. Do not promote every AI feature into a governance
programme, and do not treat a decision-making system as merely a security
question.

## The data boundary

The first thing to establish, and usually the most consequential.

- **What enters the prompt?** Read the prompt construction, not the docs. System
  instructions, user input, retrieved documents, database rows, file contents,
  prior conversation.
- **Whose data is it?** In a multi-tenant system, is retrieval scoped to the
  caller's tenant *in the query*, or filtered afterwards, or not at all? An
  unscoped vector search is a cross-customer leak with a friendly interface.
- **Where does it go?** Which provider, under what terms, in which region, with
  what retention, and whether the account is configured to exclude the data from
  training. That configuration is usually outside the repository — an external
  verification item, and an important one.
- **What is stored?** Prompts and completions in logs, transcripts in the
  database, embeddings of customer content in a vector store. Embeddings are
  derived personal data when the source was personal data; teams routinely miss
  this in deletion paths.

## Prompt injection and input integrity

Any text the model reads can attempt to change what it does. That includes
retrieved documents, uploaded files, web content, database fields written by
other users, and previous turns.

The severity depends entirely on what the model can *do*:

```
Model can only produce text shown to the same user      → LOW to MEDIUM
Model output is rendered as HTML or Markdown links      → escalates: XSS, exfiltration
Model can call tools that read data                     → data exfiltration path
Model can call tools that write, pay, email, or delete  → HIGH to CRITICAL
Model runs in an agent loop with persistent state       → assume compromise is reachable
```

Assess the tool surface directly: what can be invoked, with whose privileges, and
whether the authorization check happens at the tool boundary or was assumed
upstream. **The model must not be the authorization boundary.** If the only thing
stopping a tool call from reading another tenant's data is the prompt, that is a
finding at high severity.

Prompt-level mitigations (delimiters, instructions to ignore injected content)
are partial and cannot be verified statically. Report them as present, not as
effective.

## Output handling

Model output is untrusted input to everything downstream. Check rendering
(HTML, Markdown, links, images that can carry data in a URL), any generated code
or SQL that is executed, any output written to storage and later re-read, and
any output that triggers an action without review.

## Human oversight

For anything consequential — eligibility, pricing, moderation, ranking of
people, support decisions — establish whether a person can see the decision,
override it, and whether the reason is recorded. Absence of oversight on a
consequential automated decision is a finding on its own, and it is the point
where AI regulation actually engages.

## Evaluation and monitoring

Is there any test of model behaviour? Any measurement of quality, refusal rate,
or harm? Any logging that would let someone reconstruct what the model was asked
and what it said, for a support case or an incident? "No evaluation exists" is a
legitimate finding for a production AI feature and an unreasonable one for a
prototype.

## Supply chain

Which model, which version, pinned or floating · prompt templates as code, and
whether changes are reviewed · third-party agent frameworks and plugins, which
execute with the application's privileges · any model weights or datasets pulled
from a public source · fallback behaviour when the provider fails.

## Cost and availability

Unbounded consumption is a real availability risk with a direct financial
consequence. Look for per-user rate limits, token ceilings, timeouts, and
loop bounds on agents. An agent with no iteration cap is an outage waiting for a
prompt.

## Frameworks

OWASP LLM Top 10 for the application security work — it is the most directly
applicable, and most of its risks are visible in code. NIST AI RMF for framing
risk conversations. ISO/IEC 42001 where an organization must demonstrate AI
governance to customers. The EU AI Act where the system is placed on the EU
market — and there, the risk tier is a legal determination, not a technical one.
Most product AI features are not high-risk systems, and treating them as such
produces expensive nonsense.

## What to say

```
Bad   "This AI feature is not compliant with the EU AI Act."
Good  "The assistant retrieves customer records without tenant scoping
       (src/ai/retrieve.ts:34) and can call a tool that sends email
       (src/ai/tools/email.ts). A prompt injected through an uploaded document
       could reach both. That is an authorization and output-handling problem
       first. Separately, if this is placed on the EU market, transparency
       obligations under the AI Act are likely engaged and the risk tier is a
       legal determination — the code cannot settle it."
```
