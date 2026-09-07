# Project profiling

Applicability is a function of what the software *is*. Get the profile wrong and
every downstream conclusion is confidently misdirected — which is worse than no
assessment, because it looks like work.

The profile is cheap. It is a targeted read of manifests, entry points, schema,
routes, configuration and deployment files, not a full pass over the codebase.
Ten minutes of profiling saves an hour of assessing the wrong things.

## What the profile records

Every line carries a label: `OBSERVED` (read directly, with where), `INFERRED`
(concluded, with confidence and what would overturn it), `STATED` (the user told
you), or `UNKNOWN`.

```
Type            Public multi-tenant SaaS web application + JSON API   OBSERVED
                  next.js app router; /api routes; organizations table with
                  tenant_id on 14 tables
Stack           TypeScript, Next.js, Postgres via Prisma, Redis, S3   OBSERVED
Auth            Session cookie + custom middleware                     OBSERVED  src/middleware/auth.ts
Personal data   name, email, phone, address, uploaded documents        OBSERVED  prisma/schema.prisma
Payments        Stripe Checkout (hosted), webhooks                     OBSERVED  src/api/billing/*
AI              OpenAI chat over customer records                      OBSERVED  src/ai/assistant.ts
Deployment      Vercel + AWS S3; no IaC in repo                        INFERRED (High)
Users           UNKNOWN — no evidence of who the customers are
Jurisdictions   UNKNOWN — ask; changes privacy applicability materially
Maturity        Production                                             INFERRED (Medium)
                  from: CHANGELOG releases, staging/production configs, error tracking
```

## Application type

Determine from structure, not from the README's self-description.

| Type | Signals |
| --- | --- |
| Web application | Templates or JSX, routing, static assets, a frontend build |
| API / backend service | Route definitions with no view layer, OpenAPI, client SDKs |
| SaaS / multi-tenant | Tenant or organization identifiers threading through schema and queries |
| Mobile application | `Info.plist`, `AndroidManifest.xml`, React Native or Flutter manifests |
| Desktop | Electron main process, Tauri, platform packaging |
| CLI | Bin entries, argument parsers, no server |
| Data platform | ETL/DAG definitions, warehouse connectors, notebooks in the pipeline |
| AI / ML application | Model SDKs, prompt construction, vector stores, inference endpoints |
| Embedded / IoT | Cross-compilation, firmware build, device SDKs, hardware abstraction |
| Internal tool | No public registration path, SSO-only auth, internal hostnames |

More than one is normal. A SaaS product with a mobile client and a data pipeline
is three profiles that share a database, and their applicable standards differ.

## Interfaces and boundaries

Where does untrusted input enter, and where does privileged action happen?

- Public routes versus authenticated versus admin
- Webhooks and callbacks, and whether they verify signatures
- File uploads and downloads
- Background jobs, schedulers, queue consumers
- Third-party calls out, and what is sent
- Model calls, and what goes into the prompt

This list drives the evidence phase directly. Everything here is a place a
control either exists or does not.

## Data categories

**Do not infer a sensitive category without evidence.** This is the rule that
keeps a report credible. A `patients` table is evidence. A wellness app storing
step counts is not automatically health data in a regulatory sense.

| Category | Evidence that establishes it |
| --- | --- |
| Personal data | Names, emails, phones, addresses, identifiers tied to a person |
| Sensitive personal data | Health, biometric, racial or ethnic, political, religious, sexual orientation, trade union — as actual fields, not as a guess |
| Health data | Clinical fields, provider identifiers, medical record numbers, healthcare integrations |
| Financial | Account numbers, balances, transactions, tax identifiers |
| Payment card data | PAN, CVV, expiry, or a card form the application itself renders |
| Credentials | Password hashes, tokens, API keys belonging to users |
| Location | Coordinates, geofences, address histories |
| Children's data | Age fields, parental consent flows, an evidently under-13 audience |
| Uploaded documents | Any user file store, whose contents are unknown by definition |
| Confidential business data | Contracts, pricing, internal reporting |
| AI prompts and outputs | Stored conversations, logged prompts, embeddings of customer content |

