#!/usr/bin/env python3
"""Tracker setup helper for the delivery-planner skill. Python 3 stdlib only.

Covers setup only: store a credential, prove it, list what it can see, and
create a board or column on an explicit yes. Ticket create/move/comment stay
with the agent (references/trackers.md).

    tracker.py secret <tracker>              interactive; run in your own terminal
    tracker.py whoami                        the authenticated identity
    tracker.py boards                        projects / boards / repos / teams
    tracker.py columns <board>               statuses / lists / stacks / states
    tracker.py create-board <name> [--key K] only where the API allows it
    tracker.py create-column <board> <name>  only where the API allows it

Trackers: jira, jira-dc, trello, deck, github, gitlab, linear.
Which tracker and site: --tracker/--url flags, else DELIVERY_TRACKER/DELIVERY_URL
(written into .delivery/.env by `secret`), else .delivery/config.yml.
Credentials: .delivery/.env, overridden by the environment. --api-base (or
DELIVERY_API_BASE) points every call at another root, e.g. a local mock.

Every result is one JSON object on stdout. No secret value is ever printed.
Exit 0 on success, 1 on a tracker or input error, 2 on a refusal.
"""
import argparse
import base64
import getpass
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ENV_FILE = os.path.join(".delivery", ".env")
CONFIG_FILE = os.path.join(".delivery", "config.yml")

# name -> (prompt, secret?, where it comes from). Facts cited in references/trackers.md.
CREDENTIALS = {
    "jira": {
        "where": "https://id.atlassian.com/manage-profile/security/api-tokens → Create API token",
        "scope": "a classic API token acts as you: you need Browse projects, Create, Edit and "
                 "Transition issues and Add comments in the project",
        "vars": [("JIRA_EMAIL", False, "Atlassian account email"),
                 ("JIRA_API_TOKEN", True, "API token")],
        "url": ("DELIVERY_URL", "Site URL, e.g. https://example.atlassian.net"),
    },
    "jira-dc": {
        "where": "Jira: your avatar → Profile → Personal Access Tokens → Create token",
        "scope": "the token acts as you: Browse projects, Create, Edit and Transition issues, "
                 "Add comments in the project",
        "vars": [("JIRA_PAT", True, "Personal access token")],
        "url": ("DELIVERY_URL", "Jira base URL, e.g. https://jira.example.com"),
    },
    "trello": {
        "where": "https://trello.com/apps/admin → your Power-Up (create one if none) → "
                 "Trello Auth tab → Generate a new API key; then the 'Token' link next to it",
        "scope": "read,write (no account scope needed)",
        "vars": [("TRELLO_API_KEY", True, "API key"), ("TRELLO_TOKEN", True, "Token")],
        "url": None,
    },
    "deck": {
        "where": "Nextcloud: Personal settings → Security → Devices & sessions → "
                 "enter an app name → create new app password",
        "scope": "an app password acts as you: you need edit rights on the board",
        "vars": [("NEXTCLOUD_USER", False, "Nextcloud username"),
                 ("NEXTCLOUD_APP_PASSWORD", True, "App password")],
        "url": ("DELIVERY_URL", "Nextcloud URL, e.g. https://cloud.example.org"),
    },
    "github": {
        "where": "https://github.com/settings/personal-access-tokens/new (fine-grained), "
                 "or skip this and use `gh auth login`",
        "scope": "Repository access: only this repo · Repository permissions → Issues: "
                 "Read and write. (A Projects board you own personally needs `gh auth login` "
                 "+ `gh auth refresh -s project` instead: fine-grained tokens cannot reach it)",
        "vars": [("GH_TOKEN", True, "Fine-grained personal access token")],
        "url": None,
    },
    "gitlab": {
        "where": "GitLab: avatar → Edit profile → Access tokens → Add new token "
                 "(gitlab.com: https://gitlab.com/-/user_settings/personal_access_tokens), "
                 "or skip this and use `glab auth login`",
        "scope": "api (read_api is not enough to create or move issues)",
        "vars": [("GITLAB_TOKEN", True, "Personal access token")],
        "url": ("DELIVERY_URL", "GitLab URL [https://gitlab.com]"),
    },
    "linear": {
        "where": "https://linear.app/settings/account/security → Personal API keys → New key",
        "scope": "Read and Write (or Create issues + Create comments), limited to this team",
        "vars": [("LINEAR_API_KEY", True, "Personal API key")],
        "url": None,
    },
}

