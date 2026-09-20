# Example — no target, and the report that says so

The shortest example here, and the one that matters most. A capable agent asked
this question will produce a fluent, plausible, entirely invented answer.

---

**Request:**

> Will this run on a standard Ubuntu VPS?

---

## Phase 1 — Target and tier

There is no target. "A standard Ubuntu VPS" is a category, not an environment:
no version, no resources, no installed software, no provider, no access, and no
specification.

```
Tier        NONE
Available   the repository
Not         anything about a target environment
```

So the ceiling is `NOT ASSESSED`, and it is set before the project is read. The
project half is still worth doing in full — the contract is derivable from the
repository alone, it is genuinely useful, and it is what turns the follow-up
into three commands instead of a conversation.

## Phase 2 — The contract

```
RUNTIME    PHP >= 8.2            composer.json require.php
           Composer 2            composer.lock plugin-api-version 2.6
SERVICES   MySQL >= 8.0          config/database.php; utf8mb4_0900_ai_ci collation
                                 in database/migrations/2026_03_11_add_index.php
           Redis                 config/queue.php — the default connection
PROCESSES  web                   public/index.php
           queue worker          app/Jobs/, and queue.php default is redis
           scheduler             app/Console/Kernel.php — 3 scheduled commands
PORTS      80/443 via a web server; PHP-FPM socket   no application port binding
STORAGE    storage/app/public persists    app/Services/DocumentStore.php
           and a symlink into the web root is expected
DATABASE   11 pending migrations          database/migrations/
ENV        14 required, 5 optional        inventory in the detail below
EXTERNAL   SMTP · S3-compatible object storage · a payment provider webhook
           (inbound — the target must be reachable from outside)
EXTENSIONS pdo_mysql, mbstring, intl, gd, zip   composer.json require
RESOURCES  UNKNOWN                        nothing establishes a figure
```

Three of those are worth surfacing without any server knowledge at all, because
they are true of every target:

- The project needs **three** process types. A VPS does not supply a process
  manager for the worker and the scheduler by itself; something has to.
- `storage/app/public` must persist **and** be reachable through the web root by
  symlink, which constrains the deployment layout more than most people expect.
- The payment webhook requires the host to be reachable **from the internet**,
  which is a different requirement from the host reaching out, and it is the one
  people discover after go-live.

## The answer

```markdown
DEPLOYMENT COMPATIBILITY
────────────────────────────────────────
TARGET   none — "a standard Ubuntu VPS" names a category, not a host
PROJECT  Laravel · PHP 8.2 · MySQL 8 · Redis · web + worker + scheduler
STATE    ⬜ NOT ASSESSED

I can't answer this one yet. Nothing about a target environment has been
established, so any compatibility claim would be invented. What I can give you
is what the project requires — which is the half that does not need a server.

WHAT THIS PROJECT REQUIRES
· PHP >= 8.2 with pdo_mysql, mbstring, intl, gd, zip; Composer 2
· MySQL >= 8.0 — a migration uses a collation introduced in 8.0
· Redis — it is the default queue connection, not an optional cache
· Three process types: web, a queue worker, and a scheduler. The last two need
  a process manager and a cron entry; a plain VPS gives you neither
· storage/app/public must persist across deploys and be symlinked into the
  web root
· 11 pending migrations
· 14 required environment variables
· Outbound: SMTP, S3-compatible storage, a payment provider
· Inbound: the payment webhook needs this host reachable from the internet
· Memory and CPU: the repository does not establish a figure, and I will not
  estimate one

TO ASSESS THE FIT, three commands on the box:
  1. cat /etc/os-release; php -v; php -m | tr '\n' ' '; composer --version
  2. mysql --version; redis-cli --version; systemctl list-units --type=service --state=running
  3. ss -tulpn; df -h; free -h

Paste the output and I'll produce the matrix. Or if you have a provider
specification instead, that works too — I'll mark those facts as supplied
rather than measured, and the conditions will say which ones to confirm.
```

## What this run refused to do

- **It did not describe a typical Ubuntu VPS.** Ubuntu 24.04 ships PHP 8.3, so
  the runtime row would probably have fit — and "probably" is not a row. The
  moment that sentence is written, a reader has a compatibility claim about
  their server that nobody made.
- **It did not say "this should work fine on any modern VPS."** That is the
  fluent, helpful-sounding version of the same fabrication.
- **It did not pad the report** with generic deployment advice to compensate for
  having no target. The project contract is the deliverable available here, and
  it is a real one.
- **It did not ask twelve questions.** Three commands answer most of the matrix,
  and they were chosen for that rather than for completeness.
- **It did not round up to `READY WITH CONDITIONS`** by turning every unknown
  into a condition. Conditions attach to an assessment; there is no assessment
  here, and `NOT ASSESSED` is the accurate word.
