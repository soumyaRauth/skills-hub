# Read-only commands per ecosystem

Every command here reads. None installs, writes a manifest, or changes the
lockfile the project commits. Prefer the project's own package manager: a
`pnpm-lock.yaml` means pnpm, not npm.

When a command needs the network and the environment has none, the fact it would
have produced is `UNVERIFIED`. Never fill the gap from memory.

## JavaScript / TypeScript

| Question | Command |
| --- | --- |
| Does the name resolve, and what is it? | `npm view <name> name version repository.url license maintainers time.modified deprecated --json` |
| Install scripts? | `npm view <name>@<version> scripts --json`, then look for `preinstall`, `install`, `postinstall`, `prepare` |
| What would installing add? | `npm install <name> --dry-run --ignore-scripts` · `pnpm add <name> --lockfile-only` in a throwaway copy · `yarn add <name> --mode=update-lockfile` in a throwaway copy |
| Already installed, and why? | `npm ls <name>` · `npm explain <name>` · `pnpm why <name>` |
| Known advisories | See *Advisories before install* below. Never only after the install |
| Runtime floor | `npm view <name>@<version> engines --json`, set against `engines` / `.nvmrc` / the CI matrix |

A dry run that executes lifecycle scripts is not read-only. Keep `--ignore-scripts`.

### Advisories before install

1. **The package itself.** Use the exact version the range would resolve to
   (`npm view <name>@<range> version`):
   `curl -s -X POST https://registry.npmjs.org/-/npm/v1/security/advisories/bulk -H 'content-type: application/json' -d '{"<name>":["<version>"]}'`.
   An empty object means no advisories for that version.
2. **What it brings in.** Copy `package.json` and the lockfile to a throwaway
   directory, then run
   `npm install <name>@<range> --package-lock-only --ignore-scripts --no-audit && npm audit --json`.
   Nothing is installed into `node_modules`, and no scripts run.
3. **Subtract the baseline.** Run `npm audit --json` on the project's own
   lockfile. Only advisories that appear in step 2 and not here come from the
   new package.

pnpm and yarn projects use the same bulk query for step 1, and
`pnpm audit --json` / `yarn npm audit --json` on the throwaway copy for step 2.

## Python

| Question | Command |
| --- | --- |
| Does the name resolve? | `pip index versions <name>` · `curl -s https://pypi.org/pypi/<name>/json` (read `info.home_page`, `info.project_urls`, `info.license`, `info.requires_python`) |
| What would installing add? | `pip install <name> --dry-run --report - --quiet` |
| Already installed? | `pip show <name>` · `pipdeptree -p <name>` when present · `uv tree` / `poetry show --tree` |
| Build-time code | A source distribution with no wheel for the platform runs its build backend at install time. Check the files list on the JSON API for wheels |
| Known advisories | Before install: `pip-audit -r <(echo '<name>==<version>')`. Without pip-audit, `curl -s -X POST https://api.osv.dev/v1/query -d '{"package":{"name":"<name>","ecosystem":"PyPI"},"version":"<version>"}'` |

## Other ecosystems

| Ecosystem | Resolve and inspect | Dry run / tree |
| --- | --- | --- |
| Rust | `cargo search <name> --limit 1` · `cargo info <name>` | `cargo tree -i <name>` after adding in a scratch copy; `build.rs` is install-time code |
| Go | `go list -m -versions <module>` · `go list -m -json <module>@latest` | `go mod graph`; no install scripts, but `go generate` directives are worth a look |
| Ruby | `gem info -r <name>` · `gem specification -r <name>` | `bundle lock --update <name>` in a scratch copy; native extensions compile at install |
| Java / Kotlin | Maven Central search API for the group and artifact | `mvn dependency:tree` · `gradle dependencies` |
| GitHub Actions | The action's repository and the tag's commit: `git ls-remote https://github.com/<owner>/<repo> refs/tags/<tag>` | Pin by SHA when the workflow already does; the tag is a mutable pointer |
| Containers | `docker buildx imagetools inspect <image>:<tag>` for the digest | Pin `FROM` by digest when the project already does |

## Reading the lockfile diff

The diff after the install is the evidence for rule 5:

- **Count direct and transitive additions** from the diff, not from package
  documentation.
- **`resolved` URLs:** every one should be on the registry host the project
  uses. A tarball from an unexpected host is a stop.
- **Integrity:** `integrity` / `sha512` fields present for every new entry.
- **Duplicates:** a second major version of something already installed is
  growth nobody asked for, and it's worth a line.