DEFAULT_BASE = {
    "trello": "https://api.trello.com",
    "github": "https://api.github.com",
    "gitlab": "https://gitlab.com",
    "linear": "https://api.linear.app",
}

FIX = {
    401: ("unauthorized", "The credential is wrong, expired, or does not match the account. "
          "Create a new one (Connect step 1) and run `tracker.py secret <tracker>` again."),
    403: ("forbidden", "The credential works but lacks a scope or project permission. "
          "Grant the scope in Connect step 2, or ask the project admin for access."),
    404: ("not_found", "Wrong board, project, repo or site URL, or this account cannot see it. "
          "Check the identifier and the URL."),
}


class TrackerError(Exception):
    def __init__(self, error, fix, status=None, code=1):
        super().__init__(error)
        self.error, self.fix, self.status, self.code = error, fix, status, code


# ------------------------------------------------------------------ settings --

def read_env_file(path=ENV_FILE):
    """Parse KEY=value lines, shell-quoted as `secret` writes them."""
    values = {}
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, raw = line.split("=", 1)
                parts = shlex.split(raw) if raw else [""]
                values[key.strip()] = parts[0] if parts else ""
    except FileNotFoundError:
        pass
    return values


def read_config(path=CONFIG_FILE):
    """ponytail: two keys by regex, not a YAML parser; the template keeps them simple."""
    out = {}
    try:
        text = open(path).read()
    except FileNotFoundError:
        return out
    for key in ("type", "url", "flavor"):
        m = re.search(r"^\s+%s:\s*([^\s#]+)" % key, text, re.M)
        if m:
            out[key] = m.group(1).strip("\"'")
    return out


def settings(args):
    env = read_env_file()
    env.update({k: v for k, v in os.environ.items()})  # the environment overrides the file
    cfg = read_config()
    tracker = args.tracker or env.get("DELIVERY_TRACKER") or cfg.get("type")
    if tracker == "jira" and cfg.get("flavor") == "datacenter" and not args.tracker:
        tracker = "jira-dc"
    if tracker not in CREDENTIALS:
        raise TrackerError("unknown_tracker", "Pass --tracker with one of: " + ", ".join(CREDENTIALS), code=2)
    url = args.url or env.get("DELIVERY_URL") or cfg.get("url") or DEFAULT_BASE.get(tracker)
    base = args.api_base or env.get("DELIVERY_API_BASE") or url
    if not base:
        raise TrackerError("missing_url", "This tracker needs its site URL: --url or DELIVERY_URL.", code=2)
    missing = [name for name, _, _ in CREDENTIALS[tracker]["vars"] if not env.get(name)]
    if missing:
        raise TrackerError("missing_credential",
                           "Not set: %s. Run `python3 %s secret %s` in your terminal."
                           % (", ".join(missing), sys.argv[0], tracker), code=2)
    return tracker, base.rstrip("/"), env


# ---------------------------------------------------------------------- http --

