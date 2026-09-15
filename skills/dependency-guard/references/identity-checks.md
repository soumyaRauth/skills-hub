# Identity checks

Is the package you are about to install the one you mean? For a human typing a
familiar name this is a formality. For an agent, it is the check that matters
most. A model can produce a name that fits the request perfectly and belongs to
nobody, or to somebody who registered it after noticing models suggest it.

## The four ways a name goes wrong

| Failure | What it looks like | How to check |
| --- | --- | --- |
| **Unresolved** | The name does not exist in the registry | Resolve it (`ecosystem-commands.md`). No result means `DON'T ADD`. Do not substitute a similar name on your own |
| **Invented, then squatted** | The name resolves, but to a young package with a thin history, no repository or a mismatched one, and a name that reads like a description of the need | Read creation date, version count, repository URL, and whether the repository's own README names this package |
| **Typosquat** | One character from a popular name, a transposed pair, a separator swapped (`-` vs `_` vs none), or a plausible scope added | Compare against the package the ecosystem's own documentation names for this capability |
| **Dependency confusion** | The project uses a private registry or scope, and the same name exists publicly | Check the registry config (`.npmrc`, `pip.conf`, `uv.toml`, `settings.xml`); a private-scope name must resolve from the private registry |

## Signals, and what they are not

- **Repository match** is the strongest single signal. The registry entry
  points at a repository, and that repository's README or manifest names this
  exact package.
- **Age and history.** A package created recently with one version is not
  proof of anything. Weigh it against a name that should belong to something
  established.
- **Popularity** can be checked only from output actually read. A download count
  from memory is an invented number (rule 1).
- **A familiar-sounding name** is not evidence. It is the property squatting
  exploits.

## When identity cannot be checked

No network, a registry that needs credentials, a tool that is not installed:
the identity is `UNVERIFIED`, and the decision says so in its conditions:

```
DECISION    ADD WITH CONDITIONS
CONDITIONS  confirm `<name>` resolves to github.com/<expected-org>/<repo> before
            installing — the registry was not reachable from here
```

Never promote an unverified identity to `ADD` because the name looks right.

## What to say when a name is wrong

State what was asked for, what the registry returned, and what the ecosystem's
documentation names for this capability, if anything. Then stop. Picking a
different package yourself is a new dependency decision, and it goes through
the ladder again.
