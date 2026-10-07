# Security Validation

## Contents

- How to scope it
- Authentication
- Authorization
- Injection
- Cross-site scripting and output encoding
- Request forgery and cross-origin
- Server-side request forgery
- Files and paths
- Unsafe parsing and deserialization
- Business-logic abuse
- Abuse resistance and resource exhaustion
- Secrets, configuration and transport
- Cryptography
- Dependencies and supply chain
- AI and LLM features
- Data exposure
- Multi-tenancy
- Destructive and privileged operations
- Running the project's own tools
- Reporting security findings

Behavior-oriented, not checklist-oriented. The question is not "does this code
mention authorization?" but "can someone do something here they should not?"

## How to scope it

Run the classes the change actually reaches, not all of them on every diff.
Two passes:

1. **Entry points** — what new or changed input reaches the system: routes,
   form fields, query/path params, headers, cookies, uploaded files, webhooks,
   queue messages, CLI args, imported files, model output.
2. **Sinks** — where that input ends up: a query, a shell, a template, a file
   path, an outbound URL, a deserializer, a redirect, a log line, a response.

A class applies when an entry point in the diff can reach its sink. Trace the
path; a sink with only constant input is not a finding. Classes the change does
not reach are skipped silently, and classes it reaches but you could not trace
go to `UNVERIFIED`.

Search for sinks in the diff first, then the code the diff calls. The
`Sinks to grep` lines below are starting points, not proof: every hit needs a
traced path from untrusted input before it becomes a finding.

## Authentication

Is authentication required for this path? Are unauthenticated requests rejected
by the server, with a status that does not leak whether the resource exists?
Does a new route inherit the middleware everyone assumes it does — or was it
registered outside the protected group?

When the change touches sign-in, sessions or credentials:

- **Sessions** — rotated on login and privilege change (no fixation);
  invalidated on logout and password change; expiry enforced server-side.
- **Tokens** — JWTs verified with a pinned algorithm (no `alg: none`, no
  HS/RS confusion), expiry and audience checked; reset, invite and magic-link
  tokens single-use, short-lived, random and stored hashed.
- **Passwords** — hashed with bcrypt, scrypt or argon2, never a fast hash or
  reversible encryption; no length cap that silently truncates.
- **Brute force** — rate limiting or lockout on login, reset, OTP and MFA
  verification; MFA cannot be skipped by calling the next step directly.
- **Enumeration** — login, reset and sign-up respond the same for existing and
  unknown accounts, in body and timing where it matters.

## Authorization

The highest-yield area in most reviews.

- Can a **different role** perform the operation?
- Can a user act on an **object they do not own** by changing an ID?
- Are **object-level** permissions enforced, or only route-level? Route-level
  auth answers "may this user use this endpoint"; it does not answer "may this
  user touch *this record*".
- In a **bulk** operation, is every item authorized, or only the first?
- Does the **backend** enforce what the UI enforces?
- Can a user **escalate**: set their own role, join another org, approve their
  own request, or reach an admin route by guessing its path?

The last two are the recurring findings. A hidden button is not a permission
check. Verify the server rejects the request when the UI would not have sent it.

## Injection

Untrusted input interpreted as code or structure by some interpreter. The fix is
always the same shape: keep data and code separate (parameters, argument
arrays, auto-escaping), not blocklists.

- **SQL** — string-built queries: concatenation, interpolation, `format`,
  template literals, raw/unsafe ORM escapes, dynamic `ORDER BY` or column and
  table names. Identifiers cannot be bound as parameters, so they need an
  allowlist.
  Sinks to grep: `raw(`, `query(`, `execute(`, `exec(`, `$queryRawUnsafe`,
  `whereRaw`, `orderByRaw`, `.extra(`, `f"SELECT`, `"SELECT … " +`, `${` inside SQL.
- **NoSQL** — request objects passed straight into a filter so `{"$ne": null}`
  or `$where` rides along; operators accepted from the client.
- **OS command** — a shell invoked with a built string. Use an argument array
  and no shell; never pass input as an option (`--` before positional args).
  Sinks: `exec(`, `system(`, `popen`, `shell=True`, `child_process`, backticks,
  `Runtime.exec`.
- **Template (SSTI)** — user input compiled *as* a template instead of passed
  *into* one: `render_template_string`, `Template(user_input)`, `eval` in views.
