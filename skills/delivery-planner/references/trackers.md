# Trackers

## Contents

- Access order
- Statuses, across trackers
- Jira (Cloud; Data Center differences noted)
- Trello
- Nextcloud Deck
- GitHub Issues (and Projects)
- GitLab Issues
- Linear
- local
- Adding another tracker

For each supported tracker: how to reach it, the seven operations sync needs,
how statuses work, and what goes wrong. Every endpoint and command below was
checked against the official documentation cited next to it, **checked
2026-09-28**. Anything that could not be confirmed there is marked
**UNVERIFIED**; treat it as a hypothesis and read the tracker's response before
relying on it. APIs change: when a call returns 404, 410 or an unexpected shape,
re-read the cited page rather than guessing a fix.

Each tracker opens with **Connect**: the connection options best first (an
official MCP server with its own sign-in, where one exists), where the
credential is created, the least scope it needs, the env var names, and the
read-only calls `scripts/tracker.py` makes during setup. Show the human only
their tracker's Connect section.

The seven operations: **find** an item by its `[T-nnn]` marker · **create** ·
**update** title, text and labels · **move** between statuses · **comment** ·
**link** a PR · **list** everything on the board or project.

## Access order

For every tracker, the first that works:

1. **An MCP server for it, already installed in this session.** Use its tools;
   its own auth applies. Official servers are listed first below. A community
   server that is *not* already installed is a new dependency: it runs with your
   tracker credentials. Hand it to `dependency-guard` (identity, maintainer,
   install surface) and install it only on the human's yes.
2. **The official CLI**, when installed and logged in (`gh`, `glab`, `acli`).
3. **The REST (or GraphQL) API with `curl`**, credentials from the env vars named
   in `config.yml`, loaded from `auth_file` (`.delivery/.env`) when it is set.
4. **`local`**: files only, and say so.

Record the choice in `tracker.via` and name it whenever the tracker is touched.

### Handling credentials in commands

Load `.delivery/.env` inside the same command and pass secrets by reference, so
neither the chat nor a log sees them:

```bash
# Good: the file is sourced in this command; the transcript shows only names
set -a; . .delivery/.env; set +a; curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H 'Accept: application/json' "$DELIVERY_URL/rest/api/3/myself"
# Never: cat/grep/echo .delivery/.env or a token, set -x around such a command, or a token pasted inline
```

`scripts/tracker.py` lets an already-exported variable override the file.
Sourcing the file in a shell command does the opposite for that one command, so
when the human chose shell env vars (Connect option c) there is no `auth_file`
and nothing to source.

Check presence without printing: `[ -n "$JIRA_API_TOKEN" ] && echo set || echo missing`.

## Statuses, across trackers

| Tracker | What a status is | How a move is made | `blocked`, `dropped` when missing |
| --- | --- | --- | --- |
| Jira | Workflow status | A **transition**, looked up per issue | `Blocked` label + comment; `dropped` → a *Won't Do*-type status if the workflow has one, else done + `dropped` label |
| Trello | List | Change the card's `idList` | A `Blocked` list or label; `dropped` → archive (`closed=true`) + comment |
| Nextcloud Deck | Stack | `reorder` with a new `stackId` | A `Blocked` stack or label; `dropped` → archive + comment |
| GitHub | open/closed, plus a label or a Projects Status field | Labels, `state`, or the Projects field | Label `blocked`; `dropped` → closed as *not planned* |
| GitLab | open/closed, plus board-list labels | Swap labels; close/reopen | Label; `dropped` → close + `dropped` label |
| Linear | Workflow state (per team) | `issueUpdate` with `stateId` | A state if the team has one, else a label; `dropped` → a *Canceled*-type state if present |
| local | `status:` in the file | Edit the file | — |

Match the configured name to the tracker's own list **at the moment of the
move**, not an id cached at setup: columns get renamed.

---

## Jira (Cloud; Data Center differences noted)

### Connect (checked 2026-09-28)

**Option a, recommended on Cloud: Atlassian Rovo MCP server** (official, OAuth
2.1, no token stored). The agent runs:

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp
```

and the human runs `/mcp` in Claude Code, picks `atlassian` and signs in in the
browser (`claude mcp login atlassian` does the same from a shell). Cloud only.
— https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ ·
https://code.claude.com/docs/en/mcp

**Option b: API token (Cloud)** via `tracker.py secret jira`.

1. **Create it:** https://id.atlassian.com/manage-profile/security/api-tokens →
   *Create API token*. Tokens created since 15 Dec 2024 expire after one year
   by default (1–365 days). —
   https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
2. **Least access:** a classic (unscoped) token acts as the user, so the user
   needs, in the project: *Browse projects*, *Create issues*, *Edit issues*,
   *Transition issues*, *Add comments*. A token *with scopes* needs
   `read:jira-work` + `write:jira-work` (+ `read:jira-user` for the identity
   check), and calls a different base URL,
   `https://api.atlassian.com/ex/jira/{cloudId}`, which `tracker.py` does not
   build: use a classic token with the helper. That the scope picker shows
   exactly these names is **UNVERIFIED** (they are the OAuth scope names in the
   OpenAPI spec). — https://developer.atlassian.com/cloud/jira/platform/swagger-v3.v3.json
