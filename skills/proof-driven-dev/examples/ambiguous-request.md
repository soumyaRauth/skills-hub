# Example — An ambiguous request

Nine questions could be asked here. Eight are answered by the repository. The
ninth changes the product, so it is asked — once, with options.

---

**Developer:**

> Add "Sign in with Google".

---

## 1. Every question the request raises

| Question | Class | Resolved by |
| --- | --- | --- |
| Which OAuth library? | resolvable | `omniauth` is already a dependency, used for GitHub sign-in |
| Where do the routes go? | resolvable | `config/routes.rb` — existing `/auth/:provider/callback` |
| How are sessions created? | resolvable | `SessionsController#create` — the GitHub flow's pattern |
| What identity data is stored? | resolvable | `identities` table: provider, uid, user_id |
| Where do credentials live? | resolvable | `Rails.application.credentials` — GitHub's are there |
| Is a new user created on first sign-in? | safe default | GitHub flow does; match it |
| What if Google returns no email? | safe default | Reject with the existing "email required" error |
| What does the button look like? | safe default | Existing provider button component |
| **An email that already has a password account?** | **material** | **nothing in the repository decides this** |

Eight rows resolved without a word to the developer. The GitHub flow answers
almost everything, because someone already made these decisions once.

## 2. Why the last one is material

Three defensible behaviors, and they produce different products:

```
link automatically      convenient; if Google's email is unverified or an
                        attacker controls it, it is account takeover
require confirmation    safe; adds an email round-trip to first sign-in
reject                  safest; users with an existing account hit a dead end
```

It is not reversible in the quiet way a default should be: whichever is chosen,
accounts get linked or not, and undoing that later is a data migration. And the
repository's GitHub flow does not settle it — that provider was added before the
password path existed.

## 3. Ask once, with options

```
Ready to implement — one decision I can't make from the repository:

Google sign-in with an email that already has a password account:

  [link automatically]   [require confirmation]   [reject]

Everything else follows the existing GitHub flow: same omniauth config,
same identities table, new user created on first sign-in, credentials in
Rails credentials.
```

What that message does *not* contain: a security essay, four questions, or a
request to design the answer. The options are concrete, the rest of the plan is
visible in three lines, and the answer is one word.

> **Developer:** require confirmation

## 4. Contract, now that it is decidable

Risk: **high** — authentication and account linking.

```yaml
objective: "Users can sign in with Google, with existing accounts linked only after confirmation"
risk: high
assumptions:
  - "Follows the existing GitHub omniauth flow — config/initializers/omniauth.rb"
  - "New user created on first sign-in, as GitHub does"
  - "Google account without a verified email is rejected"
requirements:
  - { id: OAUTH-001, priority: critical, description: "A new user can sign in with Google and gets an account", proof: { type: integration } }
  - { id: OAUTH-002, priority: critical, description: "A returning Google user signs into the same account", proof: { type: integration } }
  - { id: OAUTH-003, priority: critical, description: "Google email matching an existing password account triggers a confirmation email; no link happens yet", proof: { type: integration } }
  - { id: OAUTH-004, priority: critical, description: "Clicking the confirmation link links the identity; only then does Google sign-in reach that account", proof: { type: integration } }
  - { id: OAUTH-005, priority: critical, description: "An unconfirmed link attempt cannot access the existing account", proof: { type: security } }
  - { id: OAUTH-006, priority: critical, description: "A Google account with an unverified email is rejected", proof: { type: security } }
  - { id: OAUTH-007, priority: critical, description: "A tampered or replayed OAuth state parameter is rejected", proof: { type: security } }
  - { id: OAUTH-008, priority: high,     description: "Existing password sign-in is unchanged", proof: { type: regression } }
  - { id: OAUTH-009, priority: high,     description: "Existing GitHub sign-in is unchanged", proof: { type: regression } }
```

The chosen behavior became OAUTH-003 through OAUTH-005 — three requirements,
because "require confirmation" has a middle state that must not be exploitable.

## 5. Result

```
✓ VERIFIED

Sign in with Google

Requirements   9/9
Tests          38/38
Regression     password and GitHub sign-in unchanged
Changed        7 files

Linking behavior is as you chose: confirmation email, no access before it is
clicked.
```

---

## What this example demonstrates

- Nine questions, one asked. The ratio is the point — the other eight had
  answers sitting in the repository.
- The material question was identified by **reversibility and blast radius**,
  not by how uncertain it felt.
- It was asked *before* implementation, when the answer was still free. The same
  question after the code is written costs a rewrite.
- The answer expanded into three requirements, because the middle state of a
  confirmation flow is itself an attack surface.
- The final message confirms the chosen behavior in one line, so the developer
  can see their decision was honored without reading a diff.
