#!/usr/bin/env python3
"""On-page and site-level SEO checks for the SEO Growth Engine skill.

Standard library only. Reports what it observes; judgment stays with the
person or agent reading the output.

  seo_audit.py page    <url-or-html-file> [--base URL] [--json]
  seo_audit.py crawl   <start-url> [--max-pages N] [--delay S] [--map-origin PROD=LOCAL] [--json]
  seo_audit.py sitemap <sitemap-or-site-url> [--check] [--max-urls N] [--map-origin PROD=LOCAL] [--json]
  seo_audit.py robots  <site-url> [--path /x ...] [--json]

The crawler stays on the start URL's host, obeys robots.txt for the "*"
group, waits between requests, and stops at --max-pages. It identifies
itself honestly and never pretends to be a search engine.
"""

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from html.parser import HTMLParser

USER_AGENT = "seo-growth-audit/1.0 (+https://github.com/soumyaRauth/skills-hub)"
ROBOTS_TOKEN = "seo-growth-audit"
MAX_BYTES = 5_000_000
TIMEOUT = 20
REDIRECT_CODES = (301, 302, 303, 307, 308)
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


# --------------------------------------------------------------- fetching ---

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _headers(msg):
    out = {}
    if msg is None:
        return out
    for key, value in msg.items():
        key = key.lower()
        out[key] = out[key] + ", " + value if key in out else value
    return out


def fetch(url, max_hops=10):
    """Fetch a URL, following redirects by hand so the chain is recorded."""
    chain = []
    current = url
    for _ in range(max_hops + 1):
        req = urllib.request.Request(current, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        try:
            with _OPENER.open(req, timeout=TIMEOUT) as resp:
                status, headers, body = resp.status, _headers(resp.headers), resp.read(MAX_BYTES)
        except urllib.error.HTTPError as err:
            status, headers = err.code, _headers(err.headers)
            try:
                body = err.read(MAX_BYTES)
            except Exception:
                body = b""
            finally:
                err.close()
        except Exception as err:  # DNS, TLS, timeout, refused
            chain.append([current, None])
            return {"url": url, "final_url": current, "status": None, "chain": chain,
                    "headers": {}, "body": b"", "error": f"{type(err).__name__}: {err}"}
        chain.append([current, status])
        if status in REDIRECT_CODES and headers.get("location"):
            current = urllib.parse.urljoin(current, headers["location"])
            continue
        return {"url": url, "final_url": current, "status": status, "chain": chain,
                "headers": headers, "body": body, "error": None}
    return {"url": url, "final_url": current, "status": None, "chain": chain,
            "headers": {}, "body": b"", "error": f"more than {max_hops} redirects"}


def decode(body, content_type=""):
    match = re.search(r"charset=([\w-]+)", content_type or "", re.I)
    if not match:
        match = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
        charset = match.group(1).decode("ascii", "ignore") if match else "utf-8"
    else:
        charset = match.group(1)
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def normalize(url):
    """Comparable form: lowercase scheme and host, no default port, no fragment, '/' for an empty path."""
    parts = urllib.parse.urlsplit(url.strip())
    scheme, netloc = parts.scheme.lower(), parts.netloc.lower()
    if (scheme == "http" and netloc.endswith(":80")) or (scheme == "https" and netloc.endswith(":443")):
        netloc = netloc.rsplit(":", 1)[0]
    return urllib.parse.urlunsplit((scheme, netloc, parts.path or "/", parts.query, ""))


def origin(url):
    parts = urllib.parse.urlsplit(normalize(url))
    return f"{parts.scheme}://{parts.netloc}"


class OriginMap:
    """Rewrites production URLs to a local server, so a build can be checked before it is deployed."""

    def __init__(self, pairs):
        self.pairs = []
        for pair in pairs or []:
            if "=" not in pair:
                raise SystemExit(f"--map-origin expects PROD=LOCAL, got {pair!r}")
            prod, local = pair.split("=", 1)
            self.pairs.append((origin(prod), origin(local)))

    def __call__(self, url):
        norm = normalize(url)
        for prod, local in self.pairs:
            if norm == prod or norm.startswith(prod + "/"):
                return local + norm[len(prod):]
        return norm

    def to_production(self, result):
        """Show production URLs in a result gathered from a local server."""
        text = json.dumps(result)
        for prod, local in self.pairs:
            text = text.replace(local, prod)
        out = json.loads(text)
        if self.pairs:
            out["checked_locally"] = [f"{local} (shown as {prod})" for prod, local in self.pairs]
        return out


# ----------------------------------------------------------------- parsing ---

class PageParser(HTMLParser):
    SKIP = {"script", "style", "noscript", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.metas = []
        self.link_tags = []
        self.headings = []
        self.anchors = []
        self.images = []
        self.jsonld = []
        self.base_href = None
        self.text = []
        self._title = None
        self._heading = None
        self._anchor = None
        self._script = None
        self._skip = 0
        self._svg = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        if tag == "html" and self.lang is None:
            self.lang = a.get("lang") or None
        elif tag == "svg":
            self._svg += 1
        elif tag == "title" and not self._svg:
            self._title = []
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("http-equiv") or "").strip().lower()
            if key:
                self.metas.append((key, a.get("content", "").strip()))
        elif tag == "link":
            rels = a.get("rel", "").lower().split()
            self.link_tags.append({"rel": rels, "href": a.get("href", "").strip(),
                                   "hreflang": a.get("hreflang")})
        elif tag == "base" and self.base_href is None:
            self.base_href = a.get("href") or None
        elif re.fullmatch(r"h[1-6]", tag):
            self._heading = [int(tag[1]), []]
        elif tag == "a":
            self._anchor = {"href": a.get("href"), "rel": a.get("rel", "").lower().split(), "text": []}
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt") if "alt" in a else None,
                                "width": a.get("width"), "height": a.get("height"),
                                "loading": a.get("loading")})
            if self._anchor is not None and a.get("alt"):
                self._anchor["text"].append(a.get("alt"))
        if tag == "script":
            kind = a.get("type", "").strip().lower()
            self._script = [] if kind == "application/ld+json" else None
            self._skip += 1
        elif tag in self.SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg:
            self._svg -= 1
        elif tag == "title" and self._title is not None:
            self.titles.append(" ".join("".join(self._title).split()))
            self._title = None
        elif re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            self.headings.append([self._heading[0], " ".join("".join(self._heading[1]).split())])
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            self._anchor["text"] = " ".join(" ".join(self._anchor["text"]).split())
            self.anchors.append(self._anchor)
            self._anchor = None
        if tag == "script":
            if self._script is not None:
                self.jsonld.append("".join(self._script))
            self._script = None
            self._skip = max(0, self._skip - 1)
        elif tag in self.SKIP:
            self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)
            return
        if self._skip:
            return
        if self._title is not None:
            self._title.append(data)
            return
        if self._heading is not None:
            self._heading[1].append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)
        self.text.append(data)


