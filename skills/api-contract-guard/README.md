# API Contract Guard

An Agent Skill that settles what an interface promises before anyone depends on
it:

> **What does this interface promise — and which of those promises can never be
> taken back?**

```bash
npx skills add soumyaRauth/skills-hub --skill api-contract-guard
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill api-contract-guard --agent claude-code --copy
```

---

## Why it exists

Code is cheap to change. A promise to someone who deploys on their own schedule
is not. After a mobile build ships, a partner integrates, or a webhook receiver
is written, every field name, status code and retry behavior carries weight.

Coding agents build endpoints well. What they miss is that this endpoint is the
first to use offset pagination in an API that uses cursors, or that a `POST`
without an idempotency key will act twice on the client's first retry. Impact
Map finds who depends on an interface *today*. Production Guard checks
idempotency *after* the code exists. Nothing made those decisions *before* the
code, when they were still cheap.

## What it does

```
the surface and its consumers → the house conventions, read from existing interfaces
  → the decisions a consumer will depend on → additive / behavioral / breaking
  → a decisions block before the code, and contract tests handed to ProofBuild
```

```
CONTRACT  GET /v1/invoices — public, API-key clients
FOLLOWS   error envelope (src/api/errors.js:3) · cursor pagination, max 100
          (GET /v1/payments) · integer minor units + currency · ISO-8601 UTC
DECIDES   order by (created_at, id) so cursors stay stable · status is an open
          enum · another customer's invoice returns 404, identical to a missing one
CHANGE    additive
```

Four worked examples: [a public list endpoint](examples/public-list-endpoint.md) ·
[an outgoing webhook](examples/outgoing-webhook.md) ·
[a breaking rename](examples/breaking-rename.md) ·
[the internal endpoint that gets nothing](examples/internal-endpoint.md)

## When it activates

It activates on its own when an interface that others deploy against is added or
changed: public and partner APIs, webhooks, events, SDKs, CLI output. It stays
quiet for internal functions, for UI work, and for endpoints whose every consumer
ships in the same deploy. See [Activation](SKILL.md#activation).

## What it will not do

- **Impose a style guide.** The house style is whatever the repository already
  does. Deviations are written down as decisions, with reasons.
- **Claim consumers it cannot see.** External consumers come from evidence, or
  they are an open question.
- **Lecture.** Every line is a convention followed, a decision made, or a
  question for a person.
- **Review security.** Authorization depth, rate limits and data exposure are
  handed to Standards Compass.

References: [`contract-decisions.md`](references/contract-decisions.md) ·
[`compatibility.md`](references/compatibility.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