- **Code evaluation** — `eval`, `new Function`, `exec`, `vm.run*`, dynamic
  `import`/`require` or `getattr`/reflection chosen by input.
- **Others when present** — LDAP filters, XPath, regex built from input (also a
  ReDoS risk), header values with CR/LF (response splitting), log lines that
  accept newlines (forged entries), CSV exports opened in spreadsheets
  (formula injection: cells starting `= + - @`).

## Cross-site scripting and output encoding

- Does user-controlled content reach HTML without the framework's escaping?
  Sinks: `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `|safe`, `{!! !!}`,
  `html_safe`, `raw`, `bypassSecurityTrust*`, `document.write`.
- Is input placed in a context the escaping does not cover: an attribute
  without quotes, a `href`/`src` (`javascript:` URLs), inline `<script>` or
  JSON embedded in HTML, a style attribute?
- Is rich text or Markdown sanitized server-side with an allowlist sanitizer?
- Are user-uploaded HTML or SVG files served from the app's own origin?

## Request forgery and cross-origin

- **CSRF** — state-changing requests authenticated by cookie require a CSRF
  token or `SameSite` cookies plus an origin check; `GET` changes nothing.
- **CORS** — no reflected `Origin` with `Allow-Credentials: true`; no `*` on
  authenticated APIs; no regex that matches `evil-example.com`.
- **Clickjacking** — sensitive pages send `frame-ancestors` or
  `X-Frame-Options`.
- **Open redirect** — `next=`, `returnTo=`, `redirect_uri` checked against an
  allowlist or restricted to relative paths (`//evil.com` is not relative).

## Server-side request forgery

Any feature that fetches a URL the user supplies — webhooks, link previews,
image import, PDF rendering, OAuth/OIDC discovery, "import from URL".

- Is the destination allowlisted, or can it reach `localhost`, `169.254.169.254`
  (cloud metadata), private ranges, or internal service names?
- Are redirects followed to a blocked destination? Is the check done on the
  resolved IP (DNS rebinding), not just the hostname?
- Are non-HTTP schemes (`file:`, `gopher:`) rejected?

## Files and paths

- **Path traversal** — input joined into a filesystem path: `../`, absolute
  paths, encoded variants, and archive entries on extraction (zip slip). Resolve
  then check the result stays under the base directory.
- **Uploads** — type checked by content, not the client's extension or MIME;
  size limited before it is read into memory; stored outside the web root or in
  object storage under a generated name; served with `Content-Disposition` and
  `X-Content-Type-Options: nosniff`; image/document parsers kept patched.
- **Downloads** — a file id is authorized like any other object, not served
  because the URL was guessable.

## Unsafe parsing and deserialization

- Native deserializers on untrusted data: `pickle`, `yaml.load` without a safe
  loader, Java/.NET `ObjectInputStream`/`BinaryFormatter`, PHP `unserialize`,
  Ruby `Marshal`.
- XML parsers with external entities or DTDs enabled (XXE).
- Prototype pollution: deep-merging request JSON into objects (`__proto__`,
  `constructor`).
- Decompression without a size cap (zip bombs); image dimensions trusted before
  allocation.

## Business-logic abuse

Where most money and data actually leaks, and no scanner finds it.

- Negative, zero, huge or fractional quantities and amounts; currency mixing.
- Client-supplied price, discount, total, role, owner or status accepted
  (mass assignment) instead of recomputed or ignored.
- Steps skippable by calling a later endpoint directly; a state that can move
  backwards; a coupon, credit, invite or trial usable twice.
- Races: two concurrent requests both passing a balance or stock check
  (time-of-check to time-of-use). Verify a lock, a conditional update or a
  constraint, not "it is fast enough".
- Replay of a webhook, a payment callback or a signed link.

## Abuse resistance and resource exhaustion

- Rate limits on authentication, password reset, OTP, sign-up, invite, email
  and SMS sending, search, export and any endpoint that costs money per call.
- Unbounded inputs: page size, batch size, request body, file size, regex input
  (catastrophic backtracking), GraphQL depth and complexity.
- Expensive work triggered without auth or per-user quota.

## Secrets, configuration and transport

- No credentials, keys or tokens committed — in code, fixtures, `.env`
  examples with real values, CI files, or the diff's history. Run the project's
  secret scanner if it has one (`gitleaks`, `trufflehog`, `detect-secrets`).
