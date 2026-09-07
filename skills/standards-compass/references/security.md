# Security assessment

The `/standards security` focus, and the largest evidence surface in most
projects. Order below is investigation order, which is roughly consequence
order.

## Authorization first, not authentication

Most applications get authentication approximately right — a library does it —
and get authorization wrong, because authorization is written by hand at every
call site. Broken access control has led the OWASP risk lists for years for this
reason, and three of the API Top 10's top five are authorization failures.

What to establish:

- Is there one policy, or several? Find the shared middleware or policy layer,
  then find every route that does not use it. **That set is the finding.**
- Object level: does the handler check that *this* user may touch *this* record,
  or only that they are signed in? An id in a path with no ownership check is
  the most common serious finding in any codebase.
- Function level: are admin operations distinguished from user operations by
  more than the URL prefix?
- Property level: can a client set fields it should not — role, tenant, price,
  status — through mass assignment or an unfiltered update?
- Escalation: can a user assign themselves or others a role that grants more
  than they have? Follow role assignment to whatever consumes the role.
- Tenant scoping in multi-tenant systems, which is authorization with a much
  larger blast radius (see below).

## Authentication and sessions

Credential storage algorithm and parameters · account enumeration through
differing responses or timings on login, reset and registration · lockout and
its own denial-of-service risk · token generation randomness · MFA enrolment and
recovery paths, which are usually weaker than the primary path · session
lifetime, idle expiry, server-side invalidation, rotation on privilege change ·
cookie attributes · logout that actually invalidates.

## Input and output

Query construction — parameterization everywhere, and any place a query is built
by concatenation, including ORMs' raw escape hatches · deserialization of
untrusted data · command construction and path handling · template escaping and
any explicitly raw rendering path · redirects built from user input · SSRF
wherever the server fetches a URL it was given · file path construction from
user-supplied names.

## Secrets

Committed credentials in code, config, fixtures, notebooks, CI definitions and
git history. History matters: a deleted secret is still exposed, and the fix is
rotation. Report redacted, with location and exposure. Also check whether secrets
reach logs, error trackers, or client bundles — a server key in a frontend build
is a full compromise wearing a build-configuration mistake.

## Tenant isolation

In multi-tenant systems this is the highest-value detector available, because
one missed scope is a cross-customer breach.

Check every path data can travel: direct queries · joins that reach through an
unscoped table · caches keyed without a tenant · background jobs that run with
elevated context · search indexes · file storage keys · exports and reports ·
webhooks · and anything an AI feature can retrieve. A single unscoped query in a
reporting endpoint undoes correct scoping everywhere else.

## APIs

Rate limiting, and where it is enforced · resource consumption limits including
pagination bounds and query depth · schema validation on input · error responses
that do not leak internals · route inventory versus documented surface —
undocumented and forgotten endpoints are a recurring source of incidents ·
versioning and deprecation · consumption of third-party APIs, where the response
is also untrusted input.

## File uploads

Server-side type and size enforcement · storage location and whether uploaded
content can be served as executable or active content · generated filenames ·
authorization on download as strictly as on upload · malware consideration where
users share files · image and document processing libraries, which are a common
memory-safety surface.

## Cryptography

Algorithm choices and where they came from · key management, rotation and where
keys live · randomness source for anything security-relevant · TLS configuration
in what the repository controls · at-rest encryption claims and whether they are
implemented in the application or inherited from the platform. Hand-rolled
cryptography is a finding by itself.

## Logging, monitoring, error handling

Are authentication failures, authorization denials, privilege changes and admin
actions logged? · Do logs contain credentials, tokens, personal data, or card
data? · Do stack traces or debug output reach users? · Are errors distinguishable
enough to act on without being informative enough to enumerate accounts? · Is
there anything that would alert a human?

## Dependencies and supply chain

Lockfiles present and committed · version pinning, including pinned CI actions ·
audit tooling in CI and whether it gates · outdated versus vulnerable, which are
different claims · dependency confusion risk from mixed registries · build
provenance and artifact signing where the maturity warrants it · secret scope in
CI, particularly on pull requests from forks.

Do not report "43 vulnerabilities" from a scanner. Classify them
(`evidence-model.md`) and report what is reachable.

## Mapping

Findings land on controls, not on standards. Typical references: ASVS for
verification requirements; OWASP Top 10 and API Security Top 10 for
prioritization language; NIST CSF for framing what a repository cannot see;
ISO/IEC 27001 Annex A themes where an ISMS is in play; SSDF for supply chain and
vulnerability handling. One finding, several references.

## Boundaries

Static analysis cannot establish that a control is effective, only that it is
present and shaped correctly. It cannot test business logic abuse, cannot verify
production configuration, and cannot substitute for a penetration test. Say so
where it matters, and never let "no findings in this area" be read as "secure".
