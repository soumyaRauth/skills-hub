# Software quality assessment

The `/standards quality` focus, using ISO/IEC 25010:2023 as vocabulary.

25010 is a **model**, not a conformance standard. There is nothing to pass. Its
value is turning "the code is bad" into a claim about a specific product
property that someone can decide whether they care about — which is the
difference between a finding and an opinion.

The failure mode here is generic code criticism with a standard's name attached.
Every finding names a characteristic, the observable behaviour that puts it at
risk, and why that matters to *this* product.

## The nine characteristics

| Characteristic | The question | Repository evidence |
| --- | --- | --- |
| Functional suitability | Does it do what it is for, correctly and completely? | Tests covering the core workflow; unhandled cases in core logic |
| Performance efficiency | Are time, resource and capacity behaviour acceptable? | N+1 queries, unbounded result sets, missing indexes on filtered columns, absent pagination |
| Compatibility | Does it coexist and interoperate as needed? | API versioning, schema evolution, dependency constraints |
| Usability | Can users achieve their goals? | Mostly not assessable from source. Accessibility is the part that is |
| Reliability | Does it behave correctly over time and recover from faults? | Error handling, retries, idempotency, transaction boundaries, race conditions |
| Security | Covered by `security.md` | — |
| Maintainability | Can it be changed safely? | Duplicated business rules, module boundaries, dead code, test coverage of core logic |
| Flexibility | Can it adapt — scale, install, replace, modify? | Configuration versus hardcoding, coupling to a provider, environment assumptions |
| Safety | Can it avoid harm under fault or misuse? | Only where the product can cause harm — see below |

## Findings worth making

**A business rule implemented in more than one place.** The most reliable
maintainability finding available, and it usually predicts a correctness bug:
the copies drift. Name the locations.

```
The cancellation window is defined in src/services/order.ts:14 and recomputed
inline at src/controllers/order.ts:60. Changing the rule requires finding both.
Relevant to maintainability, and to functional suitability — the two currently
disagree for orders created in the last minute of the window.
```

**Core workflow with no automated verification.** State which workflow and what
it means: nobody can change the payment path with confidence, and there is
nothing to catch a regression before a customer does.

**Error handling that loses information or fails unrecoverably.** Swallowed
exceptions, retries without idempotency, partial writes with no transaction.
Reliability, with a direct data-integrity consequence.

**Performance hazards, stated as hazards.** An N+1 in a list endpoint is a
finding. "This is slow" without a measurement is not — say what the code does
and what would confirm it matters.

## Findings not worth making

Style. Formatting. Naming preferences. Missing comments. Line counts. Framework
preferences. Test coverage as a percentage with no reference to what is covered.
"Insufficient abstraction". None of these belongs in a standards assessment, and
including them costs the credibility of everything around it.

## Safety

25010 added safety as a characteristic. Invoke it only where the product can
actually contribute to harm — medical, industrial, vehicular, energy, or
software controlling something physical. If the profile suggests that, escalate:
domain-specific safety standards and qualified review apply, and a
repository-level assessment is explicitly not a safety assessment.

## Wording

```
Bad   "The project violates ISO 25010."
Bad   "Code quality is poor."
Good  "The primary transaction workflow has no automated tests
       (searched tests/ and src/**/*.test.ts). That reduces confidence in
       functional suitability and reliability — two characteristics ISO/IEC
       25010 defines — and means a regression in order creation would reach
       production undetected. This review cannot establish formal conformance
       to any quality model; 25010 is a model for specifying and evaluating
       quality, not a standard to pass."
```
