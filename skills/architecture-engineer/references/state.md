# State

## State

`.architecture/`, created only when there is something worth carrying between
sessions — and the reason this skill improves rather than restarts:

```
system.md        what this is, who it serves, the constraints that bind it
requirements.md  the architectural requirements, each typed and sourced
current.md       the architecture as implemented, from evidence
target.md        the architecture decided, and what must not be violated
decisions/       one ADR per decision, numbered
risks.md         architectural risks and the open questions blocking decisions
migration.md     the staged path, and which state it is actually in
```

Two files is a complete workspace for most sessions, and a first `DISCOVER`
often writes only `requirements.md`. Record facts, decisions and open questions
— never narration, never a transcript of the conversation. **The repository
outranks the file**: re-verify a recorded claim before building on it, and
correct it when it has gone stale. Never write a secret, a credential, or a
customer's data into it.