def auth_headers(tracker, env):
    if tracker == "jira":
        raw = "%s:%s" % (env["JIRA_EMAIL"], env["JIRA_API_TOKEN"])
        return {"Authorization": "Basic " + base64.b64encode(raw.encode()).decode()}
    if tracker == "jira-dc":
        return {"Authorization": "Bearer " + env["JIRA_PAT"]}
    if tracker == "trello":
        return {"Authorization": 'OAuth oauth_consumer_key="%s", oauth_token="%s"'
                % (env["TRELLO_API_KEY"], env["TRELLO_TOKEN"])}
    if tracker == "deck":
        raw = "%s:%s" % (env["NEXTCLOUD_USER"], env["NEXTCLOUD_APP_PASSWORD"])
        return {"Authorization": "Basic " + base64.b64encode(raw.encode()).decode(),
                "OCS-APIRequest": "true"}
    if tracker == "github":
        return {"Authorization": "Bearer " + env["GH_TOKEN"],
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"}
    if tracker == "gitlab":
        return {"PRIVATE-TOKEN": env["GITLAB_TOKEN"]}
    if tracker == "linear":
        return {"Authorization": env["LINEAR_API_KEY"]}  # personal key: no "Bearer"
    raise AssertionError(tracker)


def call(ctx, method, path, body=None, query=None):
    tracker, base, env = ctx
    url = base + path
    if query:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(query)
    headers = {"Accept": "application/json", **auth_headers(tracker, env)}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        status = exc.code
        if path == "/graphql":  # GraphQL APIs report errors in the body, often with 400
            try:
                payload = json.loads(exc.read() or b"null")
            except ValueError:
                payload = None
            if isinstance(payload, dict) and payload.get("errors"):
                return payload
        if status in FIX:
            name, fix = FIX[status]
            raise TrackerError(name, fix, status)
        if status == 429:
            raise TrackerError("rate_limited", "Wait %s seconds and retry once."
                               % (exc.headers.get("Retry-After") or "a few"), status)
        raise TrackerError("http_%d" % status, "Unexpected response from the tracker; "
                           "check the URL and references/trackers.md.", status)
    except (urllib.error.URLError, OSError) as exc:
        raise TrackerError("unreachable", "No response from %s (%s). Check the URL, VPN or "
                           "network; planning continues locally." % (base, getattr(exc, "reason", exc)))
    return json.loads(raw) if raw else None


def graphql(ctx, query, variables=None):
    out = call(ctx, "POST", "/graphql", {"query": query, "variables": variables or {}})
    errors = (out or {}).get("errors")
    if errors:
        text = json.dumps(errors).lower()
        if "ratelimited" in text:
            raise TrackerError("rate_limited", "Rate limited; wait a minute and retry once.", 429)
        if "authentication" in text or "unauthorized" in text:
            name, fix = FIX[401]
            raise TrackerError(name, fix, 401)
        if "forbidden" in text or "permission" in text:
            name, fix = FIX[403]
            raise TrackerError(name, fix, 403)
        if "not found" in text or "could not resolve" in text or "entity not found" in text:
            name, fix = FIX[404]
            raise TrackerError(name, fix, 404)
        raise TrackerError("graphql_error", errors[0].get("message", "GraphQL error"))
    return out["data"]


def enc(value):
    return urllib.parse.quote(str(value), safe="")


# --------------------------------------------------------------- operations --

def whoami(ctx):
    t = ctx[0]
    if t in ("jira", "jira-dc"):
        me = call(ctx, "GET", "/rest/api/%s/myself" % ("3" if t == "jira" else "2"))
        # Cloud returns accountId; Data Center returns name (the username) and no accountId
        return {"user": me.get("displayName"), "id": me.get("accountId") or me.get("name")}
    if t == "trello":
        me = call(ctx, "GET", "/1/members/me", query={"fields": "fullName,username"})
        return {"user": me.get("fullName") or me.get("username"), "id": me.get("username")}
    if t == "deck":
        me = call(ctx, "GET", "/ocs/v2.php/cloud/user")  # JSON via the Accept header
        data = me["ocs"]["data"]
        return {"user": data.get("displayname") or data.get("id"), "id": data.get("id")}
    if t == "github":
        me = call(ctx, "GET", "/user")
        return {"user": me.get("name") or me.get("login"), "id": me.get("login")}
    if t == "gitlab":
        me = call(ctx, "GET", "/api/v4/user")
        return {"user": me.get("name") or me.get("username"), "id": me.get("username")}
    if t == "linear":
        me = graphql(ctx, "query { viewer { id name email } }")["viewer"]
        return {"user": me.get("name"), "id": me.get("id")}
    raise AssertionError(t)


def boards(ctx):
    t = ctx[0]
    if t == "jira":
        out, start = [], 0
        while True:  # ponytail: startAt paging, capped at 10 pages (500 projects)
            page = call(ctx, "GET", "/rest/api/3/project/search",
                        query={"startAt": start, "maxResults": 50})
            out += [{"id": p["key"], "name": p["name"]} for p in page.get("values", [])]
            if page.get("isLast", True) or start >= 450:
                return out
            start += 50
    if t == "jira-dc":
        return [{"id": p["key"], "name": p["name"]} for p in call(ctx, "GET", "/rest/api/2/project")]
    if t == "trello":
        rows = call(ctx, "GET", "/1/members/me/boards", query={"filter": "open", "fields": "name,url"})
        return [{"id": b["id"], "name": b["name"]} for b in rows]
    if t == "deck":
        rows = call(ctx, "GET", "/index.php/apps/deck/api/v1.0/boards")
        return [{"id": b["id"], "name": b["title"]} for b in rows if not b.get("archived")]
    if t == "github":
        repos = call(ctx, "GET", "/user/repos", query={"per_page": 100, "sort": "updated"})
        out = [{"id": r["full_name"], "name": r["full_name"], "kind": "repo"} for r in repos]
        try:
            v = graphql(ctx, "query { viewer { login projectsV2(first: 50) { nodes { number title } } } }")["viewer"]
            out += [{"id": "project:%s/%d" % (v["login"], p["number"]), "name": p["title"], "kind": "project"}
                    for p in v["projectsV2"]["nodes"]]
        except TrackerError:
            pass  # a token without project access still lists repos
        return out
    if t == "gitlab":
        rows = call(ctx, "GET", "/api/v4/projects", query={"membership": "true", "simple": "true", "per_page": 100})
        return [{"id": p["path_with_namespace"], "name": p["name"]} for p in rows]
    if t == "linear":
        rows = graphql(ctx, "query { teams { nodes { id key name } } }")["teams"]["nodes"]
        return [{"id": r["key"], "name": r["name"], "uuid": r["id"]} for r in rows]
    raise AssertionError(t)


def columns(ctx, board):
    t = ctx[0]
    if t in ("jira", "jira-dc"):
        v = "3" if t == "jira" else "2"
        names = []
        for issue_type in call(ctx, "GET", "/rest/api/%s/project/%s/statuses" % (v, enc(board))):
            for s in issue_type.get("statuses", []):
                if s["name"] not in names:
                    names.append(s["name"])
        return [{"id": n, "name": n} for n in names]
    if t == "trello":
        return [{"id": l["id"], "name": l["name"]} for l in call(ctx, "GET", "/1/boards/%s/lists" % enc(board))]
    if t == "deck":
        rows = call(ctx, "GET", "/index.php/apps/deck/api/v1.0/boards/%s/stacks" % enc(board))
        return [{"id": s["id"], "name": s["title"]} for s in sorted(rows, key=lambda s: s.get("order", 0))]
    if t == "github":
        if board.startswith("project:"):
            owner, number = board[len("project:"):].rsplit("/", 1)
            q = ("query($login: String!, $n: Int!) { user(login: $login) { projectV2(number: $n) { "
                 "field(name: \"Status\") { ... on ProjectV2SingleSelectField { options { id name } } } } } }")
            node = graphql(ctx, q, {"login": owner, "n": int(number)})["user"]["projectV2"]
            return [{"id": o["id"], "name": o["name"]} for o in node["field"]["options"]]
        rows = call(ctx, "GET", "/repos/%s/labels" % board, query={"per_page": 100})
        return [{"id": l["name"], "name": l["name"], "kind": "label"} for l in rows]
    if t == "gitlab":
        rows = call(ctx, "GET", "/api/v4/projects/%s/labels" % enc(board), query={"per_page": 100})
        return [{"id": l["name"], "name": l["name"], "kind": "label"} for l in rows]
    if t == "linear":
        q = ("query($key: String!) { workflowStates(filter: {team: {key: {eq: $key}}}) "
             "{ nodes { id name type } } }")
        rows = graphql(ctx, q, {"key": board})["workflowStates"]["nodes"]
        return [{"id": s["id"], "name": s["name"], "type": s["type"]} for s in rows]
    raise AssertionError(t)


def create_board(ctx, name, key=None):
    t = ctx[0]
    if t in ("jira", "jira-dc"):
        if not key:
            raise TrackerError("missing_key", "A Jira project needs a key: --key SAL.", code=2)
        me = whoami(ctx)
        body = {"key": key, "name": name, "projectTypeKey": "software"}
        body["leadAccountId" if t == "jira" else "lead"] = me["id"]
        try:
            p = call(ctx, "POST", "/rest/api/%s/project" % ("3" if t == "jira" else "2"), body)
        except TrackerError as exc:
            if exc.status in (401, 403):
                raise TrackerError("needs_jira_admin", "Creating a Jira project needs the Administer "
                                   "Jira global permission. Ask a Jira admin, or pick an existing "
                                   "project.", exc.status)
            raise
        return {"id": p.get("key", key), "name": name}
    if t == "trello":
        b = call(ctx, "POST", "/1/boards/", query={"name": name})
        return {"id": b["id"], "name": b["name"]}
    if t == "deck":
        b = call(ctx, "POST", "/index.php/apps/deck/api/v1.0/boards", {"title": name, "color": "0082c9"})
        return {"id": b["id"], "name": b["title"]}
    if t == "github":
        v = graphql(ctx, "query { viewer { id } }")["viewer"]
        q = ("mutation($o: ID!, $t: String!) { createProjectV2(input: {ownerId: $o, title: $t}) "
             "{ projectV2 { number title owner { ... on User { login } } } } }")
        p = graphql(ctx, q, {"o": v["id"], "t": name})["createProjectV2"]["projectV2"]
        login = (p.get("owner") or {}).get("login", "")
        return {"id": "project:%s/%d" % (login, p["number"]), "name": p["title"],
                "note": "A Projects board; issues still live in a repository."}
    if t == "gitlab":
        p = call(ctx, "POST", "/api/v4/projects", {"name": name})
        return {"id": p["path_with_namespace"], "name": p["name"]}
    if t == "linear":
        q = "mutation($n: String!) { teamCreate(input: {name: $n}) { success team { id key name } } }"
        try:
            team = graphql(ctx, q, {"n": name})["teamCreate"]["team"]
        except TrackerError as exc:
            if exc.status == 403:
                raise TrackerError("needs_linear_admin", "This key may not create teams. Ask a "
                                   "workspace admin, or pick an existing team.", 403)
            raise
        return {"id": team["key"], "name": team["name"], "uuid": team["id"]}
    raise AssertionError(t)


def create_column(ctx, board, name, state_type="started"):
    t = ctx[0]
    if t in ("jira", "jira-dc"):
        raise TrackerError("needs_jira_admin", "Jira statuses belong to the project's workflow; "
                           "adding one needs a Jira admin. Map this status to an existing one, "
                           "or use a label.", code=2)
    if t == "trello":
        l = call(ctx, "POST", "/1/lists", query={"name": name, "idBoard": board, "pos": "bottom"})
        return {"id": l["id"], "name": l["name"]}
    if t == "deck":
        existing = columns(ctx, board)
        s = call(ctx, "POST", "/index.php/apps/deck/api/v1.0/boards/%s/stacks" % enc(board),
                 {"title": name, "order": len(existing)})
        return {"id": s["id"], "name": s["title"]}
    if t == "github":
        if board.startswith("project:"):
            raise TrackerError("unsupported_here", "Add the option in the project's Status field "
                               "settings on GitHub; this helper does not edit project fields.", code=2)
        l = call(ctx, "POST", "/repos/%s/labels" % board, {"name": name})
        return {"id": l["name"], "name": l["name"], "kind": "label"}
    if t == "gitlab":
        l = call(ctx, "POST", "/api/v4/projects/%s/labels" % enc(board), {"name": name, "color": "#428BCA"})
        return {"id": l["name"], "name": l["name"], "kind": "label"}
    if t == "linear":
        teams = [b for b in boards(ctx) if b["id"] == board]
        if not teams:
            name_, fix = FIX[404]
            raise TrackerError(name_, fix, 404)
        q = ("mutation($i: WorkflowStateCreateInput!) { workflowStateCreate(input: $i) "
             "{ success workflowState { id name type } } }")
        s = graphql(ctx, q, {"i": {"teamId": teams[0]["uuid"], "name": name,
                                   "type": state_type, "color": "#bec2c8"}})
        s = s["workflowStateCreate"]["workflowState"]
        return {"id": s["id"], "name": s["name"], "type": s["type"]}
    raise AssertionError(t)


# ------------------------------------------------------------------- secret --

def ensure_ignored():
    """Add .delivery/.env to .gitignore if needed, then prove git ignores it."""
    entry = ".delivery/.env"
    try:
        lines = open(".gitignore").read().splitlines()
    except FileNotFoundError:
        lines = []
    if entry not in [l.strip() for l in lines]:
        with open(".gitignore", "a") as fh:
            if lines and lines[-1] != "":
                fh.write("\n")
            fh.write(entry + "\n")
    probe = subprocess.run(["git", "check-ignore", "-q", entry], capture_output=True)
    if probe.returncode != 0:
        raise TrackerError("not_ignored", "git does not ignore .delivery/.env here (not a git "
                           "repository, or a rule re-includes it). Nothing was written. Fix "
                           ".gitignore, or keep the credential in your shell environment.", code=2)


def quote(value):
    return "'" + value.replace("'", "'\\''") + "'"


def write_env(values, path=ENV_FILE):
    current = read_env_file(path)
    current.update(values)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as fh:
        fh.write("# delivery-planner credentials. Git-ignored. Never commit, cat or paste.\n")
        for k, v in current.items():
            fh.write("%s=%s\n" % (k, quote(v)))
    os.chmod(path, 0o600)


def secret(args):
    tracker = args.name
    if tracker not in CREDENTIALS:
        raise TrackerError("unknown_tracker", "One of: " + ", ".join(CREDENTIALS), code=2)
    spec = CREDENTIALS[tracker]
    ensure_ignored()  # before a single character is typed
    say = lambda s: print(s, file=sys.stderr)
    say("Create the credential here:  " + spec["where"])
    say("Least access it needs:       " + spec["scope"])
    say("Input for secrets is hidden. Values go to .delivery/.env (git-ignored, mode 600).")
    values = {"DELIVERY_TRACKER": tracker}
    if spec["url"]:
        name, prompt = spec["url"]
        default = args.url or DEFAULT_BASE.get(tracker, "")
        values[name] = (input(prompt + ": ").strip() or default).rstrip("/")
    for name, hidden, prompt in spec["vars"]:
        value = (getpass.getpass(prompt + ": ") if hidden else input(prompt + ": ")).strip()
        if not value:
            raise TrackerError("empty_value", "%s was empty; nothing was written." % name, code=2)
        values[name] = value
    write_env(values)
    for k, v in values.items():
        os.environ[k] = v
    args.tracker = tracker
    result = {"written": sorted(values), "file": ENV_FILE, "mode": "600"}
    try:
        result["whoami"] = whoami(settings(args))
        result["ok"] = True
    except TrackerError as exc:
        result.update(ok=False, error=exc.error, status=exc.status, fix=exc.fix)
    return result


# --------------------------------------------------------------------- main --

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--tracker", choices=sorted(CREDENTIALS))
    p.add_argument("--url")
    p.add_argument("--api-base")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("secret")
    s.add_argument("name")
    sub.add_parser("whoami")
    sub.add_parser("boards")
    c = sub.add_parser("columns")
    c.add_argument("board")
    cb = sub.add_parser("create-board")
    cb.add_argument("name")
    cb.add_argument("--key")
    cc = sub.add_parser("create-column")
    cc.add_argument("board")
    cc.add_argument("name")
    cc.add_argument("--type", default="started",
                    choices=["backlog", "unstarted", "started", "completed", "canceled"],
                    help="linear only: the workflow state type")
    args = p.parse_args(argv)
    try:
        if args.cmd == "secret":
            out = secret(args)
        else:
            ctx = settings(args)
            if args.cmd == "whoami":
                out = {"ok": True, "tracker": ctx[0], **whoami(ctx)}
            elif args.cmd == "boards":
                out = {"ok": True, "tracker": ctx[0], "boards": boards(ctx)}
            elif args.cmd == "columns":
                out = {"ok": True, "tracker": ctx[0], "board": args.board, "columns": columns(ctx, args.board)}
            elif args.cmd == "create-board":
                out = {"ok": True, "tracker": ctx[0], "created": create_board(ctx, args.name, args.key)}
            else:
                out = {"ok": True, "tracker": ctx[0], "created": create_column(ctx, args.board, args.name, args.type)}
    except TrackerError as exc:
        print(json.dumps({"ok": False, "error": exc.error, "status": exc.status, "fix": exc.fix}))
        return exc.code
    print(json.dumps(out))
    return 0 if out.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