Uploaded documents deserve their own attention: the application does not know
what is in them, so their sensitivity is the maximum of what a user might
plausibly upload, not the minimum the schema implies.

## Money, privilege and automated decisions

Three questions with outsized effect on applicability:

- **Does money move?** Payments, refunds, payouts, credits, invoices. Then
  determine the architecture (`payments.md`) before naming a standard.
- **Is there privileged access?** Admin panels, impersonation, bulk export,
  support tooling. These concentrate risk more than any other feature class.
- **Are decisions made about people automatically?** Scoring, ranking,
  eligibility, moderation, pricing. This is where AI regulation and privacy law
  actually bite, far more than a chat feature.

## Maturity

Maturity changes what counts as a finding. Infer it, state the inference, and
let the user correct it.

| Level | Signals | Assessment posture |
| --- | --- | --- |
| Prototype | No releases, no CI, no environments, single contributor, TODOs in core paths | Dangerous mistakes only |
| MVP | Deployed, few users, thin tests, some CI | Security and data handling; skip process findings |
| Production | Real users, releases, monitoring, environments | Full technical assessment; operational evidence expected |
| Business-critical | Revenue depends on it, on-call, SLAs | Add availability, recovery, auditability |
| Regulated / high assurance | Regulated data or sector, audit obligations, formal QMS | Traceability and evidence become findings in themselves |

## Context that code cannot give you

Industry, customer type, jurisdictions, whether the organization has an ISMS,
whether a customer has asked for SOC 2, whether the product is sold in the EU.
These change applicability more than anything in the code.

Ask for them **only where the answer changes the assessment**, at most a handful
at a time, with a stated default so silence is a usable answer:

> Two things change what applies here: are your users in the EU or UK, and has
> any customer asked you for a SOC 2 report or an ISO 27001 certificate? If you
> would rather not decide now, I will assess the technical controls that apply
> either way and mark the jurisdictional questions as unresolved.

Then proceed. A blocked audit helps nobody.

## Systems made of more than one repository

Large products are several repositories, and a report that silently treats one
of them as the whole system is misleading even when every finding in it is
correct. Say what you are assessing.

```
Assessment scope   The `billing-api` service
System context     Part of a product also comprising `web`, `worker`, and
                   `infra`, which were not assessed
Inherited          Authentication is performed at the gateway (referenced in
                   src/middleware/auth.ts:8 but implemented elsewhere) —
                   assessed as EXTERNAL, not as missing
```

Three distinctions that matter once more than one repository is in play:

- **System-level versus service-level.** A finding that a service has no rate
  limiting may be a system-level `PASS` if the gateway does it. Say which level
  the finding belongs to, and mark the cross-repository claim as unverified
  unless you have actually seen the other side.
- **Control ownership.** For each area, who owns it — this service, another
  service, the platform team, the cloud provider, an identity or payment
  provider? An owner outside the repository makes the status `EXTERNAL`, and the
  report's job is to route it, not to grade it.
- **Inherited controls are not gaps.** A managed platform supplying TLS, a
  provider supplying card handling, an identity provider supplying MFA — report
  as *potentially inherited, verify externally*. A report that lists these as
  missing trains its reader to skim.

When several services are assessed together, keep findings attributed to the
service they live in, and raise a system-level finding only where the *gap is
between* services — an authorization rule enforced in one and assumed in another
is exactly that, and it is the most valuable finding this shape of assessment
produces.

## Safety-critical detection

If the profile suggests the software can cause physical harm — medical device
software, vehicle or industrial control, avionics, energy — stop and say so.
Domain-specific safety standards and professional review apply, and a
repository-level assessment is not a substitute for either. Offer the general
engineering assessment explicitly framed as *not* a safety assessment.