def _jsonld_types(node, out):
    if isinstance(node, list):
        for item in node:
            _jsonld_types(item, out)
    elif isinstance(node, dict):
        kind = node.get("@type")
        if isinstance(kind, list):
            out.extend(str(k) for k in kind)
        elif kind:
            out.append(str(kind))
        for key, value in node.items():
            if key != "@type" and isinstance(value, (dict, list)):
                _jsonld_types(value, out)


def parse_jsonld(raw):
    try:
        data = json.loads(raw)
    except ValueError as err:
        return {"types": [], "error": f"does not parse as JSON: {err}", "has_context": False}
    types = []
    _jsonld_types(data, types)
    items = data if isinstance(data, list) else [data]
    has_context = all(isinstance(i, dict) and "@context" in i for i in items) if items else False
    return {"types": types, "error": None, "has_context": has_context}


def _issue(issues, severity, code, message):
    issues.append({"severity": severity, "code": code, "message": message})


def analyze_html(html, page_url, status=200, headers=None, chain=None, origin_map=None):
    """Extract SEO facts from one HTML document and flag unambiguous problems."""
    headers = headers or {}
    chain = chain or [[page_url, status]]
    origin_map = origin_map or OriginMap([])
    parser = PageParser()
    parser.feed(html)
    parser.close()
    base = urllib.parse.urljoin(page_url, parser.base_href) if parser.base_href else page_url

    def meta(name):
        return [content for key, content in parser.metas if key == name]

    robots = ", ".join(meta("robots"))
    googlebot = ", ".join(meta("googlebot"))
    x_robots = headers.get("x-robots-tag", "")
    canonicals = [urllib.parse.urljoin(base, l["href"]) for l in parser.link_tags
                  if "canonical" in l["rel"] and l["href"]]
    canonical_raw = [l["href"] for l in parser.link_tags if "canonical" in l["rel"]]
    link_header_canon = re.findall(r'<([^>]+)>\s*;\s*rel="?canonical"?', headers.get("link", ""), re.I)
    hreflang = [{"hreflang": l["hreflang"], "href": urllib.parse.urljoin(base, l["href"])}
                for l in parser.link_tags if "alternate" in l["rel"] and l["hreflang"]]

    page_host = urllib.parse.urlsplit(origin_map(page_url)).netloc
    internal, external, nofollow, empty_text = [], [], 0, 0
    for anchor in parser.anchors:
        href = (anchor["href"] or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        target = urllib.parse.urljoin(base, href).split("#", 1)[0]
        if urllib.parse.urlsplit(target).scheme not in ("http", "https"):
            continue
        if "nofollow" in anchor["rel"]:
            nofollow += 1
        if not anchor["text"]:
            empty_text += 1
        if urllib.parse.urlsplit(origin_map(target)).netloc == page_host:
            internal.append({"url": normalize(target), "text": anchor["text"], "rel": anchor["rel"]})
        else:
            external.append(normalize(target))

    missing_alt = [i["src"] for i in parser.images if i["alt"] is None]
    no_dims = sum(1 for i in parser.images if not (i["width"] and i["height"]))
    jsonld = [parse_jsonld(raw) for raw in parser.jsonld]
    words = len(" ".join(parser.text).split())
    h1 = [text for level, text in parser.headings if level == 1]
    title = parser.titles[0] if parser.titles else None
    descriptions = meta("description")
    final_url = chain[-1][0]

    issues = []
    if status is None or status >= 400:
        _issue(issues, "critical" if status and status >= 500 else "high", "status",
               f"final status {status}")
    if len(chain) > 2:
        _issue(issues, "medium", "redirect-chain", f"{len(chain) - 1} redirect hops before the page")
    directives = " ".join([robots, googlebot, x_robots]).lower()
    if "noindex" in directives:
        where = ", ".join(n for n, v in (("meta robots", robots), ("meta googlebot", googlebot),
                                         ("X-Robots-Tag header", x_robots)) if "noindex" in v.lower())
        _issue(issues, "high", "noindex", f"noindex via {where}: excluded from search; confirm this is intended")
    if "nofollow" in directives:
        _issue(issues, "medium", "nofollow-page", "page-level nofollow: links here pass no signals; confirm intent")
    if not title:
        _issue(issues, "high", "title-missing", "no <title>, or it is empty")
    elif len(parser.titles) > 1:
        _issue(issues, "medium", "title-multiple", f"{len(parser.titles)} <title> elements")
    if not descriptions or not descriptions[0]:
        _issue(issues, "low", "description-missing", "no meta description; search engines will pick snippet text")
    elif len(descriptions) > 1:
        _issue(issues, "medium", "description-multiple", f"{len(descriptions)} meta descriptions")
    if len(canonicals) > 1 and len({normalize(c) for c in canonicals}) > 1:
        _issue(issues, "high", "canonical-conflict", "several different canonical URLs; search engines may ignore all of them")
    if canonicals:
        canon = normalize(canonicals[0])
        if canonical_raw and not re.match(r"https?://", canonical_raw[0]):
            _issue(issues, "low", "canonical-relative", f"canonical is relative ({canonical_raw[0]}); absolute is safer")
        if origin_map(canon) != origin_map(final_url):
            if origin(origin_map(canon)) != origin(origin_map(final_url)):
                _issue(issues, "medium", "canonical-other-origin",
                       f"canonical points to another origin: {canon}")
            else:
                _issue(issues, "info", "canonicalized", f"canonical points elsewhere: {canon}")
    else:
        _issue(issues, "low", "canonical-missing", "no canonical link")
    if not h1:
        _issue(issues, "medium", "h1-missing", "no <h1>")
    if not parser.lang:
        _issue(issues, "low", "lang-missing", "<html> has no lang attribute")
    if not meta("viewport"):
        _issue(issues, "medium", "viewport-missing", "no viewport meta tag; mobile rendering may suffer")
    if missing_alt:
        _issue(issues, "low", "img-alt-missing", f"{len(missing_alt)} image(s) without an alt attribute")
    for idx, block in enumerate(jsonld, 1):
        if block["error"]:
            _issue(issues, "high", "jsonld-invalid", f"JSON-LD block {idx} {block['error']}; it is ignored entirely")
        elif not block["has_context"]:
            _issue(issues, "medium", "jsonld-context", f"JSON-LD block {idx} has no @context")
    if status == 200 and words < 50:
        _issue(issues, "info", "little-text", f"{words} words of text in the HTML; check rendering or thin content")

    return {
        "url": page_url,
        "final_url": final_url,
        "status": status,
        "redirect_chain": chain,
        "content_type": headers.get("content-type"),
        "lang": parser.lang,
        "title": title,
        "title_count": len(parser.titles),
        "title_length": len(title) if title else 0,
        "meta_description": descriptions[0] if descriptions else None,
        "meta_robots": robots or None,
        "meta_googlebot": googlebot or None,
        "x_robots_tag": x_robots or None,
        "indexable": status == 200 and "noindex" not in directives,
        "canonical": normalize(canonicals[0]) if canonicals else None,
        "canonical_header": link_header_canon or None,
        "hreflang": hreflang,
        "viewport": bool(meta("viewport")),
        "open_graph": {k: v for k, v in parser.metas if k.startswith("og:")},
        "twitter": {k: v for k, v in parser.metas if k.startswith("twitter:")},
        "headings": parser.headings,
        "h1": h1,
        "links": {"internal": len(internal), "external": len(external), "nofollow": nofollow,
                  "no_anchor_text": empty_text},
        "internal_links": internal,
        "images": {"total": len(parser.images), "missing_alt": missing_alt,
                   "empty_alt": sum(1 for i in parser.images if i["alt"] == ""),
                   "missing_dimensions": no_dims},
        "jsonld": jsonld,
        "word_count": words,
        "issues": sorted(issues, key=lambda i: SEVERITY_ORDER[i["severity"]]),
    }


def audit_page(target, base=None, origin_map=None):
    if os.path.isfile(target):
        with open(target, "rb") as handle:
            body = handle.read()
        url = base or urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(target)))
        return analyze_html(decode(body), url, 200, {}, [[url, 200]], origin_map)
    res = fetch(target)
    if res["error"] and res["status"] is None:
        return {"url": target, "final_url": res["final_url"], "status": None, "redirect_chain": res["chain"],
                "issues": [{"severity": "critical", "code": "fetch-failed", "message": res["error"]}]}
    ctype = res["headers"].get("content-type", "")
    if "html" not in ctype.lower():
        return {"url": target, "final_url": res["final_url"], "status": res["status"],
                "redirect_chain": res["chain"], "content_type": ctype,
                "x_robots_tag": res["headers"].get("x-robots-tag"),
                "issues": [{"severity": "info", "code": "not-html", "message": f"content type {ctype or 'unknown'}"}]}
    return analyze_html(decode(res["body"], ctype), target, res["status"], res["headers"], res["chain"], origin_map)