- Debug mode, verbose error pages, admin consoles, GraphQL introspection and
  test routes off in production configuration.
- Cookies for sessions: `Secure`, `HttpOnly`, `SameSite`.
- TLS verification never disabled (`verify=False`, `rejectUnauthorized: false`,
  `InsecureSkipVerify`); HSTS on HTTPS sites.
- Security headers where the app serves HTML: CSP, `nosniff`, `Referrer-Policy`.
- Default credentials, sample users and seeded admin accounts not present in
  production seeds.

## Cryptography

- Randomness for tokens, ids and codes from a CSPRNG (`secrets`,
  `crypto.randomBytes`, `SecureRandom`), never `Math.random` or `rand()`.
- No home-made crypto; no ECB, no static IVs, no MD5/SHA-1 for anything that
  must resist forgery; HMAC compared in constant time.
- Webhook and callback signatures verified on the raw body, with a timestamp
  window against replay.

## Dependencies and supply chain

- Run the ecosystem's audit (`npm audit`, `pnpm audit`, `pip-audit`,
  `bundle audit`, `composer audit`, `cargo audit`, `govulncheck`,
  `dotnet list package --vulnerable`) when the lockfile changed or the release
  is a full release. Report reachable criticals; a CVE in an unused code path
  is a note, not a blocker.
- New packages: `HANDOFF → dependency-guard`.
- CI changes: third-party actions pinned, secrets not exposed to pull requests
  from forks, no `pull_request_target` checking out untrusted code.

## AI and LLM features

When the change sends input to a model or acts on its output:

- Prompt injection: can content a user or a fetched document controls change
  the model's instructions, reach tools, or exfiltrate other users' data?
- Model output treated as untrusted input: never executed, never interpolated
  into SQL, shell or HTML, never trusted for authorization.
- Tool calls scoped to the requesting user's permissions.
- `HANDOFF → standards-compass` for the governance side.

## Data exposure

Check what actually leaves the system:

- API responses, including nested and serialized relations
- Error messages and stack traces
- Logs, especially structured logs that dump whole objects
- Exports, reports, webhooks, analytics and error-tracking payloads
- Cache keys and URLs (tokens in query strings end up in logs and referrers)
- Shared caches and CDNs: authenticated responses not marked cacheable

Look for credentials, tokens, password hashes, internal IDs, other users' data,
and personal information that the endpoint has no reason to return.

## Multi-tenancy

If the repository has tenants, organizations, workspaces, or accounts, verify
that tenant A cannot reach tenant B's data:

- Is the tenant scope applied at the query layer, or remembered by convention at
  each call site? Convention fails eventually.
- Does a new query path include the scope?
- Do bulk, export, report, admin, search-index, cache and job paths include it
  too? These are where scoping is most often forgotten, because they were
  written by someone thinking about volume rather than isolation.

## Destructive and privileged operations

Deletion, role changes, impersonation, credential resets, and financial
mutations deserve: explicit authorization, an audit record identifying the
actor, confirmation for irreversible actions, and rate limiting where
enumeration or abuse is plausible.

## Running the project's own tools

Before reasoning by hand, run what the repository already has and report it as
evidence: its SAST config (`semgrep`, `bandit`, `brakeman`, `gosec`, CodeQL,
ESLint security plugins), its dependency audit, its secret scanner, and any
security tests. A tool that is configured but was not run goes to `UNVERIFIED`;
never report a scan as clean when it did not run.

## Reporting security findings

Give the concrete path, not a category name:

```
🔴 BLOCKER — Bulk deletion authorizes only the requesting user's role,
not each target record.

Evidence:  BulkDeleteController::destroy() calls authorize('bulkDelete', User::class)
           once, then deletes every id in the payload without a per-record check
           (app/Http/Controllers/BulkDeleteController.php:34).
Risk:      A team admin can delete users outside their team by supplying their ids.
Confidence: High — the ids come straight from the request body.
Recommendation: Authorize each target, or scope the query to the actor's team
           before deleting.
```

Severity follows reachability: an injectable sink reached by unauthenticated
input is a 🔴 BLOCKER; the same sink reached only by an admin-controlled setting
is usually 🟠 or 🟡. Do not report theoretical vulnerabilities with no path to
them, and do not escalate a missing defense-in-depth measure to a blocker when
no exploit exists. Precision is what makes the blockers believable.
