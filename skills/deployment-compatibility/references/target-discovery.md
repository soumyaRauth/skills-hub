# Target discovery

Establishing what the target environment actually is, at whatever access level
exists, without changing it and without filling gaps from imagination.

## Establish the tier before anything else

Do not ask the user which tier applies. Try the cheapest read and observe:

```bash
uname -srm                      # anything at all comes back → at least READ-ONLY
```

| Outcome | Tier |
| --- | --- |
| Commands run against the target | `READ-ONLY` until the user names what may change |
| No command channel, but a specification, provider page, compose file or the user's description exists | `DECLARED` |
| Neither | `NONE` |

`AUTHORIZED` is never inferred. It exists only when the user names what may
change, and it is a list — *you may install packages and restart the app
service* — not a blanket. Anything outside the list stays proposal-only.

Record the boundary in one block, and put it in the report header:

```
Tier        READ-ONLY
Available   SSH to app-01 as deploy; docker; systemctl status; read /etc/nginx
Not         the database host, the managed Redis instance, DNS, the provider console
```

An unavailable capability is a stated gap, never a silent one. Investigate what
is reachable, then ask for the minimum that closes the gap that matters.

## Order of inspection

Cheapest first, and each result narrows what is worth asking next. Stop when the
contract's open questions are answered — a full sweep of a server nobody asked
about is noise.

### 1. Identity and platform

```bash
cat /etc/os-release                 # distribution and version
uname -srm                          # kernel and architecture
nproc; free -h; df -h; swapon --show
```

Architecture matters more often than people expect: an image built for `amd64`
does not run on `arm64`, and the failure arrives as an exec-format error nobody
connects to the build host.

### 2. Runtimes and package managers

Ask only about the runtimes the contract names.

```bash
node --version; npm --version; pnpm --version; bun --version
python3 --version; pip --version
php --version; composer --version
java -version; go version; ruby --version; dotnet --info
```

A missing command is a fact worth recording. So is a version manager: a `node`
on the interactive `PATH` that a systemd unit will never see is a classic
false `FIT`, so check how the process will actually be started, not how your
shell resolves the binary.

### 3. Containers

```bash
docker version; docker compose version
docker ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}'
docker image ls; docker volume ls; docker network ls
docker inspect <name> --format '{{.HostConfig.RestartPolicy.Name}} {{.HostConfig.Memory}}'
```

Four things decide whether a container deployment survives contact with reality,
and all four are readable: the restart policy, the memory limit, which paths are
volumes rather than container filesystem, and whether the Docker socket is
mounted into anything.

Do not conclude that a project should be containerized because the host runs
Docker. The contract decides the deployment model, not the host's inventory.

### 4. Services

Only the ones the contract requires.

```bash
systemctl list-units --type=service --state=running
psql --version; mysql --version; redis-cli --version
systemctl status postgresql nginx redis-server --no-pager
crontab -l; systemctl list-timers --no-pager
```

For each required service, four separate facts — and they are genuinely
separate, which is why a single "Redis: yes" is not an answer:

```
INSTALLED    the binary or package exists
RUNNING      the service is up now
REACHABLE    the application can connect, with its own credentials
COMPATIBLE   the version satisfies what the project requires
```

Reachable is the one that gets skipped, and it is the one that fails at 3 AM. A
running PostgreSQL the application cannot authenticate against is not a `FIT`.

### 5. Ports and exposure

```bash
ss -tulpn                                   # what listens, and on which address
ufw status verbose; iptables -S; nft list ruleset
```

The bind address is the finding, not the port number. Record every listener as
one of:

```
PUBLIC        bound to 0.0.0.0 or a routable address, and no firewall blocks it
INTERNAL      reachable inside a private network only
LOOPBACK      127.0.0.1 only
CONTAINER     published to a container network, not to the host
UNKNOWN       cannot be determined from here — say what would determine it
```

`0.0.0.0:5432` with no firewall rule is a finding whatever else is true. Verify
the claim from the outside where you legitimately can; a firewall rule read from
inside the box is evidence of intent, not of reachability.

### 6. Reverse proxy and TLS

```bash
nginx -T 2>/dev/null | head -100            # effective config, includes resolved
caddy validate; apachectl -S
openssl s_client -connect <host>:443 -servername <host> </dev/null 2>/dev/null \
  | openssl x509 -noout -dates -subject
curl -sI http://<host>/                     # does plain HTTP redirect?
```

What matters for compatibility: which host names route where, whether the
upstream matches the port the application will actually listen on, the
certificate's expiry and the names it covers, whether renewal is automated
(a timer or cron entry that exists — not the assumption that one does), request
size limits against the project's upload limits, timeouts against its slowest
legitimate response, and websocket upgrade headers when the project needs them.

Derive proxy configuration from the application. A generic Nginx block copied in
is how upload limits and timeouts end up contradicting the app.

### 7. Pressure

```bash
uptime; vmstat 1 3; df -i           # load, memory behavior, inode exhaustion
journalctl -k --since -7d | grep -i 'out of memory'
```

An OOM kill in the kernel log is the most useful single line on a server that
has run something before. Inodes are worth one command: a disk with free bytes
and no free inodes fails in a way nobody guesses.

## Recording a target fact

Every one carries its grade and its date. Facts age, and a dated fact can be
re-verified instead of re-trusted.

```
T-04  MEASURED   node --version → v20.11.1                         2026-09-20
T-07  MEASURED   ss -tulpn → 0.0.0.0:5432 postgres                 2026-09-20
T-09  SUPPLIED   "the box has 8 GB" — user, in the request
T-11  INFERRED   uploads are on container filesystem — no volume in
                 docker inspect app.Mounts  (from T-10)
T-12  UNKNOWN    SMTP reachability from the host
                 would settle it: a connect test from the target to the relay
```

## When the tier is `NONE`

This is a supported outcome, not a failure. Do the project side in full — the
contract is derivable from the repository alone, and it is genuinely useful —
then stop honestly:

```
STATE   NOT ASSESSED

The deployment contract below is derived from the repository. Nothing about the
target environment was established, so no compatibility claim is made.

To assess it, the smallest useful set is:
  1. cat /etc/os-release; uname -srm; nproc; free -h; df -h
  2. node --version; psql --version; redis-cli --version
  3. ss -tulpn
```

Ask for the smallest set that answers the contract's open questions — not a
questionnaire. Three commands that resolve six rows beat twelve that resolve
seven.

A specification the user pastes moves the tier to `DECLARED`, and every fact
from it is `SUPPLIED`. That is genuinely useful and it is not a measurement:
under rule 3, a matrix that fits entirely on supplied facts produces
`READY WITH CONDITIONS`, with each supplied fact as a condition to confirm.

## Safety

Discovery is read-only. Every command in this file reads. Before running
anything not in it, classify it — `READ-ONLY`, `REVERSIBLE`, `HIGH IMPACT`,
`DESTRUCTIVE` — and run only the first without asking. See `remediation.md`.

Never print a secret you encounter while reading configuration. An environment
file, a connection string in a systemd unit, a password in a compose file: cite
the location, redact the value, and treat the exposure itself as the finding.