# ------------------------------------------------------------------ robots ---

class Robots:
    """robots.txt as Google reads it (RFC 9309): groups by user agent, '*' and '$' patterns,
    the longest matching rule wins, and allow wins a tie."""

    def __init__(self, text):
        self.groups, self.sitemaps = [], []
        agents, rules, in_agents = [], [], False
        for raw in (text or "").splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            key, value = (part.strip() for part in line.split(":", 1))
            key = key.lower()
            if key == "user-agent":
                if not in_agents and agents:
                    self.groups.append((agents, rules))
                    agents, rules = [], []
                agents.append(value.lower())
                in_agents = True
            elif key == "sitemap":
                self.sitemaps.append(value)
            else:
                in_agents = False
                if key in ("allow", "disallow") and agents and value:
                    rules.append((key == "allow", value))
        if agents:
            self.groups.append((agents, rules))

    def rules_for(self, token):
        token = token.lower()
        named = [r for agents, rules in self.groups if token in agents for r in rules]
        if any(token in agents for agents, _ in self.groups):
            return named
        return [r for agents, rules in self.groups if "*" in agents for r in rules]

    @staticmethod
    def _matches(pattern, path):
        anchored = pattern.endswith("$")
        body = pattern[:-1] if anchored else pattern
        regex = "".join(".*" if ch == "*" else re.escape(ch) for ch in body)
        return re.match(regex + ("$" if anchored else ""), path) is not None

    def allowed(self, url, token="*"):
        parts = urllib.parse.urlsplit(url)
        path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
        if path == "/robots.txt":
            return True
        best = None
        for allow, pattern in self.rules_for(token):
            if self._matches(pattern, path):
                if best is None or len(pattern) > best[0] or (len(pattern) == best[0] and allow):
                    best = (len(pattern), allow)
        return True if best is None else best[1]


