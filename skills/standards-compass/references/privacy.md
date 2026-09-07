# Privacy assessment

The `/standards privacy` focus. The rule that governs everything here: **the
repository shows what happens to data; it does not establish what law applies.**

Personal data in a schema is the trigger to *ask* about jurisdiction, not to
conclude one. A privacy assessment that opens with "GDPR applies" has failed
before it starts.

## Map the data first

Nothing useful can be said until this exists. Build it from the schema, the
models, the API surface and the third-party calls.

```
Category            Where                          Purpose (stated?)   Shared with
name, email         users                          account             SendGrid
phone               users                          2FA + support       Twilio
address             addresses, orders              fulfilment          shipping API
uploaded docs       documents + S3                 UNKNOWN             —
IP + user agent     access logs, analytics         debugging?          analytics vendor
chat transcripts    ai_conversations               product feature     model provider
```

The `UNKNOWN` rows are findings. Data with no recorded purpose is the most
common privacy gap in a codebase, and it is usually the first thing a real
assessment asks about.

## The lifecycle

| | What to look for |
| --- | --- |
| Collection | What is collected, and whether anything is collected that nothing uses |
| Processing | What is derived, inferred, or profiled |
| Storage | Where, encrypted or not, and which copies exist |
| Sharing | Third parties in server code, SDKs in client code, analytics, error trackers |
| Retention | Any expiry job at all. Usually none exists, which is the finding |
| Deletion | What `deleteUser` actually removes, and what it leaves behind |
| Export | Whether a person's data can be produced in a usable form |
| Backup | Whether deletion reaches backups — usually outside the repository |

## Deletion is where the real findings are

Trace a delete end to end. Foreign keys and cascade rules · soft-delete flags
that leave data queryable · related records in other tables, other services,
other databases · search indexes · caches · object storage · logs · analytics
platforms · the model provider, for anything sent to an AI feature · backups.

```
FAIL         deleteUser() removes the users row; email and address remain on
             orders, and the search index is never updated
             src/services/users.ts:88, src/search/index.ts
Gap type     implementation
Relevance    erasure obligations under privacy law, where applicable
```

## Consent, tracking and the client

Cookies and local storage set before any consent decision · analytics and
session-recording SDKs, which often capture far more than the team believes ·
third-party scripts on authenticated pages · tracking identifiers persisted
across sessions · marketing pixels. Client code frequently contradicts the
privacy policy, and that contradiction is a legitimate `CONTRADICTORY` finding.

## Logs

Personal data in application logs is common, invisible, and rarely intentional.
Check what is logged on request, error, webhook and audit paths — full request
bodies, headers with tokens, email addresses used as identifiers. Logs also
usually have their own retention, outside the deletion path.

## Automated decisions

If the system scores, ranks, filters, prices, or moderates people, say so
explicitly. This is where privacy law and AI regulation actually bite, far more
than a chat feature: transparency, contestability, human review, and — under the
California ADMT regulations and the EU AI Act — specific obligations depending
on scope.

## What to say about law

```
Never   "This is GDPR compliant" / "not compliant"
Never   "GDPR applies to you"
Do      "Personal data including <categories> is processed. If the organization
         is established in the EU, or offers services to or monitors people
         there, GDPR obligations are engaged — that determination is legal, not
         technical. On the technical side, three things would matter if it
         applies: deletion is incomplete, there is no retention mechanism, and
         email addresses are written to application logs."
```

The engineering findings are the same whether or not the law applies. Lead with
them. They are also what a team can act on today.

## Organizational versus technical

A repository cannot show records of processing, data processing agreements,
transfer mechanisms, a DPO, DPIAs, a breach procedure, or a retention policy as
an organizational rule. List these as external verification items — not as
failures, and not as things to write into the repository to make a finding go
away.
