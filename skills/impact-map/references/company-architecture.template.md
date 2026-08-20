# Company Architecture (template)

Copy this file to `company-architecture.md` in this directory and fill it in for
your codebase. Impact Map reads it during Phase 2 (repository reconnaissance),
where it overrides generic framework assumptions.

Keep it factual and short — it is context, not documentation. Do not commit it
to a public fork if it contains anything internal.

```markdown
# <Team> Architecture Notes

## Domain boundaries
- <module>: owns <entities>. Entry point: <path>.
- Cross-boundary calls go through <mechanism>; direct imports across boundaries
  are a defect worth flagging.

## Layer conventions
- HTTP:        <path>
- Application: <path>
- Domain:      <path>
- Persistence: <path>
- Async:       <path>

## Naming conventions
- Services: <pattern>          Repositories: <pattern>
- Events:   <pattern>          Jobs:         <pattern>

## Known shared modules
- <path> — used by <consumers>. Changes here are high-blast-radius by default.

## Integrations
- <system> — direction, transport, owning team, contract location.

## Data
- Migration tool and ordering rules.
- Tables that are replicated to the warehouse or read by other services.
- Anything with a hard backward-compatibility requirement.

## Business terminology
- <term> = <meaning in code>, stored as <column/enum>.

## Standing risks
- <area that has broken before, and why>
```

Rules of thumb: prefer facts an agent cannot infer from the tree; update it when
the architecture changes; leave it out entirely rather than let it go stale.