def load_robots(site_url, origin_map=None):
    origin_map = origin_map or OriginMap([])
    url = origin(origin_map(site_url)) + "/robots.txt"
    res = fetch(url)
    if res["status"] == 200:
        return Robots(decode(res["body"], res["headers"].get("content-type", ""))), res
    # A missing robots.txt (4xx) means everything may be crawled.
    return Robots(""), res


# ----------------------------------------------------------------- sitemap ---

def read_sitemap(url, origin_map=None, max_files=50, max_urls=50000):
    origin_map = origin_map or OriginMap([])
    urls, files, errors, queue, seen = [], [], [], deque([url]), set()
    while queue and len(files) < max_files and len(urls) < max_urls:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        res = fetch(origin_map(current))
        files.append({"url": current, "status": res["status"], "redirects": len(res["chain"]) - 1})
        if res["status"] != 200:
            errors.append(f"{current}: status {res['status']}{' ' + res['error'] if res['error'] else ''}")
            continue
        body = res["body"]
        if body[:2] == b"\x1f\x8b":
            try:
                body = gzip.decompress(body)
            except OSError as err:
                errors.append(f"{current}: gzip error {err}")
                continue
        try:
            root = ET.fromstring(body)
        except ET.ParseError as err:
            errors.append(f"{current}: not valid XML ({err})")
            continue
        tag = root.tag.rsplit("}", 1)[-1]
        for entry in root:
            loc = next((c.text.strip() for c in entry if c.tag.rsplit("}", 1)[-1] == "loc" and c.text), None)
            if not loc:
                continue
            lastmod = next((c.text.strip() for c in entry if c.tag.rsplit("}", 1)[-1] == "lastmod" and c.text), None)
            if tag == "sitemapindex":
                queue.append(loc)
            else:
                urls.append({"loc": normalize(loc), "lastmod": lastmod})
    return {"sitemaps": files, "urls": urls[:max_urls], "errors": errors,
            "truncated": bool(queue) or len(urls) >= max_urls}