3. **Env vars:** `JIRA_EMAIL`, `JIRA_API_TOKEN`; site URL in `DELIVERY_URL`.

**Option b, Data Center: personal access token** via `tracker.py secret jira-dc`.

1. **Create it:** avatar → *Profile* → *Personal access tokens* → *Create
   token*; optional expiry. Jira 8.14 or later. —
   https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html
2. **Least access:** the token acts as the user: the same five project
   permissions as above.
3. **Env var:** `JIRA_PAT`; base URL in `DELIVERY_URL`.

**Option c:** `acli jira auth login --web` (Cloud), or the env vars already in
the shell.

**Setup calls** (`tracker.py`): identity `GET /rest/api/3/myself` (DC
`/rest/api/2/myself`, which returns `name`, not `accountId`); boards `GET
/rest/api/3/project/search` (DC `GET /rest/api/2/project`; that DC returns a
bare array is **UNVERIFIED**: the DC spec types the 200 response as a single
project); columns `GET
/rest/api/{3|2}/project/{key}/statuses`; create project `POST
/rest/api/{3|2}/project`, which needs the *Administer Jira* global permission
(`manage:jira-configuration`), so most users get `needs_jira_admin`. Statuses
are workflow configuration: `create-column` always refuses on Jira. —
https://developer.atlassian.com/cloud/jira/platform/swagger-v3.v3.json ·
https://docs.atlassian.com/software/jira/docs/api/REST/9.12.0/


**Base URL** Cloud `https://<site>.atlassian.net/rest/api/3/…` (v2 also
available at `/rest/api/2/…`) · Data Center `https://<host>/rest/api/2/…`.

**Auth**
- Cloud: `Authorization: Basic base64(<email>:<api token>)`, e.g. `curl -u
  "$JIRA_EMAIL:$JIRA_API_TOKEN"`. Passwords are deprecated for this. —
  https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
- Data Center: personal access token, `Authorization: Bearer <token>`
  (`$JIRA_PAT`). —
  https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html

