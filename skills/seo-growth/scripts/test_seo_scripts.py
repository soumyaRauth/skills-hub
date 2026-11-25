#!/usr/bin/env python3
"""Self-check for seo_audit.py and gsc_report.py. Standard library only, no network:
it serves a small site with planted problems from a local HTTP server.

  python3 test_seo_scripts.py
"""

import contextlib
import gzip
import http.server
import io
import os
import sys
import tempfile
import threading
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsc_report  # noqa: E402
import seo_audit  # noqa: E402

PROD = "https://site.example"

PAGES = {
    "index.html": """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>Home</title>
<link rel="canonical" href="https://site.example/"></head><body>
<h1>Jane Example</h1><p>Data engineer.</p>
<a href="/about.html">About</a> <a href="/blog/">Blog</a> <a href="/old">Old link</a>
<a href="/private/x.html">Private</a> <img src="me.jpg">
</body></html>""",
    "about.html": """<!doctype html><html lang="en"><head><title>About Jane</title>
<meta name="robots" content="noindex, follow"><meta name="description" content="About Jane.">
<link rel="canonical" href="https://site.example/about.html"></head><body><h1>About</h1>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Person", "name": "Jane",}</script>
<a href="/">Home</a></body></html>""",
    "blog/index.html": """<!doctype html><html lang="en"><head><title>Blog</title>
<meta name="description" content="Posts."><link rel="canonical" href="https://site.example/blog/"></head>
<body><h1>Blog</h1><a href="/blog/post.html">Post</a> <a href="/blog/missing.html">Missing</a></body></html>""",
    "blog/post.html": """<!doctype html><html lang="en"><head><title>Blog</title>
<meta name="description" content="Posts."><link rel="canonical" href="http://www.site.example/blog/post.html">
<script type="application/ld+json">{"@context": "https://schema.org", "@graph": [{"@type": "BlogPosting"}, {"@type": "BreadcrumbList"}]}</script>
</head><body><h1>Post</h1><p>Text.</p></body></html>""",
    "new.html": """<!doctype html><html lang="en"><head><title>New</title>
<link rel="canonical" href="https://site.example/new.html"></head><body><h1>New</h1></body></html>""",
    "orphan.html": """<!doctype html><html lang="en"><head><title>Talks</title>
<link rel="canonical" href="https://site.example/orphan.html"></head><body><h1>Talks</h1>
<a href="/seed-child.html">Slides</a></body></html>""",
    "seed-child.html": """<!doctype html><html lang="en"><head><title>Slides</title>
<link rel="canonical" href="https://site.example/seed-child.html"></head><body><h1>Slides</h1></body></html>""",
    "private/x.html": "<html><head><title>Private</title></head><body>secret</body></html>",
    "robots.txt": "User-agent: *\nDisallow: /private/\n\nUser-agent: Googlebot\nDisallow: /orphan.html$\n\n"
                  "Sitemap: https://site.example/sitemap_index.xml\n",
}
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://site.example/</loc><lastmod>2026-11-01</lastmod></url>
<url><loc>https://site.example/about.html</loc></url>
<url><loc>https://site.example/orphan.html</loc></url>
<url><loc>https://site.example/old</loc></url>
</urlset>"""
INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap><loc>https://site.example/sitemap-pages.xml.gz</loc></sitemap>
</sitemapindex>"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        redirects = {"/old": "/old2", "/old2": "/new.html"}
        if self.path in redirects:
            self.send_response(301)
            self.send_header("Location", redirects[self.path])
            self.end_headers()
            return
        if self.path == "/sitemap-pages.xml.gz":
            body = gzip.compress(SITEMAP.encode())
            self.send_response(200)
            self.send_header("Content-Type", "application/gzip")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/sitemap_index.xml":
            body = INDEX.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/header-noindex.html":
            body = b"<html><head><title>H</title></head><body><h1>H</h1></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("X-Robots-Tag", "noindex")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        for rel, text in PAGES.items():
            path = os.path.join(cls.tmp.name, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as handle:
                handle.write(text)
        handler = lambda *a, **k: Handler(*a, directory=cls.tmp.name, **k)
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.local = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.omap = seo_audit.OriginMap([f"{PROD}={cls.local}"])

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def codes(self, result):
        return {i["code"] for i in result["issues"]}

    def test_page_facts_and_issues(self):
        r = seo_audit.audit_page(self.local + "/about.html", origin_map=self.omap)
        self.assertEqual(r["title"], "About Jane")
        self.assertFalse(r["indexable"])
        self.assertIn("noindex", self.codes(r))
        self.assertIn("jsonld-invalid", self.codes(r))
        self.assertNotIn("canonical-other-origin", self.codes(r))
        home = seo_audit.audit_page(self.local + "/", origin_map=self.omap)
        self.assertEqual(home["h1"], ["Jane Example"])
        self.assertEqual(len(home["images"]["missing_alt"]), 1)
        self.assertIn("description-missing", self.codes(home))
        self.assertEqual(home["links"]["internal"], 4)

    def test_header_noindex_and_jsonld_graph(self):
        r = seo_audit.audit_page(self.local + "/header-noindex.html")
        self.assertFalse(r["indexable"])
        self.assertIn("X-Robots-Tag", next(i["message"] for i in r["issues"] if i["code"] == "noindex"))
        post = seo_audit.audit_page(self.local + "/blog/post.html", origin_map=self.omap)
        self.assertEqual(post["jsonld"][0]["types"], ["BlogPosting", "BreadcrumbList"])
        self.assertIn("canonical-other-origin", self.codes(post))

    def test_redirect_chain(self):
        r = seo_audit.audit_page(self.local + "/old")
        self.assertEqual([s for _, s in r["redirect_chain"]], [301, 301, 200])
        self.assertIn("redirect-chain", self.codes(r))

    def test_local_file(self):
        path = os.path.join(self.tmp.name, "about.html")
        r = seo_audit.audit_page(path, base=PROD + "/about.html")
        self.assertEqual(r["status"], 200)
        self.assertIn("noindex", self.codes(r))

    def test_crawl_findings(self):
        with contextlib.redirect_stdout(io.StringIO()):
            r = seo_audit.crawl(PROD + "/", max_pages=50, delay=0, origin_map=self.omap)
        found = {f["code"]: f["urls"] for f in r["findings"]}
        self.assertTrue(any("/blog/missing.html [404]" in u and "/blog/" in u for u in found["broken-internal"]))
        self.assertTrue(any(u.endswith("/about.html") for u in found["sitemap-noindex"]))
        self.assertTrue(any(u.endswith("/orphan.html") for u in found["orphan"]))
        # Reached only through a sitemap page: it has an inlink, so it is not an orphan,
        # but no link path leads to it from the start page.
        self.assertFalse(any(u.endswith("/seed-child.html") for u in found["orphan"]))
        self.assertTrue(any(u.endswith("/seed-child.html") for u in found["unreachable-from-start"]))
        self.assertTrue(any("/old" in u for u in found["internal-link-to-redirect"]))
        self.assertTrue(any("/old" in u for u in found["sitemap-not-200"]))
        self.assertIn("redirect-chain", found)
        self.assertTrue(any('"blog"' in u.lower() for u in found["duplicate-title"]))
        self.assertTrue(any(u.endswith("/private/x.html") for u in found["robots-blocked"]))
        self.assertTrue(any(u.endswith("/orphan.html") for u in found["sitemap-blocked-googlebot"]))
        self.assertTrue(any("post.html" in u for u in found["canonical-other-origin"]))
        self.assertNotIn(self.local + "/private/x.html", {p["url"] for p in r["pages"]})
        self.assertEqual(r["sitemap"]["url_count"], 4)


class RobotsTests(unittest.TestCase):
    def test_rfc9309_matching(self):
        robots = seo_audit.Robots(
            "User-agent: *\nDisallow: /private\nAllow: /private/public\nDisallow: /*.pdf$\n"
            "User-agent: Googlebot\nUser-agent: bingbot\nDisallow: /nogoogle/\nAllow: /p\nDisallow: /p\n")
        allowed = lambda path, ua="*": robots.allowed("https://x.example" + path, ua)
        self.assertFalse(allowed("/private/a"))
        self.assertTrue(allowed("/private/public/a"))
        self.assertFalse(allowed("/files/a.pdf"))
        self.assertTrue(allowed("/files/a.pdf?x=1"))
        self.assertTrue(allowed("/private/a", "googlebot"))       # its own group replaces '*'
        self.assertFalse(allowed("/nogoogle/x", "Googlebot"))
        self.assertFalse(allowed("/nogoogle/x", "bingbot"))       # grouped user agents share rules
        self.assertTrue(allowed("/p", "googlebot"))               # allow wins a tie
        self.assertTrue(allowed("/robots.txt", "googlebot"))


class GscTests(unittest.TestCase):
    QUERIES = ("Top queries,Clicks,Impressions,CTR,Position\n"
               "jane example,40,100,40%,1.2\n"
               "jane example engineer,2,60,3.33%,1.4\n"
               "airflow retries,2,400,0.5%,9.4\n"
               "airflow sensors,0,30,0%,15\n"
               + "".join(f"topic {i},{10 + i},100,{10 + i}%,1.3\n" for i in range(5)))
    PREVIOUS = ("Top queries,Clicks,Impressions,CTR,Position\n"
                "jane example,30,90,33.3%,1.5\n"
                "old query,3,50,6%,8\n")
    DATES = "Date,Clicks,Impressions,CTR,Position\n2026-11-01,60,500,12%,4.1\n2026-11-02,64,590,10.8%,3.9\n"

    def write(self, folder, files):
        os.makedirs(folder, exist_ok=True)
        for name, text in files.items():
            with open(os.path.join(folder, name), "w") as handle:
                handle.write(text)

    def test_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            cur, prev = os.path.join(tmp, "cur"), os.path.join(tmp, "prev")
            self.write(cur, {"Queries.csv": self.QUERIES, "Dates.csv": self.DATES})
            self.write(prev, {"Queries.csv": self.PREVIOUS})
            out = gsc_report.report(gsc_report.load_export(cur), gsc_report.load_export(prev),
                                    ["Jane Example"], 20, 10, 0.5)
        self.assertEqual(out["totals"]["clicks"], 124)
        self.assertEqual(out["totals"]["source"], "Dates.csv")
        self.assertEqual(out["brand"]["brand"]["rows"], 2)
        self.assertEqual(out["brand"]["brand"]["clicks"], 42)
        self.assertEqual([r["key"] for r in out["almost_page_one_queries"]], ["airflow retries", "airflow sensors"])
        self.assertIn("jane example engineer", [r["key"] for r in out["low_ctr_queries"]])
        comp = out["comparison"]["queries"]
        self.assertIn("airflow retries", [c["key"] for c in comp["new"]])
        self.assertIn("old query", [c["key"] for c in comp["lost"]])

    def test_compare_mode_columns_and_locale_numbers(self):
        text = ("Top queries,Last 28 days Clicks,Previous 28 days Clicks,Last 28 days Impressions,"
                "Previous 28 days Impressions,Last 28 days CTR,Previous 28 days CTR,"
                "Last 28 days Position,Previous 28 days Position\n"
                "jane,\"1,200\",900,\"4,000\",\"3,000\",\"30,0%\",30%,\"1,5\",1.6\n")
        _, tables = gsc_report.read_csv_text(text)
        self.assertEqual(tables["current"][0]["clicks"], 1200)
        self.assertEqual(tables["previous"][0]["impressions"], 3000)
        self.assertAlmostEqual(tables["current"][0]["position"], 1.5)
        self.assertFalse(tables["assumed_order"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