def discover_sitemaps(site_url, robots, origin_map=None):
    if robots.sitemaps:
        return robots.sitemaps
    return [origin(site_url) + "/sitemap.xml"]


# ------------------------------------------------------------------- crawl ---

def crawl(start, max_pages=200, delay=0.5, origin_map=None):
    origin_map = origin_map or OriginMap([])
    start_local = origin_map(start)
    host = urllib.parse.urlsplit(start_local).netloc
    robots, robots_res = load_robots(start_local)
    sitemap_urls = discover_sitemaps(start, robots, origin_map)
    sitemap = {"sitemaps": [], "urls": [], "errors": [], "truncated": False}
    for sm in sitemap_urls:
        part = read_sitemap(sm, origin_map)
        for key in ("sitemaps", "urls", "errors"):
            sitemap[key].extend(part[key])
        sitemap["truncated"] |= part["truncated"]
    in_sitemap = {origin_map(u["loc"]) for u in sitemap["urls"]}

    pages, inlinks, depth, blocked = {}, {}, {start_local: 0}, []
    queue, queued = deque([start_local]), {start_local}
    seeded = False
    fetched = 0

    def visit(url):
        nonlocal fetched
        if not robots.allowed(url, ROBOTS_TOKEN):
            blocked.append(url)
            return None
        if fetched:
            time.sleep(delay)
        fetched += 1
        res = fetch(url)
        ctype = res["headers"].get("content-type", "")
        if res["status"] == 200 and "html" in ctype.lower():
            page = analyze_html(decode(res["body"], ctype), url, res["status"], res["headers"], res["chain"], origin_map)
        else:
            page = {"url": url, "final_url": res["final_url"], "status": res["status"],
                    "redirect_chain": res["chain"], "content_type": ctype, "error": res["error"],
                    "indexable": False, "internal_links": [], "issues": []}
        pages[url] = page
        return page

    # Links from the start page first, breadth-first, so depth is the shortest
    # click path. Then sitemap URLs those links never reached become extra
    # starting points, and their links are followed too: a page reached only
    # that way has no depth, but its links still count as inlinks.
    while fetched < max_pages:
        if not queue:
            if seeded:
                break
            seeded = True
            for url in sorted(in_sitemap - queued):
                if urllib.parse.urlsplit(url).netloc == host:
                    queued.add(url)
                    queue.append(url)
            continue
        url = queue.popleft()
        if url in pages:
            continue
        page = visit(url)
        if not page:
            continue
        for link in page.get("internal_links", []):
            target = origin_map(link["url"])
            if urllib.parse.urlsplit(target).netloc != host:
                continue
            if target != url:
                inlinks.setdefault(target, []).append({"from": url, "text": link["text"]})
            if url in depth and target not in depth:
                depth[target] = depth[url] + 1
            if target not in queued:
                queued.add(target)
                queue.append(target)
    truncated = bool(queue) or any(u not in pages for u in in_sitemap)
    return summarize_crawl(start_local, pages, inlinks, depth, in_sitemap, sitemap, robots,
                           robots_res, blocked, truncated, max_pages, origin_map)