**Operations** (Cloud v3 unless noted; source: the official OpenAPI spec,
https://developer.atlassian.com/cloud/jira/platform/swagger-v3.v3.json, and the
v2 spec https://developer.atlassian.com/cloud/jira/platform/swagger.v3.json)

| Operation | Cloud | Data Center |
| --- | --- | --- |
| Find | `GET /rest/api/3/search/jql?jql=project=PROJ AND labels="T-004"&fields=summary,status,labels,updated` | `GET /rest/api/2/search?jql=…` |
| Create | `POST /rest/api/3/issue` `{"fields":{"project":{"key":"PROJ"},"summary":"[T-004] …","issuetype":{"name":"Task"},"labels":["T-004"],"description":<ADF>}}` | `POST /rest/api/2/issue`, `description` a plain string |
| Update | `PUT /rest/api/3/issue/{key}` `{"fields":{…}}` (a status change here is ignored) | `PUT /rest/api/2/issue/{key}` |
| Move | `GET /rest/api/3/issue/{key}/transitions`, pick the one whose target status name equals the `status_map` value, then `POST` the same path `{"transition":{"id":"<id>"}}` | same, under `/rest/api/2/` |
| Comment | `POST /rest/api/3/issue/{key}/comment`, body in **ADF** | `POST /rest/api/2/issue/{key}/comment` `{"body":"plain text"}` |
| Link a PR | `POST /rest/api/3/issue/{key}/remotelink` `{"object":{"url":"<pr url>","title":"PR #31"}}` | `/rest/api/2/issue/{key}/remotelink` (**UNVERIFIED** on DC: path taken to mirror Cloud) |
| List | `search/jql` with `jql=project=PROJ AND labels in (…)` or `summary ~ "T"` then filter, paging with `nextPageToken` | `search` with `startAt` |

DC paths: https://developer.atlassian.com/server/jira/platform/rest/v11001/api-group-search/
and https://developer.atlassian.com/server/jira/platform/rest/v11001/api-group-issue/.

Minimal ADF body for a v3 comment or description:

```json
{"body":{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"[delivery-planner] T-004 → In Review · PR https://…/pull/31"}]}]}}
```

**Gotchas**
- **Transitions are per issue and per workflow.** The list returned is what is
  possible *from the issue's current status*; an impossible move returns an
  empty list, not an error. Always look up by the target status name, never
  reuse a transition id from another issue or project. If no transition leads
  to the mapped status, stop and report the path (e.g. *To Do → In Review needs
  In Progress first*), and move one step at a time only if each step is itself
  a mapped status.
- **Old search is gone.** `GET/POST /rest/api/3/search` is marked deprecated,
  "currently being removed" (changelog CHANGE-2046). Use `/rest/api/3/search/jql`:
  it returns only ids unless `fields=` is given, pages with `nextPageToken`,
  rejects unbounded JQL (add `project = …`), and is eventually consistent (pass
  `reconcileIssues` for read-after-write). The exact removal date could not be
  read from the changelog page: **UNVERIFIED**.
- **Brackets and hyphens are not searchable text.** `+ - & | ! ( ) { } [ ] ^ ~ *
  ? \ :` are not indexed, so `summary ~ "[T-004]"` matches loosely. Put the id
  in a **label** (`T-004`) and search `labels = "T-004"`; then confirm the
  title prefix exactly. Labels cannot contain spaces. —
  https://confluence.atlassian.com/jirasoftwareserver/search-syntax-for-text-fields-939938747.html
  (DC page; the Cloud page confirms the phrase syntax but does not list the
  characters: https://support.atlassian.com/jira-software-cloud/docs/search-for-work-items-using-the-text-field/) ·
  labels: https://support.atlassian.com/automation/kb/automation-for-jira-fails-to-copy-components-list-to-label-with-error/
- **v3 needs ADF; v2 takes plain text.** A plain string sent as a v3 comment or
  description is rejected. When writing plain text is simpler, Cloud's v2
  endpoints accept it.
- **Development panel.** With the GitHub for Jira app, the issue key in the
  branch name, commit message and PR title links them automatically: name
  branches `PROJ-17-reset-password`. —
  https://support.atlassian.com/jira-cloud-administration/docs/integrate-with-github/
- **Rate limits.** `429` with `Retry-After` (seconds). Wait that long; do not
  loop. — https://developer.atlassian.com/cloud/jira/platform/rate-limiting/

**Official CLI: Atlassian CLI (`acli`)** — Cloud.
https://developer.atlassian.com/cloud/acli/reference/commands/jira-workitem/

| Operation | Command |
| --- | --- |
| Login | `acli jira auth login --web`, or `--site <site>.atlassian.net --email "$JIRA_EMAIL" --token < <(printf %s "$JIRA_API_TOKEN")` |
| Find / list | `acli jira workitem search --jql 'project = PROJ AND labels = "T-004"' --json` |
| Create | `acli jira workitem create --project PROJ --type Task --summary "[T-004] …" --label T-004 --description-file body.txt` |
| Update | `acli jira workitem edit --key PROJ-17 --summary "…" --labels …` |
| Move | `acli jira workitem transition --key PROJ-17 --status "In Review" --yes` (by status name) |
| Comment | `acli jira workitem comment create --key PROJ-17 --body "…"` (the reference's examples omit `create`; the synopsis includes it) |

Whether `acli` works against Data Center: **UNVERIFIED** (its docs are Cloud
only). For DC use REST.

**MCP servers**
- Official: **Atlassian Rovo MCP Server**, remote, `https://mcp.atlassian.com/v2/mcp`,
  OAuth 2.1 (an API token for headless use if an org admin allows it); v1 is
  deprecated. Cloud only as documented; nothing says it serves Data Center. —
  https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ ·
  https://developer.atlassian.com/cloud/rovo-mcp/guides/getting-started/
- Community: `sooperset/mcp-atlassian` ("not an official Atlassian product");
  supports Cloud and Server/Data Center 8.14+. The only MCP route for DC found.
  Trust decision required. — https://github.com/sooperset/mcp-atlassian

---

## Trello

### Connect (checked 2026-09-28)

**Option a: Trello's official MCP server**, `https://mcp.trello.com/v1`, OAuth
2.0 with a consent screen (one workspace per connection). Atlassian's page gives
no Claude Code command; by Claude Code's documented syntax it would be
`claude mcp add --transport http trello https://mcp.trello.com/v1`, then `/mcp`
to sign in (**UNVERIFIED** as a Trello-documented command). Comments and
attachments were still *planned* there, so sync falls back to REST for those,
which needs option b anyway. —
https://support.atlassian.com/trello/docs/connect-trello-to-ai-assistants-with-trello-mcp/

**Option b: API key + token** via `tracker.py secret trello` (default).

1. **Create them:** https://trello.com/apps/admin → your Power-Up (create one if
   there is none) → *Trello Auth* tab → *Generate a new API key*; then the
   *Token* link next to the key, which authorizes the token. —
   https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/
2. **Least access:** scope `read,write` (not `account`); expiration `never`,
   `30days`, `1day` or `1hour`. Authorize URL shape:
   `https://trello.com/1/authorize?expiration=30days&scope=read,write&response_type=token&key=<key>`. —
   https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/
3. **Env vars:** `TRELLO_API_KEY`, `TRELLO_TOKEN`.

**Setup calls:** identity `GET /1/members/me`; boards `GET
/1/members/me/boards?filter=open`; columns `GET /1/boards/{id}/lists`; create
board `POST /1/boards/?name=…` (`defaultLists` defaults to true: *To Do*,
*Doing*, *Done*); create list `POST /1/lists?name=…&idBoard=…`. —
https://developer.atlassian.com/cloud/trello/swagger.v3.json


**Base URL** `https://api.trello.com/1/…`

**Auth** API key and token, either as query parameters `key=$TRELLO_API_KEY&token=$TRELLO_TOKEN`
or the header `Authorization: OAuth oauth_consumer_key="<key>", oauth_token="<token>"`.
Prefer the header: query strings end up in logs. —
https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/

**Operations** — https://developer.atlassian.com/cloud/trello/rest/api-group-cards/ ·
https://developer.atlassian.com/cloud/trello/rest/api-group-boards/ ·
https://developer.atlassian.com/cloud/trello/rest/api-group-search/

| Operation | Call |
| --- | --- |
| List columns | `GET /1/boards/{boardId}/lists` |
| List / find | `GET /1/boards/{boardId}/cards` (open cards), match the `[T-004]` prefix on `name` locally. Archived cards: `GET /1/boards/{boardId}/cards/closed` (**UNVERIFIED** path; check the boards reference) |
| Create | `POST /1/cards` with `idList` (required), `name="[T-004] …"`, `desc` |
| Update | `PUT /1/cards/{cardId}` with `name`, `desc` |
| Move | `PUT /1/cards/{cardId}` with `idList=<target list id>` |
| Comment | `POST /1/cards/{cardId}/actions/comments` with `text` |
| Link a PR | `POST /1/cards/{cardId}/attachments` with `url` |
| Label | `POST /1/cards/{cardId}/idLabels` with `value=<labelId>`; a board label is created with `POST /1/boards/{boardId}/labels` (`name`, `color`) only on a yes |

**Gotchas**
- **A move is a field change**, `idList`. Look the list id up by name from
  `/boards/{id}/lists` at move time.
- **Archive, never delete.** `DELETE /1/cards/{id}` exists; never call it.
  `dropped` is `closed=true` on the card plus a comment. (That `closed` archives
  is standard Trello behavior; the reference lists the field without describing
  it.)
- **Search is not an idempotency check.** `GET /1/search` exists, but how it
  tokenizes `[T-004]` is not documented (**UNVERIFIED**). List the board's cards
  and match the prefix exactly.
- **Rate limits:** 100 requests per 10 s per token, 300 per 10 s per key; a
  `429` names which. Batch reads (one `/boards/{id}/cards` rather than one call
  per card). — https://developer.atlassian.com/cloud/trello/guides/rest-api/rate-limits/

**Official CLI:** none found from Atlassian (**UNVERIFIED** that none exists);
use REST.

**MCP servers**
- Official: **Trello MCP server**, `https://mcp.trello.com/v1`, OAuth 2.0.
  Reads and writes boards, lists and cards, searches, archives. Comments,
  attachments and custom fields were listed as *planned*, not available, when
  checked: fall back to REST for those two operations. —
  https://support.atlassian.com/trello/docs/connect-trello-to-ai-assistants-with-trello-mcp/
- The Rovo MCP server does not list Trello. —
  https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/
- Community (not verified beyond search results; trust decision required):
  `delorenj/mcp-server-trello` and others.

---

## Nextcloud Deck

### Connect (checked 2026-09-28)

**Option a:** Nextcloud's Context Agent MCP server exists but needs the
AppAPI/ExApp stack on the server; offer it only if the admin already runs it
(see *MCP servers* below). No `claude mcp add` recipe is documented for it.

**Option b: app password** via `tracker.py secret deck` (default).

1. **Create it:** Nextcloud → *Personal settings* → *Security* → *Devices &
   sessions*: enter an app name at the bottom and create the device-specific
   password; it is shown once. Required when two-factor auth is on. (The exact
   button label is **UNVERIFIED**.) —
   https://docs.nextcloud.com/server/stable/user_manual/en/session_management.html
2. **Least access:** an app password acts as the user; the user needs edit
   rights on the board (or to be its owner to add stacks).
3. **Env vars:** `NEXTCLOUD_USER`, `NEXTCLOUD_APP_PASSWORD`; server URL in
   `DELIVERY_URL`.

**Setup calls:** identity `GET /ocs/v2.php/cloud/user` with `OCS-APIRequest:
true` and `Accept: application/json` (returns `ocs.data.id`, `displayname`;
from the provisioning API's OpenAPI file,
https://raw.githubusercontent.com/nextcloud/server/master/apps/provisioning_api/openapi.json;
not on docs.nextcloud.com, where JSON via `Accept` is documented:
https://docs.nextcloud.com/server/latest/developer_manual/client_apis/OCS/ocs-api-overview.html);
boards `GET /boards`; columns `GET /boards/{id}/stacks`; create board `POST
/boards` `{"title","color":"0082c9"}` (hex without `#`); create stack `POST /boards/{id}/stacks`
`{"title","order"}`. — https://deck.readthedocs.io/en/latest/API/


**Base URL** `https://<nextcloud>/index.php/apps/deck/api/v1.0/…` (v1.1 exists
from Deck 1.3.0 and differs only in attachments). Comments use the **OCS** base
`https://<nextcloud>/ocs/v2.php/apps/deck/api/v1.0/…`.

**Auth and headers** — every request:

```
OCS-APIRequest: true
Content-Type: application/json
Authorization: Basic base64(<user>:<app password>)     # curl -u "$NEXTCLOUD_USER:$NEXTCLOUD_APP_PASSWORD"
```

Use an **app password** (Settings → Security → Devices & sessions), never the
account password; it is mandatory when two-factor auth is on, and can be
revoked on its own. —
https://docs.nextcloud.com/server/latest/user_manual/en/session_management.html

**Operations** — https://deck.readthedocs.io/en/latest/API/ and
https://raw.githubusercontent.com/nextcloud/deck/main/docs/API.md

| Operation | Call |
| --- | --- |
| List boards | `GET /boards` |
| List / find | `GET /boards/{boardId}/stacks`: each stack carries its `cards`; match the `[T-004]` prefix on `title` |
| Create | `POST /boards/{b}/stacks/{s}/cards` `{"title":"[T-004] …","type":"plain","order":999,"description":"…"}` |
| Update | `PUT /boards/{b}/stacks/{s}/cards/{c}` with the **full** card: `title`, `type`, `owner` are required, and `order`/`description` reset to defaults if left out |
| Move | `PUT /boards/{b}/stacks/{s}/cards/{c}/reorder` `{"stackId":<target>,"order":0}` |
| Comment | `POST /ocs/v2.php/apps/deck/api/v1.0/cards/{cardId}/comments` `{"message":"…"}` (max 1000 characters) |
| Link a PR | No link field: put the URL in the comment (and optionally the description) |
| Label | `PUT /boards/{b}/stacks/{s}/cards/{c}/assignLabel` `{"labelId":<id>}` |
| Archive | `PUT /boards/{b}/stacks/{s}/cards/{c}/archive` |

**Gotchas**
- **Forgetting `OCS-APIRequest: true`** makes Nextcloud treat the call as a
  browser request; send it on every call, REST and OCS alike.
- **PUT replaces.** Read the card first and send every field back, or its
  description and position are lost (from the controller's signature:
  https://raw.githubusercontent.com/nextcloud/deck/main/lib/Controller/CardApiController.php).
- **Moves are `reorder`**, not a field on the update.
- **Comments are OCS, not REST**, and cap at 1000 characters.
- **`DELETE …/cards/{c}` exists; never call it.** `dropped` is archive + comment.
- **ETags.** Board, stack and card responses carry `ETag`; `If-None-Match`
  returns `304` when nothing changed, which makes the pull before each write
  cheap. The Deck version that introduced this is **UNVERIFIED**.

**Official CLI:** none found (**UNVERIFIED** that none exists); use REST.

**MCP servers**
- Official: Nextcloud's **Context Agent** app exposes an MCP server at
  `/index.php/apps/app_api/proxy/context_agent/mcp/` (`Authorization: Bearer
  <app password>`), with Deck tools. It needs the AppAPI/ExApp stack on the
  server, which many instances do not have. —
  https://docs.nextcloud.com/server/stable/admin_manual/ai/app_context_agent.html
- Community: `cbcoutinho/nextcloud-mcp-server` (AGPL-3.0, Deck tools). Trust
  decision required. — https://github.com/cbcoutinho/nextcloud-mcp-server

---

## GitHub Issues (and Projects)

### Connect (checked 2026-09-28)

**Option a, recommended: `gh auth login`.** GitHub CLI's own browser sign-in; no
token file. Default scopes are `repo`, `read:org`, `gist`; a Projects board
also needs `gh auth refresh -s project`. The agent then uses `gh`, and runs the
setup calls through `gh api`. —
https://cli.github.com/manual/gh_auth_login · https://cli.github.com/manual/gh_project

**The official GitHub MCP server is not a no-token option.** Its remote install
for Claude Code sends a PAT header:
`claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GH_TOKEN"`
(the repo's guide shows the same with `claude mcp add-json`). Offer it only when
the human prefers MCP and already has the token. —
https://code.claude.com/docs/en/mcp ·
https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md

**Option b: fine-grained personal access token** via `tracker.py secret github`.

1. **Create it:** https://github.com/settings/personal-access-tokens/new
   (Settings → Developer settings → Personal access tokens → Fine-grained
   tokens). —
   https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
2. **Least access:** *Repository access* → only this repository;
   *Repository permissions* → *Issues: Read and write* (covers issues, comments
   and labels). *Metadata: Read* is listed as required; that it is added
   automatically is **UNVERIFIED**. Fine-grained tokens **cannot** reach a
   Projects board owned by a user account; an organization's board needs the
   organization permission *Projects*. For a personal board use option a. —
   https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens
3. **Env var:** `GH_TOKEN` (the name `gh` itself reads).

**Setup calls:** identity `GET /user`; boards `GET /user/repos` plus GraphQL
`viewer { projectsV2 }`; columns: repo labels `GET /repos/{o}/{r}/labels`, or a
project's *Status* options via GraphQL; create board: a Projects board via
GraphQL `createProjectV2(input: {ownerId, title})` at `POST /graphql` (that exact
endpoint path was not quoted on a fetched page: **UNVERIFIED**) (`gh project create --owner @me --title …`); create column: a
label `POST /repos/{o}/{r}/labels`. New repositories are out of scope. —
https://docs.github.com/en/rest/users/users · https://cli.github.com/manual/gh_project_create


**Base URL** `https://api.github.com` (GitHub Enterprise Server: its own host).

**Auth** `Authorization: Bearer $GH_TOKEN`, `Accept: application/vnd.github+json`,
`X-GitHub-Api-Version: 2022-11-28` (still supported, and the default when the
header is omitted; newer versions exist). —
https://docs.github.com/en/rest/about-the-rest-api/api-versions

**Operations** — CLI: https://cli.github.com/manual/gh_issue_create ·
[edit](https://cli.github.com/manual/gh_issue_edit) ·
[close](https://cli.github.com/manual/gh_issue_close) ·
[comment](https://cli.github.com/manual/gh_issue_comment) ·
[list](https://cli.github.com/manual/gh_issue_list) ·
[reopen](https://cli.github.com/manual/gh_issue_reopen). REST:
https://docs.github.com/en/rest/issues/issues ·
https://docs.github.com/en/rest/issues/comments

| Operation | `gh` | REST |
| --- | --- | --- |
| Find / list | `gh issue list --state all --search '"[T-004]" in:title' --json number,title,labels,state,updatedAt`, then match the prefix exactly | `GET /repos/{o}/{r}/issues?state=all` (paged), or `GET /search/issues?q=repo:o/r is:issue in:title "T-004"` |
| Create | `gh issue create --title "[T-004] …" --body-file body.md --label T-004` | `POST /repos/{o}/{r}/issues` |
| Update | `gh issue edit 42 --title "…" --add-label status:in-review --remove-label status:in-progress` | `PATCH /repos/{o}/{r}/issues/42` |
| Move | labels as above; `done` → `gh issue close 42 --reason completed`; `dropped` → `--reason "not planned"`; back from closed → `gh issue reopen 42` | `PATCH` with `state` and `state_reason` (`completed`, `not_planned`, `duplicate`, `reopened`) |
| Comment | `gh issue comment 42 --body "…"` | `POST /repos/{o}/{r}/issues/42/comments` `{"body":"…"}` |
| Link a PR | `Closes #42` in the PR description | same |

**Projects (v2) as the board.** When `tracker.github_project` is set, the
column is the project's single-select **Status** field. `gh project field-list`
gives the field and option ids; `gh project item-add` adds the issue;
`gh project item-edit --id <item> --project-id <p> --field-id <f>
--single-select-option-id <opt>` moves it (one field per call). GraphQL:
`updateProjectV2ItemFieldValue`. The token needs the `project` scope
(`gh auth refresh -s project`). —
https://cli.github.com/manual/gh_project ·
https://cli.github.com/manual/gh_project_item-edit ·
https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects

**Gotchas**
- **Closing keywords only fire when the PR targets the default branch.** `Closes
  #42` on a PR into `develop` does nothing. Do not rely on it for `done`: the
  planner closes the issue itself after `VERIFIED` + merge. —
  https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
- **Auto-close is not proof.** When GitHub closed an issue on merge but
  ProofBuild never reported `VERIFIED`, do not reopen it on your own: keep the
  local ticket `in_review`, comment that proof is missing, and ask the human.
  Never fight the tracker in a loop.
- **Search has its own rate limit** (30 requests/min authenticated). Prefer
  listing. — https://docs.github.com/en/rest/search/search
- **Labels are silently dropped** on create when the token lacks push access.
  Read back. — https://docs.github.com/en/rest/issues/issues
- **Pull requests are issues** to the list endpoint: filter out items with a
  `pull_request` key.

**MCP servers**
- Official: **GitHub MCP Server**, remote `https://api.githubcopilot.com/mcp/`.
  The `issues` toolset is on by default; `projects` must be enabled
  (`--toolsets` / `GITHUB_TOOLSETS`). — https://github.com/github/github-mcp-server

---

## GitLab Issues

### Connect (checked 2026-09-28)

**Option a:** the official GitLab MCP server (beta, OAuth 2.0 dynamic client
registration) must first be enabled by an admin. Where it is:
`claude mcp add --transport http gitlab https://<gitlab>/api/v4/mcp`, then `/mcp`
(the command follows Claude Code's syntax; that GitLab documents this exact
line is **UNVERIFIED**). —
https://docs.gitlab.com/user/model_context_protocol/mcp_server/

**Option c, usually simplest: `glab auth login`**, interactive, detects the
instance from the git remote. — https://docs.gitlab.com/cli/auth/login/

**Option b: personal access token** via `tracker.py secret gitlab`.

1. **Create it:** avatar → *Edit profile* → *Access* → *Personal access
   tokens* → *Generate token* (choose the legacy, scoped token). On gitlab.com
   the page is `/-/user_settings/personal_access_tokens` (path **UNVERIFIED**). —
   https://docs.gitlab.com/user/profile/personal_access_tokens/
2. **Least access:** scope `api`. `read_api` cannot create, move or comment. —
   https://docs.gitlab.com/security/tokens/access_token_scopes/
3. **Env var:** `GITLAB_TOKEN`; self-hosted URL in `DELIVERY_URL`.

**Setup calls:** identity `GET /api/v4/user`; boards `GET
/api/v4/projects?membership=true&simple=true`; columns: the project's labels
`GET /projects/:id/labels` (board lists are labels; `GET /projects/:id/boards`
shows which); create project `POST /projects` with `name` (required unless `path` is
given); create column: a label `POST /projects/:id/labels` with `name` and
`color` (both required; `#RRGGBB`). — https://docs.gitlab.com/api/users/ ·
https://docs.gitlab.com/api/boards/ · https://docs.gitlab.com/api/projects/ ·
https://docs.gitlab.com/api/labels/


**Base URL** `https://gitlab.com/api/v4` or the self-hosted host. `:id` is the
numeric project id or the URL-encoded path (`shop%2Fstorefront`); `:issue_iid`
is the number shown in the UI.

**Auth** `PRIVATE-TOKEN: $GITLAB_TOKEN` (or `Authorization: Bearer`). —
https://docs.gitlab.com/api/rest/authentication/

**Operations** — REST: https://docs.gitlab.com/api/issues/ ·
https://docs.gitlab.com/api/notes/ · CLI: https://docs.gitlab.com/cli/issue/create/ ·
[update](https://docs.gitlab.com/cli/issue/update/) ·
[close](https://docs.gitlab.com/cli/issue/close/) ·
[note](https://docs.gitlab.com/cli/issue/note/) ·
[list](https://docs.gitlab.com/cli/issue/list/)

| Operation | `glab` | REST |
| --- | --- | --- |
| Find / list | `glab issue list --all --search "T-004" --in title -O json`, then match the prefix | `GET /projects/:id/issues?state=all&search=T-004&in=title` |
| Create | `glab issue create -t "[T-004] …" -d "…" -l T-004` | `POST /projects/:id/issues` (`title`, `description`, `labels`) |
| Update | `glab issue update 57 --label status::in-review --unlabel status::in-progress` | `PUT /projects/:id/issues/:iid` (`title`, `description`, `add_labels`, `remove_labels`) |
| Move | swap the board-list labels; `done`/`dropped` → `glab issue close 57`; back → `glab issue reopen 57` | `PUT` with `state_event=close` / `reopen` |
| Comment | `glab issue note 57 -m "…"` | `POST /projects/:id/issues/:iid/notes` `{"body":"…"}` |
| Link a MR | `Closes #57` in the merge request description | same |

**Gotchas**
- **Board columns are labels.** A label list moves a card by removing the old
  label and adding the new one (Free tier). Scoped labels (`status::review`),
  which replace their siblings automatically, are Premium/Ultimate; on Free use
  plain labels and remove the old one yourself. Status-based lists (native
  work-item Status) are Premium, from GitLab 18.2. —
  https://docs.gitlab.com/user/project/issue_board/ ·
  https://docs.gitlab.com/user/project/labels/

**MCP servers**
- Official: **GitLab MCP server**, beta, `https://<gitlab>/api/v4/mcp`, OAuth 2.0
  dynamic client registration, enabled by an admin. Tools include
  `save_work_item`, `get_work_item`, `list_work_items`, `save_note`, `search`.
  No dedicated close tool was listed; closing presumably goes through
  `save_work_item` (**UNVERIFIED**; fall back to `glab` or REST). —
  https://docs.gitlab.com/user/model_context_protocol/mcp_server/ ·
  https://docs.gitlab.com/user/model_context_protocol/mcp_server_tools/

---

## Linear

### Connect (checked 2026-09-28)

**Option a, recommended: Linear's official MCP server** (OAuth 2.1, no token
stored). The agent runs:

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

then the human runs `/mcp` and signs in. — https://linear.app/docs/mcp

**Option b: personal API key** via `tracker.py secret linear`.

1. **Create it:** https://linear.app/settings/account/security → *Personal API
   keys*. Workspace admins decide whether members may create keys. —
   https://linear.app/developers/graphql
2. **Least access:** a key can be limited to *Read* + *Write* (or *Create
   issues* + *Create comments*) and to specific teams: limit it to this team.
   — https://linear.app/docs/api-and-webhooks
3. **Env var:** `LINEAR_API_KEY`.

**Setup calls:** identity `viewer { id name email }`; boards `teams { nodes { id
key name } }`; columns `workflowStates(filter: {team: …})`; create board
`teamCreate(input: {name})` (only `name` required); create column
`workflowStateCreate(input: {teamId, name, type, color})`, all four required,
`type` one of `backlog`, `unstarted`, `started`, `completed`, `canceled`. —
https://raw.githubusercontent.com/linear/linear/master/packages/sdk/src/schema.graphql.
Which roles may create teams or states is **UNVERIFIED**; a refusal comes back
as `forbidden`. Errors arrive in `errors[]`, sometimes with HTTP 400; rate
limiting is `extensions.code: RATELIMITED` (https://linear.app/developers/rate-limiting).
How an auth failure is reported is not in the docs (**UNVERIFIED**); the
official SDK reads `extensions.type: "authentication error"`, which the helper
maps to `unauthorized`.


**Endpoint** `POST https://api.linear.app/graphql` (GraphQL only).

**Auth** personal API key: `Authorization: $LINEAR_API_KEY` (**no** `Bearer`);
OAuth token: `Authorization: Bearer <token>`. — https://linear.app/developers/graphql

**Operations** — names checked in the official SDK schema,
https://raw.githubusercontent.com/linear/linear/master/packages/sdk/src/schema.graphql

| Operation | GraphQL |
| --- | --- |
| Statuses | `workflowStates(filter: {team: {key: {eq: "ENG"}}}) { nodes { id name type } }` |
| Find / list | `issues(filter: {team: {key: {eq: "ENG"}}, title: {contains: "[T-004]"}}) { nodes { id identifier title state { name } updatedAt } }`, then match the prefix |
| Create | `issueCreate(input: {teamId, title: "[T-004] …", description, stateId, labelIds})` |
| Update / move | `issueUpdate(id: "ENG-17", input: {title, description, stateId})` |
| Comment | `commentCreate(input: {issueId, body})` (Markdown) |
| Link a PR | `attachmentLinkURL(issueId: "ENG-17", url: "<pr url>", title: "PR #31")`; with Linear's GitHub integration, `attachmentLinkGitHubPR` also syncs PR status |

**Gotchas**
- **States belong to a team.** Look up `stateId` by name within the configured
  team at move time.
- **`searchIssues` is rate-limited** (30/min) and `issueSearch` is deprecated;
  prefer the `issues(filter:)` list above.
- The team-key filter shape above follows the schema's filter types; confirm
  against the schema if the API rejects it.

**Official CLI:** none found on Linear's site (**UNVERIFIED** that none exists).

**MCP servers**
- Official: **Linear MCP server**, `https://mcp.linear.app/mcp` (Streamable
  HTTP; `/sse` deprecated), OAuth 2.1 or an API key header. —
  https://linear.app/docs/mcp

---

## local

No tracker. `.delivery/tickets/` is the whole truth; `tracker_ref` stays
empty; sync is a no-op and says `tracker: local`. Everything else (planning,
fixed moments, *what's left?*) works the same. Switching to a real tracker later
is a first sync: every ticket goes through idempotent create.

---

## Adding another tracker

Before `config.yml` names it, write a section here with:

1. Base URL and auth header shape, from the vendor's docs, with the URL and
   `checked <date>`.
2. The seven operations, each with its exact endpoint or command.
3. What a status is (column, state, label) and how a move is made.
4. Whether its search can find `[T-004]` exactly; if not, how to list and match.
5. How to archive or close without deleting.
6. Rate limits and the error that signals them.
7. Official MCP server or CLI, if any; community servers marked as needing a
   trust decision.

Anything not confirmed in the docs is marked **UNVERIFIED**. Until the section
exists, the project runs as `local`.
