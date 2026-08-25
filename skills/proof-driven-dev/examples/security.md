# Example — Security-sensitive change

For a permission change, the positive cases prove the feature exists. Only the
**negative** cases prove it is a boundary.

---

**Developer:**

> Let team admins export their team's members to CSV.

---

## 1. Investigate

```
Repository   Rails 7, RSpec, Pundit for authorization
Existing     ExportsController#create — org-wide export, admin-only
Policy       app/policies/export_policy.rb
Model        User belongs_to :team, Team belongs_to :organization
Roles        member · team_admin · org_admin
Test helper  spec/support/auth_helpers.rb — sign_in_as(user)
```

The multi-tenant shape (organization → team → user) makes the interesting
question not *can a team admin export?* but *whose members do they get?*

## 2. Contract

Risk: **high** — authorization boundary, personal data leaving the system.

```yaml
objective: "A team admin can export the members of their own team, and only those"
risk: high
requirements:
  # positive
  - { id: SEC-001, priority: critical, description: "A team admin can export their own team's members", proof: { type: integration } }
  - { id: SEC-002, priority: critical, description: "The CSV contains exactly that team's members — no more, no fewer", proof: { type: integration } }
  # negative — the actual security surface
  - { id: SEC-003, priority: critical, description: "An unauthenticated request is rejected (401)", proof: { type: security } }
  - { id: SEC-004, priority: critical, description: "A plain member of the team is rejected (403)", proof: { type: security } }
  - { id: SEC-005, priority: critical, description: "A team admin requesting ANOTHER team's export is rejected (403)", proof: { type: security } }
  - { id: SEC-006, priority: critical, description: "A team admin from another ORGANIZATION is rejected (404, not 403 — no existence disclosure)", proof: { type: security } }
  - { id: SEC-007, priority: critical, description: "A tampered team_id in the request body does not override the authorized team", proof: { type: security } }
  # data
  - { id: SEC-008, priority: critical, description: "The CSV excludes password digests, session tokens, and API keys", proof: { type: integration } }
  - { id: SEC-009, priority: high,     description: "The export is recorded in the audit log with actor, team, and row count", proof: { type: integration } }
  # regression
  - { id: SEC-010, priority: high,     description: "The existing org-wide export is unchanged for org admins", proof: { type: regression } }
```

Seven of the ten are negatives, boundaries, or regressions. That ratio is normal
for an authorization change and abnormal for a feature request as written.

## 3. Verify — and find the hole

```
Stage 2  bundle exec rspec spec/requests/team_exports_spec.rb
         9 examples, 8 passed, 1 failure

FAIL  SEC-007  "a tampered team_id does not override the authorized team"
      POST /teams/7/members/export  body: { team_id: 12 }
      expected  team 7's members
      received  team 12's members  (200, 34 rows)
```

```
Classification  IMPLEMENTATION_ERROR
Diagnosis       the controller authorizes params[:id] from the route but builds
                the query from export_params[:team_id] from the body
                (app/controllers/team_exports_controller.rb:14). Authorization
                and data selection use different inputs.
Fix             derive the team once, from the authorized record; ignore any
                team identifier in the body.
Attempt         1 of 2 (high risk)
```

This is the defect the positive cases could never have found. SEC-001 and
SEC-002 passed the entire time.

## 4. Re-verify

```
bundle exec rspec spec/requests/team_exports_spec.rb    9 examples, 0 failures
bundle exec rspec spec/policies/ spec/requests/exports_spec.rb   41 examples, 0 failures
```

```
SEC-008 evidence
  Command   rspec spec/requests/team_exports_spec.rb -e "excludes sensitive columns"
  Expected  CSV header excludes encrypted_password, session_token, api_key
  Actual    PASS — header: id,name,email,role,joined_at
  Level     A
```

## 5. What the developer sees

```
✓ VERIFIED

Team member CSV export

Requirements   10/10  (7 of them negative or boundary cases)
Tests          50/50
Regression     org-wide export unchanged
Changed        4 files

One thing worth knowing: the first implementation authorized the team from the
URL but selected rows from the request body — a tampered team_id returned
another team's members. Caught by SEC-007, fixed, re-verified.

The tested authorization properties hold. Ask for the evidence to see which
properties those are.
```

Note the last sentence. Not "the export is secure" — *the tested properties
hold*, with an invitation to see exactly which ones were tested. Everything
untested stays visibly untested.

---

## What this example demonstrates

- The negative cases outnumbered the positive ones, and the only defect lived
  entirely inside them.
- The tampering case (SEC-007) is the one a feature-shaped contract omits, and
  the one that mattered: **authorize and select from the same input**.
- SEC-006 distinguishes 403 from 404 — a boundary that leaks existence is still
  a leak.
- The status line reports the tested properties, never a security guarantee.
- The one narrative sentence in the response earns its place: a
  vulnerability was found and fixed, and the developer should know that even
  though the final state is green.
