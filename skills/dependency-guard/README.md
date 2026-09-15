# Dependency Guard

An Agent Skill that asks one question before a dependency comes in:

> **Should this dependency come in — and is it the one we think it is?**

```bash
npx skills add soumyaRauth/skills-hub --skill dependency-guard
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill dependency-guard --agent claude-code
```

---

## Why it exists

Most dependencies are never decided. A request's obvious implementation is
`npm install x`, and nobody reviews it again. Each one is lasting: code nobody
here wrote runs in the build, often at install time; its transitive tree grows
unreviewed; and a mistyped or invented name installs somebody else's package.

Coding agents make each of those more likely. They reach for a library by
reflex, and they sometimes name packages that do not exist — the gap a squatter
registers into.

## What it does

```
need → is it already here? (codebase · standard library · installed · a few lines)
     → is the package the one intended? (resolves · publisher · repository)
     → what comes with it? (install scripts · transitive growth · license)
     → is it maintained? (observed signals only)
     → USE EXISTING · ADD · ADD WITH CONDITIONS · DON'T ADD
```

```
DEPENDENCY  lodash — debounce for the customer search box
DECISION    USE EXISTING
WHY         The need is one function. src/lib/timing.js already holds throttle();
            a 9-line debounce beside it covers this without a new package.
```

Four worked examples: [a library for one function](examples/use-existing.md) ·
[a name that does not resolve](examples/unresolved-name.md) ·
[a major upgrade](examples/major-upgrade.md) ·
[the patch bump that gets no comment](examples/patch-bump.md)

## When it activates

It activates on its own when the work would add, replace, or major-upgrade a
dependency, or when someone asks which library to use. It stays quiet for
routine patch bumps that bring no new packages or install scripts, and for
removals. See [Activation](SKILL.md#activation).

## What it will not do

- **Invent registry facts.** Versions, downloads, maintainers, advisories and
  transitive counts come from output it actually read, or they are marked
  unverified.
- **Trust a name because it sounds right.** A name that does not resolve is
  `DON'T ADD`, and no similar name is substituted silently.
- **Install to try it.** Registry queries and dry runs only, until the decision.
- **Replace a scanner or a lawyer.** Audit output is evidence, and license
  combinations that might conflict go to a person.

Standards Compass audits dependency management across the whole project. This
skill decides one dependency at a time, as it arrives.

References: [`ecosystem-commands.md`](references/ecosystem-commands.md) ·
[`identity-checks.md`](references/identity-checks.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