def summarize_crawl(start, pages, inlinks, depth, in_sitemap, sitemap, robots, robots_res,
                    blocked, truncated, max_pages, origin_map):
    findings = []

    def add(severity, code, message, urls):
        if urls:
            findings.append({"severity": severity, "code": code, "message": message, "urls": sorted(urls)})

    html_ok = {u: p for u, p in pages.items() if p.get("status") == 200 and p.get("title") is not None}
    indexable = {u: p for u, p in html_ok.items() if p.get("indexable")}

    broken = {u: p for u, p in pages.items() if p.get("status") is None or p["status"] >= 400}
    add("high", "broken-internal", "internal URLs that fail (status, then linking pages)",
        [f"{u} [{p.get('status')}] ← " + ", ".join(sorted({l['from'] for l in inlinks.get(u, [])})[:5] or ["sitemap only"])
         for u, p in broken.items()])
    redirected = {u: p for u, p in pages.items() if len(p.get("redirect_chain", [])) > 1}
    add("medium", "internal-link-to-redirect", "internal links that point at redirects (link the final URL)",
        [f"{u} → {p['final_url']} ← " + ", ".join(sorted({l['from'] for l in inlinks.get(u, [])})[:5])
         for u, p in redirected.items() if inlinks.get(u)])
    add("medium", "redirect-chain", "redirect chains longer than one hop",
        [" → ".join(f"{c[0]} [{c[1]}]" for c in p["redirect_chain"]) for p in redirected.values()
         if len(p["redirect_chain"]) > 2])
    add("high", "noindex", "pages marked noindex (confirm each is intended)",
        [u for u, p in html_ok.items() if not p.get("indexable")])
    add("high", "sitemap-noindex", "sitemap lists pages that are noindex",
        [u for u, p in html_ok.items() if u in in_sitemap and not p.get("indexable")])
    add("high", "sitemap-not-200", "sitemap lists URLs that redirect or fail",
        [f"{u} [{pages[u].get('status')}{' → ' + pages[u]['final_url'] if len(pages[u].get('redirect_chain', [])) > 1 else ''}]"
         for u in in_sitemap if u in pages and (pages[u].get("status") != 200 or len(pages[u].get("redirect_chain", [])) > 1)])
    canon_elsewhere = {u: p for u, p in indexable.items()
                       if p.get("canonical") and origin_map(p["canonical"]) != origin_map(p["final_url"])}
    add("medium", "canonical-elsewhere", "pages whose canonical names another URL (page → canonical)",
        [f"{u} → {p['canonical']}" for u, p in canon_elsewhere.items()])
    add("medium", "sitemap-canonicalized", "sitemap lists pages that canonicalize elsewhere",
        [u for u in canon_elsewhere if u in in_sitemap])
    # Canonicalized to another page on this site: an intended variant (a filter, a
    # parameter). Canonicalized off-site: more likely a broken canonical, so it is
    # still judged as a page of its own.
    same_site_duplicate = {u for u, p in canon_elsewhere.items()
                           if origin(origin_map(p["canonical"])) == origin(origin_map(p["final_url"]))}
    orphans = [u for u in in_sitemap if u in indexable and not inlinks.get(u) and u != start]
    add("medium", "orphan", "in the sitemap, but no crawled page links to it", orphans)
    add("medium", "unreachable-from-start",
        "linked from other pages, but no chain of HTML links leads here from the start page",
        [u for u in indexable if u not in depth and u not in orphans and u not in same_site_duplicate])
    if in_sitemap:
        add("low", "missing-from-sitemap", "indexable pages the sitemap does not list",
            [u for u in indexable if u not in in_sitemap and u not in same_site_duplicate])
    add("low", "deep", "pages more than three clicks from the start page",
        [f"{u} (depth {depth[u]})" for u in indexable if (depth.get(u) or 0) > 3])
    for field, code, label in (("title", "duplicate-title", "titles"), ("meta_description", "duplicate-description", "meta descriptions")):
        groups = {}
        for u, p in indexable.items():
            # Variants that name another page as canonical are expected to repeat it.
            if p.get(field) and u not in same_site_duplicate:
                groups.setdefault(p[field].strip().lower(), []).append(u)
        add("medium", code, f"indexable pages sharing the same {label}",
            [f"\"{indexable[us[0]][field]}\": " + ", ".join(sorted(us)) for us in groups.values() if len(us) > 1])
    per_page = {
        "title-missing": ("high", "pages with no title"),
        "h1-missing": ("medium", "pages with no h1"),
        "description-missing": ("low", "pages with no meta description"),
        "jsonld-invalid": ("high", "pages with JSON-LD that does not parse"),
        "canonical-other-origin": ("medium", "pages whose canonical points to another origin"),
        "img-alt-missing": ("low", "pages with images missing alt"),
        "viewport-missing": ("medium", "pages with no viewport meta"),
    }
    for code, (severity, message) in per_page.items():
        add(severity, code, message, [u for u, p in html_ok.items() if any(i["code"] == code for i in p.get("issues", []))])
    add("info", "robots-blocked", "URLs robots.txt blocks for crawlers (not fetched)", blocked)
    googlebot_blocked = [u for u in in_sitemap if not robots.allowed(u, "googlebot")]
    add("high", "sitemap-blocked-googlebot", "sitemap URLs that robots.txt blocks for Googlebot", googlebot_blocked)

    findings.sort(key=lambda f: SEVERITY_ORDER[f["severity"]])
    return {
        "start": start,
        "pages_fetched": len(pages),
        "max_pages": max_pages,
        "truncated": truncated,
        "robots_txt": {"status": robots_res["status"], "sitemaps": robots.sitemaps,
                       "groups": [{"agents": a, "rules": [("allow " if al else "disallow ") + p for al, p in r]}
                                  for a, r in robots.groups]},
        "sitemap": {"files": sitemap["sitemaps"], "url_count": len(sitemap["urls"]),
                    "errors": sitemap["errors"], "truncated": sitemap["truncated"]},
        "findings": findings,
        "pages": [{k: p.get(k) for k in ("url", "status", "final_url", "title", "meta_description",
                                         "canonical", "indexable", "word_count")}
                  | {"depth": depth.get(u), "inlinks": len(inlinks.get(u, [])), "in_sitemap": u in in_sitemap,
                     "issues": [i["code"] for i in p.get("issues", [])]}
                  for u, p in sorted(pages.items())],
    }


