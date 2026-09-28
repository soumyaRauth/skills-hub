#!/usr/bin/env python3
"""Self-check for tracker.py against a local mock of each tracker. Stdlib only.

    python3 skills/delivery-planner/scripts/test_tracker.py

Asserts method, path and auth header shape per tracker; that documented
response shapes parse; that 401/403/404 give distinct errors naming the fix;
and that `secret` refuses to write outside git-ignore, writes mode 600 and
never prints a value.
"""
import base64
import builtins
import contextlib
import getpass
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracker  # noqa: E402

SECRET = "not-a-real-token-7f3a"
ROUTES = {}      # (method, path) -> (status, body)
SEEN = []        # (method, path, headers, body)
FORCE = {"status": None}


class Mock(BaseHTTPRequestHandler):
    def _serve(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode() if length else ""
        path = self.path.split("?", 1)[0]
        SEEN.append((self.command, self.path, {k.lower(): v for k, v in self.headers.items()}, body))
        status, payload = ROUTES.get((self.command, path), (404, {"message": "no route"}))
        if FORCE["status"]:
            status, payload = FORCE["status"], {"message": "forced"}
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_POST = do_PUT = _serve

    def log_message(self, *a):
        pass


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = tracker.main(list(argv))
    return code, json.loads(out.getvalue())


def last():
    return SEEN[-1]


CREDS = {
    "JIRA_EMAIL": "dev@example.com", "JIRA_API_TOKEN": SECRET, "JIRA_PAT": SECRET,
    "TRELLO_API_KEY": "key123", "TRELLO_TOKEN": SECRET,
    "NEXTCLOUD_USER": "dana", "NEXTCLOUD_APP_PASSWORD": SECRET,
    "GH_TOKEN": SECRET, "GITLAB_TOKEN": SECRET, "LINEAR_API_KEY": SECRET,
}

JIRA_STATUSES = [{"name": "Task", "statuses": [{"id": "1", "name": "To Do"}, {"id": "3", "name": "Done"}]},
                 {"name": "Bug", "statuses": [{"id": "1", "name": "To Do"}, {"id": "2", "name": "In Progress"}]}]


def graphql_router(handler_map):
    """Linear and GitHub GraphQL share one path; answer by a keyword in the query."""
    def pick(body):
        q = json.loads(body)["query"]
        for word, payload in handler_map.items():
            if word in q:
                return payload
        return {"errors": [{"message": "unknown query"}]}
    return pick


def check(name, cond, detail=""):
    if not cond:
        raise AssertionError("%s %s" % (name, detail))
    print("ok   " + name)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Mock)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % server.server_address[1]
    work = tempfile.mkdtemp()
    os.chdir(work)
    os.environ.update(CREDS)
    os.environ["DELIVERY_API_BASE"] = base
    os.environ["DELIVERY_URL"] = "https://unused.example"

    # ---- jira cloud
    ROUTES.update({
        ("GET", "/rest/api/3/myself"): (200, {"accountId": "abc", "displayName": "Dana Reyes"}),
        ("GET", "/rest/api/3/project/search"): (200, {"values": [{"key": "SAL", "name": "Salon"}], "isLast": True}),
        ("GET", "/rest/api/3/project/SAL/statuses"): (200, JIRA_STATUSES),
        ("POST", "/rest/api/3/project"): (201, {"key": "NEW", "id": 10001}),
    })
    code, out = run("--tracker", "jira", "whoami")
    m, p, h, _ = last()
    check("jira whoami", code == 0 and out["user"] == "Dana Reyes" and p == "/rest/api/3/myself")
    check("jira basic auth", h["authorization"] == "Basic " + base64.b64encode(("dev@example.com:" + SECRET).encode()).decode())
    code, out = run("--tracker", "jira", "boards")
    check("jira boards", out["boards"] == [{"id": "SAL", "name": "Salon"}])
    code, out = run("--tracker", "jira", "columns", "SAL")
    check("jira columns dedupe", [c["name"] for c in out["columns"]] == ["To Do", "Done", "In Progress"])
    code, out = run("--tracker", "jira", "create-board", "New", "--key", "NEW")
    body = json.loads(last()[3])
    check("jira create project", code == 0 and last()[0] == "POST" and body["leadAccountId"] == "abc" and body["key"] == "NEW")
    code, out = run("--tracker", "jira", "create-column", "SAL", "Blocked")
    check("jira create-column refused, names admin", code == 2 and out["error"] == "needs_jira_admin")

    # ---- jira data center
    ROUTES.update({
        ("GET", "/rest/api/2/myself"): (200, {"name": "dana", "displayName": "Dana Reyes"}),
        ("GET", "/rest/api/2/project"): (200, [{"key": "SAL", "name": "Salon"}]),
    })
    code, out = run("--tracker", "jira-dc", "whoami")
    check("jira-dc whoami + bearer", out["id"] == "dana" and last()[2]["authorization"] == "Bearer " + SECRET)
    code, out = run("--tracker", "jira-dc", "boards")
    check("jira-dc boards", out["boards"][0]["id"] == "SAL")

    # ---- trello
    ROUTES.update({
        ("GET", "/1/members/me"): (200, {"fullName": "Dana Reyes", "username": "dana"}),
        ("GET", "/1/members/me/boards"): (200, [{"id": "b1", "name": "Salon", "url": "u"}]),
        ("GET", "/1/boards/b1/lists"): (200, [{"id": "l1", "name": "To Do"}, {"id": "l2", "name": "Done"}]),
        ("POST", "/1/boards/"): (200, {"id": "b2", "name": "New"}),
        ("POST", "/1/lists"): (200, {"id": "l3", "name": "Blocked"}),
    })
    code, out = run("--tracker", "trello", "whoami")
    check("trello whoami + oauth header", out["user"] == "Dana Reyes"
          and last()[2]["authorization"] == 'OAuth oauth_consumer_key="key123", oauth_token="%s"' % SECRET)
    check("trello token not in URL", SECRET not in last()[1])
    code, out = run("--tracker", "trello", "boards")
    check("trello boards", out["boards"] == [{"id": "b1", "name": "Salon"}])
    code, out = run("--tracker", "trello", "columns", "b1")
    check("trello lists", [c["id"] for c in out["columns"]] == ["l1", "l2"])
    code, out = run("--tracker", "trello", "create-board", "New")
    check("trello create board", code == 0 and last()[:2] == ("POST", "/1/boards/?name=New"))
    code, out = run("--tracker", "trello", "create-column", "b1", "Blocked")
    check("trello create list", code == 0 and "idBoard=b1" in last()[1] and out["created"]["id"] == "l3")

    # ---- nextcloud deck
    D = "/index.php/apps/deck/api/v1.0"
    ROUTES.update({
        ("GET", "/ocs/v2.php/cloud/user"): (200, {"ocs": {"data": {"id": "dana", "displayname": "Dana Reyes"}}}),
        ("GET", D + "/boards"): (200, [{"id": 12, "title": "Salon", "archived": False}, {"id": 9, "title": "Old", "archived": True}]),
        ("GET", D + "/boards/12/stacks"): (200, [{"id": 8, "title": "Doing", "order": 1}, {"id": 7, "title": "To do", "order": 0}]),
        ("POST", D + "/boards"): (200, {"id": 13, "title": "New"}),
        ("POST", D + "/boards/12/stacks"): (200, {"id": 9, "title": "Blocked"}),
    })
    code, out = run("--tracker", "deck", "whoami")
    m, p, h, _ = last()
    check("deck whoami + OCS header + basic", out["user"] == "Dana Reyes" and h.get("ocs-apirequest") == "true"
          and h["authorization"].startswith("Basic "))
    code, out = run("--tracker", "deck", "boards")
    check("deck boards skip archived", out["boards"] == [{"id": 12, "name": "Salon"}])
    code, out = run("--tracker", "deck", "columns", "12")
    check("deck stacks in order", [c["name"] for c in out["columns"]] == ["To do", "Doing"])
    code, out = run("--tracker", "deck", "create-column", "12", "Blocked")
    check("deck create stack", code == 0 and json.loads(last()[3]) == {"title": "Blocked", "order": 2})
    code, out = run("--tracker", "deck", "create-board", "New")
    check("deck create board", code == 0 and json.loads(last()[3])["title"] == "New")

    # ---- github
    gh = graphql_router({
        "projectsV2": {"data": {"viewer": {"login": "dana", "projectsV2": {"nodes": [{"number": 3, "title": "Salon"}]}}}},
        "createProjectV2": {"data": {"createProjectV2": {"projectV2": {"number": 4, "title": "New", "owner": {"login": "dana"}}}}},
        "viewer { id }": {"data": {"viewer": {"id": "U_1"}}},
        "field(name": {"data": {"user": {"projectV2": {"field": {"options": [{"id": "o1", "name": "Todo"}]}}}}},
    })
    ROUTES.update({
        ("GET", "/user"): (200, {"login": "dana", "name": "Dana Reyes"}),
        ("GET", "/user/repos"): (200, [{"full_name": "acme/salon"}]),
        ("GET", "/repos/acme/salon/labels"): (200, [{"name": "bug"}]),
        ("POST", "/repos/acme/salon/labels"): (201, {"name": "status:blocked"}),
    })
    Mock.graphql = gh
    Mock.graphql_status = 200
    orig = Mock._serve

    def serve_with_graphql(self):
        if self.path == "/graphql":
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length).decode()
            SEEN.append((self.command, self.path, {k.lower(): v for k, v in self.headers.items()}, body))
            status, payload = (FORCE["status"], {"message": "forced"}) if FORCE["status"] else (Mock.graphql_status, Mock.graphql(body))
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        orig(self)
    Mock.do_GET = Mock.do_POST = Mock.do_PUT = serve_with_graphql

    code, out = run("--tracker", "github", "whoami")
    h = last()[2]
    check("github whoami + headers", out["id"] == "dana" and h["authorization"] == "Bearer " + SECRET
          and h["x-github-api-version"] == "2022-11-28")
    code, out = run("--tracker", "github", "boards")
    check("github repos + projects", [b["id"] for b in out["boards"]] == ["acme/salon", "project:dana/3"])
    code, out = run("--tracker", "github", "columns", "acme/salon")
    check("github labels", out["columns"][0]["name"] == "bug")
    code, out = run("--tracker", "github", "columns", "project:dana/3")
    check("github project status options", out["columns"] == [{"id": "o1", "name": "Todo"}])
    code, out = run("--tracker", "github", "create-board", "New")
    check("github create project", out["created"]["id"] == "project:dana/4")
    code, out = run("--tracker", "github", "create-column", "acme/salon", "status:blocked")
    check("github create label", code == 0 and last()[:2] == ("POST", "/repos/acme/salon/labels"))

    # ---- gitlab
    ROUTES.update({
        ("GET", "/api/v4/user"): (200, {"username": "dana", "name": "Dana Reyes"}),
        ("GET", "/api/v4/projects"): (200, [{"path_with_namespace": "shop/storefront", "name": "storefront"}]),
        ("GET", "/api/v4/projects/shop%2Fstorefront/labels"): (200, [{"name": "status::ready"}]),
        ("POST", "/api/v4/projects/shop%2Fstorefront/labels"): (201, {"name": "status::blocked"}),
        ("POST", "/api/v4/projects"): (201, {"path_with_namespace": "dana/new", "name": "new"}),
    })
    code, out = run("--tracker", "gitlab", "whoami")
    check("gitlab whoami + PRIVATE-TOKEN", out["id"] == "dana" and last()[2]["private-token"] == SECRET)
    code, out = run("--tracker", "gitlab", "boards")
    check("gitlab projects", out["boards"][0]["id"] == "shop/storefront")
    code, out = run("--tracker", "gitlab", "columns", "shop/storefront")
    check("gitlab labels, path encoded", out["columns"][0]["name"] == "status::ready")
    code, out = run("--tracker", "gitlab", "create-column", "shop/storefront", "status::blocked")
    check("gitlab create label", code == 0 and "color" in json.loads(last()[3]))
    code, out = run("--tracker", "gitlab", "create-board", "new")
    check("gitlab create project", out["created"]["id"] == "dana/new")

    # ---- linear
    Mock.graphql = graphql_router({
        "viewer": {"data": {"viewer": {"id": "u1", "name": "Dana Reyes", "email": "d@example.com"}}},
        "teams": {"data": {"teams": {"nodes": [{"id": "t1", "key": "ENG", "name": "Engineering"}]}}},
        "workflowStates": {"data": {"workflowStates": {"nodes": [{"id": "s1", "name": "Todo", "type": "unstarted"}]}}},
    })
    code, out = run("--tracker", "linear", "whoami")
    check("linear whoami, key without Bearer", out["user"] == "Dana Reyes" and last()[2]["authorization"] == SECRET)
    code, out = run("--tracker", "linear", "boards")
    check("linear teams", out["boards"][0]["id"] == "ENG")
    code, out = run("--tracker", "linear", "columns", "ENG")
    check("linear states", out["columns"][0]["type"] == "unstarted")
    Mock.graphql = graphql_router({
        "teamCreate": {"data": {"teamCreate": {"success": True, "team": {"id": "t2", "key": "NEW", "name": "New"}}}},
        "workflowStateCreate": {"data": {"workflowStateCreate": {"success": True,
                                "workflowState": {"id": "s9", "name": "In Review", "type": "started"}}}},
        "teams": {"data": {"teams": {"nodes": [{"id": "t1", "key": "ENG", "name": "Engineering"}]}}},
    })
    code, out = run("--tracker", "linear", "create-board", "New")
    check("linear create team", code == 0 and out["created"]["id"] == "NEW")
    code, out = run("--tracker", "linear", "create-column", "ENG", "In Review")
    sent = json.loads(last()[3])["variables"]["i"]
    check("linear create state sends required fields", code == 0 and sent["teamId"] == "t1"
          and sent["type"] == "started" and sent["color"] and sent["name"] == "In Review")
    Mock.graphql = graphql_router({"viewer": {"errors": [{"message": "Authentication required, not authenticated",
                                                          "extensions": {"type": "authentication error"}}]}})
    code, out = run("--tracker", "linear", "whoami")
    check("linear graphql auth error → unauthorized", code == 1 and out["error"] == "unauthorized")
    Mock.graphql_status = 400
    Mock.graphql = graphql_router({"viewer": {"errors": [{"message": "Rate limit exceeded",
                                                          "extensions": {"code": "RATELIMITED"}}]}})
    code, out = run("--tracker", "linear", "whoami")
    check("linear 400 RATELIMITED → rate_limited", code == 1 and out["error"] == "rate_limited")
    Mock.graphql = graphql_router({"viewer": {"errors": [{"message": "Authentication required",
                                                          "extensions": {"type": "authentication error"}}]}})
    code, out = run("--tracker", "linear", "whoami")
    check("linear 400 auth error → unauthorized", out["error"] == "unauthorized")
    Mock.graphql_status = 200

    # ---- 401 / 403 / 404 are distinct and name the fix
    errors = {}
    for status in (401, 403, 404):
        FORCE["status"] = status
        code, out = run("--tracker", "trello", "columns", "b1")
        errors[status] = out
        check("http %d → %s" % (status, out["error"]), code == 1 and out["status"] == status and out["fix"])
    FORCE["status"] = None
    check("errors distinct", len({e["error"] for e in errors.values()}) == 3 and len({e["fix"] for e in errors.values()}) == 3)
    check("401 names the Connect step", "Connect step 1" in errors[401]["fix"])
    check("403 names the scope", "scope" in errors[403]["fix"])
    check("404 names the identifier", "identifier" in errors[404]["fix"])
    server_down = run("--tracker", "trello", "--api-base", "http://127.0.0.1:9", "whoami")
    check("unreachable is its own error", server_down[1]["error"] == "unreachable")

    # ---- secret: refuses outside git-ignore
    for k in CREDS:
        os.environ.pop(k)
    typed = {"getpass": [], "input": []}
    getpass.getpass = lambda prompt="": typed["getpass"].pop(0)
    builtins.input = lambda prompt="": typed["input"].pop(0)
    not_git = tempfile.mkdtemp()
    os.chdir(not_git)
    typed["getpass"] = ["key123", SECRET]
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        code, out = run("secret", "trello")
    check("secret refuses when not git-ignored", code == 2 and out["error"] == "not_ignored")
    check("nothing written on refusal", not os.path.exists(".delivery/.env"))
    check("refusal happens before any prompt", typed["getpass"] == ["key123", SECRET])

    # ---- secret: writes 600, ignores, never prints a value
    repo = tempfile.mkdtemp()
    os.chdir(repo)
    subprocess.run(["git", "init", "-q"], check=True)
    ROUTES[("GET", "/1/members/me")] = (200, {"fullName": "Dana Reyes", "username": "dana"})
    typed["getpass"] = ["key123", "it's-" + SECRET]
    err = io.StringIO()
    out_buf = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out_buf):
        code = tracker.main(["secret", "trello"])
    printed = out_buf.getvalue() + err.getvalue()
    out = json.loads(out_buf.getvalue())
    mode = stat.S_IMODE(os.stat(".delivery/.env").st_mode)
    check("secret writes and proves identity", code == 0 and out["ok"] and out["whoami"]["user"] == "Dana Reyes")
    check("secret file mode 600", mode == 0o600, oct(mode))
    check(".gitignore has the entry", ".delivery/.env" in open(".gitignore").read())
    check("git check-ignore passes", subprocess.run(["git", "check-ignore", "-q", ".delivery/.env"]).returncode == 0)
    check("no value printed", SECRET not in printed and "key123" not in printed)
    check("guidance names where + scope", "trello.com/apps/admin" in err.getvalue() and "read,write" in err.getvalue())
    check("quoted value round-trips", tracker.read_env_file()["TRELLO_TOKEN"] == "it's-" + SECRET)
    check("sent as header, not echoed", SEEN[-1][2]["authorization"].endswith('oauth_token="it\'s-%s"' % SECRET))

    # ---- env overrides the file; missing credential names the command
    os.environ["TRELLO_TOKEN"] = "from-env"
    run("--tracker", "trello", "whoami")
    check("env var overrides .delivery/.env", 'oauth_token="from-env"' in SEEN[-1][2]["authorization"])
    del os.environ["TRELLO_TOKEN"]
    os.chdir(tempfile.mkdtemp())
    code, out = run("--tracker", "linear", "whoami")
    check("missing credential says how to add it", code == 2 and "secret linear" in out["fix"])

    server.shutdown()
    print("all tracker.py checks passed")


if __name__ == "__main__":
    main()
