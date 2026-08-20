# Team Standards (template)

Copy this file to `team-standards.md` in this directory and fill it in. Production
Guard reads it during phase 2, where it overrides the generic defaults.

Keep it short and factual. Do not commit it to a public fork if it contains
anything internal.

```markdown
# <Team> Release Standards

## Commands
- Full test suite:    <command>   (~<duration>)
- Targeted tests:     <command>
- Type check:         <command>
- Lint:               <command>
- Build:              <command>
Never run: <commands that touch shared or production-like environments>

## Risk overrides
- Changes under <path> are always high risk because <reason>.
- Changes under <path> may be treated as low risk because <reason>.

## Blocking criteria (in addition to the defaults)
- <team-specific condition that must stop a release>

## Accepted risks
- <known issue the team has consciously accepted, so it is not re-reported>

## Environment
- Available in local validation: <databases, fakes, sandboxes>
- Not available: <external systems that must be reported UNVERIFIED>

## Conventions
- Authorization is enforced via <mechanism>.
- Tenant scoping is applied by <mechanism>.
- Audit records are written through <mechanism>.
- Idempotency keys are <how they work, or "not used">.
```