# ------------------------------------------------------------------ output ---

def print_page(r):
    print(f"# Page audit: {r['url']}")
    chain = r.get("redirect_chain") or []
    if len(chain) > 1:
        print("Redirects: " + " → ".join(f"{u} [{s}]" for u, s in chain))
    print(f"Status: {r.get('status')}  Final URL: {r.get('final_url')}")
    if "title" not in r:
        for i in r.get("issues", []):
            print(f"- {i['severity'].upper()} {i['code']}: {i['message']}")
        return
    print(f"Title ({r['title_length']} chars): {r['title']!r}")
    print(f"Meta description: {r['meta_description']!r}")
    print(f"Indexable: {r['indexable']}  robots: {r['meta_robots']}  googlebot: {r['meta_googlebot']}  X-Robots-Tag: {r['x_robots_tag']}")
    print(f"Canonical: {r['canonical']}  lang: {r['lang']}  viewport: {r['viewport']}")
    if r["hreflang"]:
        print("hreflang: " + ", ".join(f"{h['hreflang']}={h['href']}" for h in r["hreflang"]))
    print("Headings:")
    for level, text in r["headings"][:40]:
        print(f"  {'  ' * (level - 1)}h{level} {text}")
    links = r["links"]
    print(f"Links: {links['internal']} internal, {links['external']} external, {links['nofollow']} nofollow, "
          f"{links['no_anchor_text']} without anchor text")
    imgs = r["images"]
    print(f"Images: {imgs['total']} total, {len(imgs['missing_alt'])} missing alt, {imgs['empty_alt']} empty alt (decorative), "
          f"{imgs['missing_dimensions']} without width/height")
    for idx, block in enumerate(r["jsonld"], 1):
        print(f"JSON-LD {idx}: " + (block["error"] or ", ".join(block["types"]) or "no @type"))
    if r["open_graph"]:
        print("Open Graph: " + ", ".join(sorted(r["open_graph"])))
    print(f"Words in HTML text: {r['word_count']}")
    print("Issues:" if r["issues"] else "Issues: none flagged")
    for i in r["issues"]:
        print(f"- {i['severity'].upper()} {i['code']}: {i['message']}")


