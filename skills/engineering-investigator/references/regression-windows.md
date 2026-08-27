# Regression Windows

"It started on Tuesday" is the most useful sentence in a bug report and the most
frequently over-read. This is how to turn a time window into causal evidence
without skipping the step where you prove it.

## Establish the window independently

Fix the boundaries before looking for suspects, or the suspect will define the
window and then be convicted by it.

```
Last known good    a successful example, with its timestamp and source
First known bad    the earliest confirmed failure, with its source
Window             everything between — including the uncertainty
```

Sources for the boundaries, best first: an error rate or latency series; log
density before and after; a customer report with a timestamp; a support ticket;
"someone noticed on Tuesday" — which bounds *detection*, not onset. Detection
lag is normal and often long, so a window that starts at the report is an upper
bound, not the onset.

## Enumerate what changed inside it

```bash
git log --since="2026-08-24" --until="2026-08-26" --pretty=format:'%h %ad %an %s' --date=iso
git log --since="2026-08-24" --name-only --pretty=format:'--- %h %s'
git log --since="2026-08-24" -- package-lock.json yarn.lock composer.lock go.sum
git diff <last-good-tag>..<first-bad-tag> --stat
```

Code is only one category. Also enumerate: dependency and base-image upgrades,
migrations, configuration and environment changes, feature-flag flips,
infrastructure changes, scheduled jobs that first ran in the window, data volume
crossing a threshold, certificate or credential expiry, and third-party provider
changes and incidents.

A window with **no** change inside it is a strong result: it points at data
growth, external drift, or something environmental — and it eliminates a whole
class of hypotheses.

## Rank the candidates by mechanism, not by suspicion

For each candidate, ask whether a mechanism connects it to *this* symptom, with
*this* scope and *this* pattern:

```
Candidate            Touches the symptom's path?   Explains the scope?   Explains the timing?
a4f1c92 serializer   yes — checkout response       all tenants ✓         deployed 14:00 ✓
b7d2e10 admin CSS    no                            —                     —
lockfile bump        maybe — HTTP client version   all tenants ✓         same deploy ✓
```

A candidate that cannot explain the scope is unlikely to be the cause, however
suspicious the diff looks. Say so, and keep it low.

## Promoting correlation to cause

Timing alignment alone earns `LIKELY` at most, and only when the window is tight
and the mechanism is plausible. Promotion requires one of:

| Evidence | Gets you to |
| --- | --- |
| Reproduction on the new version and not on the old, same input | CONFIRMED |
| Deterministic metric differs across versions (query count, response shape, call count) | CONFIRMED, when it is the metric the symptom is made of |
| Revert or flag-off restores normal behavior | CONFIRMED |
| Trace attributes the added time or the error to code introduced in the change | HIGHLY LIKELY |
| The change is present in affected requests and absent in unaffected ones | HIGHLY LIKELY |
| Only timing alignment plus a plausible mechanism | LIKELY |

`git blame` locates the author of a line, not the cause of an incident. It is a
lead and a routing tool — see who to ask — never an argument.

## Deploy-shaped confounders

Rule these out by name before concluding that the *code* in a deploy was
responsible:

- **Restart effects.** A deploy empties caches and connection pools; the first
  minutes after any deploy are slower for reasons unrelated to the diff.
- **Cold caches at scale.** A cache key change invalidates everything at once —
  the symptom is real, the diff looks innocent.
- **Migration side effects.** A new index builds; a column rewrite locks; a
  backfill competes for IO.
- **Configuration drift.** Environment values differ from the previous release
  independently of the code.
- **Traffic coincidence.** Deploys cluster in business hours, and so do peaks.
- **Same-window infrastructure work.** Node replacement, scaling, or a network
  change that shares the window.

The discriminator for most of these is duration: restart effects decay in
minutes; a code regression persists.

## Works locally, fails in production

A frequent shape, and its own small investigation. The difference is always in
one of: data (volume, shape, legacy rows), configuration and environment
variables, concurrency, infrastructure between the client and the code (proxy,
edge, load balancer), external services in use (real versus stubbed), resource
limits, or build output (minification, tree-shaking, source maps, NODE_ENV).

Investigate it as a contrast: enumerate the differences, then find the cheapest
observation that tells you which one matters. Do not port production behavior
into a local guess — compare the two directly.

```bash
git diff --stat -- '*.env*' 'config/*' 'k8s/*' 'docker*' '*.yml'
```

## Recording history evidence

History is indirect evidence. Write it as such:

```
E9  FACT       a4f1c92 "Add gift-wrap options to cart serializer" deployed
               2026-08-25 14:00, inside the window [14:00, 14:31]
               source: git log, deploy log deploys/2026-08.log
E10 INFERENCE  a4f1c92 is the leading regression candidate — it is the only
               change in the window touching the checkout response path
               from: E9, E4
```

Never let an inference like E10 be reported as a cause. It is what the next
experiment is *for*.