def print_crawl(r):
    print(f"# Crawl: {r['start']}")
    for line in r.get("checked_locally", []):
        print(f"Checked locally: {line}")
    print(f"Pages fetched: {r['pages_fetched']} (limit {r['max_pages']}){' · TRUNCATED: more URLs were found than fetched' if r['truncated'] else ''}")
    rb = r["robots_txt"]
    print(f"robots.txt: status {rb['status']}; sitemaps declared: {', '.join(rb['sitemaps']) or 'none'}")
    sm = r["sitemap"]
    print(f"Sitemap: {sm['url_count']} URLs in {len(sm['files'])} file(s)" + (f"; errors: {'; '.join(sm['errors'])}" if sm["errors"] else ""))
    print()
    if not r["findings"]:
        print("No findings.")
    for f in r["findings"]:
        print(f"## {f['severity'].upper()} {f['code']} ({len(f['urls'])}): {f['message']}")
        for u in f["urls"][:25]:
            print(f"- {u}")
        if len(f["urls"]) > 25:
            print(f"- … {len(f['urls']) - 25} more (use --json)")
        print()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("page", help="audit one page (URL or local HTML file)")
    p.add_argument("target")
    p.add_argument("--base", help="URL a local file will be served at, for resolving links")
    p.add_argument("--map-origin", action="append", default=[], metavar="PROD=LOCAL")
    p.add_argument("--json", action="store_true")
    c = sub.add_parser("crawl", help="crawl one site politely and report site-level findings")
    c.add_argument("start")
    c.add_argument("--max-pages", type=int, default=200)
    c.add_argument("--delay", type=float, default=0.5, help="seconds between requests (default 0.5)")
    c.add_argument("--map-origin", action="append", default=[], metavar="PROD=LOCAL",
                   help="check a local build: rewrite production URLs (sitemap, canonicals, links) to a local server")
    c.add_argument("--json", action="store_true")
    s = sub.add_parser("sitemap", help="read a sitemap (or a site's sitemaps) and optionally check every URL")
    s.add_argument("target")
    s.add_argument("--check", action="store_true", help="fetch each URL and report status, redirects and noindex")
    s.add_argument("--max-urls", type=int, default=500)
    s.add_argument("--delay", type=float, default=0.5)
    s.add_argument("--map-origin", action="append", default=[], metavar="PROD=LOCAL")
    s.add_argument("--json", action="store_true")
    r = sub.add_parser("robots", help="show robots.txt rules and test paths for Googlebot and '*'")
    r.add_argument("site")
    r.add_argument("--path", action="append", default=[])
    r.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    omap = OriginMap(getattr(args, "map_origin", []))

    if args.cmd == "page":
        result = audit_page(args.target, args.base, omap)
        print(json.dumps(result, indent=2, ensure_ascii=False)) if args.json else print_page(result)
    elif args.cmd == "crawl":
        result = omap.to_production(crawl(args.start, args.max_pages, args.delay, omap))
        print(json.dumps(result, indent=2, ensure_ascii=False)) if args.json else print_crawl(result)
    elif args.cmd == "sitemap":
        target = args.target
        if not urllib.parse.urlsplit(target).path.lower().endswith((".xml", ".gz")):
            robots, _ = load_robots(target, omap)
            targets = discover_sitemaps(target, robots, omap)
        else:
            targets = [target]
        result = {"sitemaps": [], "urls": [], "errors": [], "truncated": False}
        for t in targets:
            part = read_sitemap(t, omap, max_urls=args.max_urls)
            for key in ("sitemaps", "urls", "errors"):
                result[key].extend(part[key])
            result["truncated"] |= part["truncated"]
        if args.check:
            for idx, entry in enumerate(result["urls"]):
                if idx:
                    time.sleep(args.delay)
                res = fetch(omap(entry["loc"]))
                entry["status"] = res["status"]
                entry["final_url"] = res["final_url"]
                robots_hdr = res["headers"].get("x-robots-tag", "")
                noindex = "noindex" in robots_hdr.lower()
                if res["status"] == 200 and "html" in res["headers"].get("content-type", "").lower():
                    page = analyze_html(decode(res["body"]), entry["loc"], 200, res["headers"], res["chain"], omap)
                    noindex = not page["indexable"]
                    entry["canonical"] = page["canonical"]
                entry["noindex"] = noindex
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"# Sitemap: {', '.join(targets)}")
            for f in result["sitemaps"]:
                print(f"- file {f['url']} [status {f['status']}]")
            print(f"URLs: {len(result['urls'])}{' (truncated)' if result['truncated'] else ''}; "
                  f"with lastmod: {sum(1 for u in result['urls'] if u['lastmod'])}")
            for e in result["errors"]:
                print(f"- ERROR {e}")
            for u in result["urls"][:50] if not args.check else result["urls"]:
                extra = ""
                if args.check:
                    flags = []
                    if u.get("status") != 200:
                        flags.append(f"status {u.get('status')}")
                    if normalize(u.get("final_url") or u["loc"]) != omap(u["loc"]):
                        flags.append(f"redirects to {u.get('final_url')}")
                    if u.get("noindex"):
                        flags.append("noindex")
                    if u.get("canonical") and omap(u["canonical"]) != omap(u["loc"]):
                        flags.append(f"canonical {u['canonical']}")
                    extra = "  ← " + "; ".join(flags) if flags else "  ok"
                print(f"- {u['loc']}{extra}")
    elif args.cmd == "robots":
        robots, res = load_robots(args.site)
        result = {"url": origin(args.site) + "/robots.txt", "status": res["status"], "sitemaps": robots.sitemaps,
                  "groups": [{"agents": a, "rules": [("allow " if al else "disallow ") + p for al, p in rl]}
                             for a, rl in robots.groups],
                  "paths": [{"path": p, "googlebot": robots.allowed(origin(args.site) + p, "googlebot"),
                             "all": robots.allowed(origin(args.site) + p, "*")} for p in args.path]}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"# robots.txt: {result['url']} [status {result['status']}]")
            if result["status"] != 200:
                print("No robots.txt served: crawlers treat every path as allowed (a 5xx can instead pause crawling).")
            for g in result["groups"]:
                print(f"- user-agent {', '.join(g['agents'])}: " + ("; ".join(g["rules"]) or "no rules"))
            print("Sitemaps: " + (", ".join(result["sitemaps"]) or "none declared"))
            for p in result["paths"]:
                print(f"- {p['path']}: Googlebot {'allowed' if p['googlebot'] else 'BLOCKED'}, "
                      f"* {'allowed' if p['all'] else 'BLOCKED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
