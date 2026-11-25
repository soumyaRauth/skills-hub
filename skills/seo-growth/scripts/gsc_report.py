#!/usr/bin/env python3
"""Summarize a Google Search Console Performance export. Standard library only.

  gsc_report.py EXPORT [--compare PREVIOUS] [--brand "name,brand"] [--min-impressions N] [--json]

EXPORT is the unzipped folder Search Console produces (Performance → Export →
CSV: Queries.csv, Pages.csv, Dates.csv, ...), the .zip itself, or one CSV.
Localized exports: name the files with --queries, --pages and --dates.

It reports only what the export contains:
  - totals, from Dates.csv when present (query tables omit privacy-filtered queries)
  - brand and name queries versus the rest, by the terms you pass
  - queries and pages averaging positions 8-20 ("almost page one")
  - low CTR for position, measured against this site's own median CTR at a
    similar position, not against an industry curve
  - with --compare, or an export made in compare mode: gains, losses, new and lost rows
"""

import argparse
import csv
import io
import json
import os
import re
import statistics
import sys
import unicodedata
import zipfile

METRICS = ("clicks", "impressions", "ctr", "position")
PREVIOUS_WORDS = ("previous", "prior", "before", "earlier")
BANDS = ((1, 1.5, "1"), (1.5, 2.5, "2"), (2.5, 3.5, "3"), (3.5, 5.5, "4-5"), (5.5, 10.5, "6-10"),
         (10.5, 20.5, "11-20"), (20.5, 10 ** 6, "21+"))


# ----------------------------------------------------------------- reading ---

def _int(value):
    digits = re.sub(r"[^\d]", "", value or "")
    return int(digits) if digits else 0


def _float(value):
    v = (value or "").replace("%", "").replace(" ", "").strip()
    if not v:
        return None
    if "," in v and "." in v:
        v = v.replace(",", "")
    elif "," in v:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def _classify(name, header):
    low = name.lower()
    first = (header[0] if header else "").lower()
    for kind, words in (("queries", ("quer",)), ("pages", ("page",)), ("dates", ("date",)),
                        ("countries", ("countr",)), ("devices", ("device",))):
        if any(w in low for w in words) or any(w in first for w in words):
            return kind
    return None


def read_csv_text(text):
    rows = list(csv.reader(io.StringIO(text.lstrip("﻿"))))
    if not rows:
        return [], {}
    header, body = rows[0], rows[1:]
    cols = {}
    for idx, name in enumerate(header):
        low = name.strip().lower()
        for metric in METRICS:
            if low == metric or low.endswith(" " + metric):
                cols.setdefault(metric, []).append((idx, low))
    current, previous, assumed = {}, {}, False
    for metric, found in cols.items():
        prev = [i for i, n in found if any(w in n for w in PREVIOUS_WORDS)]
        cur = [i for i, n in found if i not in prev]
        if cur:
            current[metric] = cur[0]
        if prev:
            previous[metric] = prev[0]
        elif len(cur) >= 2:
            # Two periods and neither is named "previous": take the first as current, and say so.
            previous[metric] = cur[1]
            assumed = True

    def build(index):
        out = []
        for row in body:
            if not row or not row[0].strip():
                continue
            get = lambda m: row[index[m]] if m in index and index[m] < len(row) else ""
            clicks, impressions = _int(get("clicks")), _int(get("impressions"))
            ctr = clicks / impressions if impressions else 0.0
            out.append({"key": row[0].strip(), "clicks": clicks, "impressions": impressions,
                        "ctr": ctr, "position": _float(get("position"))})
        return out

    tables = {"current": build(current)}
    if previous and "impressions" in previous:
        tables["previous"] = build(previous)
        tables["assumed_order"] = assumed
    return header, tables


def load_export(path, explicit=None):
    """Return {kind: {"current": rows, "previous": rows?}} from a folder, a zip or one CSV."""
    explicit = explicit or {}
    sources = []
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            if name.lower().endswith(".csv"):
                with open(os.path.join(path, name), encoding="utf-8-sig", errors="replace") as handle:
                    sources.append((name, handle.read()))
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.lower().endswith(".csv"):
                    sources.append((os.path.basename(name), archive.read(name).decode("utf-8-sig", "replace")))
    elif os.path.isfile(path):
        with open(path, encoding="utf-8-sig", errors="replace") as handle:
            sources.append((os.path.basename(path), handle.read()))
    else:
        raise SystemExit(f"not found: {path}")
    data = {}
    for kind, file in explicit.items():
        if file:
            with open(file, encoding="utf-8-sig", errors="replace") as handle:
                data[kind] = read_csv_text(handle.read())[1]
    for name, text in sources:
        header, tables = read_csv_text(text)
        kind = _classify(name, header)
        if kind and kind not in data and tables.get("current") is not None:
            data[kind] = tables
    if not data:
        raise SystemExit(f"no Search Console tables recognized in {path}; name them with --queries/--pages/--dates")
    return data


# ---------------------------------------------------------------- analysis ---

def _fold(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def totals(rows):
    clicks = sum(r["clicks"] for r in rows)
    impressions = sum(r["impressions"] for r in rows)
    weighted = [(r["position"], r["impressions"]) for r in rows if r["position"] is not None and r["impressions"]]
    position = (sum(p * i for p, i in weighted) / sum(i for _, i in weighted)) if weighted else None
    return {"clicks": clicks, "impressions": impressions,
            "ctr": clicks / impressions if impressions else None,
            "position": round(position, 1) if position is not None else None, "rows": len(rows)}


def band(position):
    if position is None:
        return None
    for low, high, label in BANDS:
        if low <= position < high:
            return label
    return None


def low_ctr(rows, min_impressions, ratio, min_rows=5):
    eligible = [r for r in rows if r["impressions"] >= min_impressions and r["position"] is not None and r["position"] <= 10.5]
    medians = {}
    for label in {band(r["position"]) for r in eligible}:
        ctrs = [r["ctr"] for r in eligible if band(r["position"]) == label]
        if len(ctrs) >= min_rows:
            medians[label] = statistics.median(ctrs)
    flagged = [dict(r, band=band(r["position"]), band_median_ctr=medians[band(r["position"])])
               for r in eligible if band(r["position"]) in medians
               and r["ctr"] < ratio * medians[band(r["position"])]]
    return sorted(flagged, key=lambda r: -r["impressions"]), medians


def compare(current, previous, min_impressions, top):
    prev = {r["key"]: r for r in previous}
    cur = {r["key"]: r for r in current}
    changes = []
    for key in set(cur) | set(prev):
        a, b = cur.get(key), prev.get(key)
        changes.append({"key": key,
                        "clicks": (a or {}).get("clicks", 0), "clicks_before": (b or {}).get("clicks", 0),
                        "impressions": (a or {}).get("impressions", 0),
                        "impressions_before": (b or {}).get("impressions", 0),
                        "position": (a or {}).get("position"), "position_before": (b or {}).get("position")})
    for c in changes:
        c["clicks_delta"] = c["clicks"] - c["clicks_before"]
        c["impressions_delta"] = c["impressions"] - c["impressions_before"]
    return {
        "gains": sorted([c for c in changes if c["impressions_delta"] > 0], key=lambda c: (-c["impressions_delta"], c["key"]))[:top],
        "losses": sorted([c for c in changes if c["impressions_delta"] < 0], key=lambda c: (c["impressions_delta"], c["key"]))[:top],
        "new": sorted([c for c in changes if c["impressions_before"] == 0 and c["impressions"] >= min_impressions],
                      key=lambda c: -c["impressions"])[:top],
        "lost": sorted([c for c in changes if c["impressions"] == 0 and c["impressions_before"] >= min_impressions],
                       key=lambda c: -c["impressions_before"])[:top],
    }


def report(data, previous_data, brand_terms, min_impressions, top, ratio):
    out = {"min_impressions": min_impressions, "notes": []}
    queries = data.get("queries", {}).get("current", [])
    pages = data.get("pages", {}).get("current", [])
    if "dates" in data:
        out["totals"] = dict(totals(data["dates"]["current"]), source="Dates.csv")
    elif pages:
        out["totals"] = dict(totals(pages), source="Pages.csv")
        out["notes"].append("No Dates.csv: totals come from the pages table and may differ from the chart.")
    elif queries:
        out["totals"] = dict(totals(queries), source="Queries.csv")
        out["notes"].append("Totals from the query table undercount: privacy-filtered queries are omitted.")
    if queries:
        q_total = totals(queries)
        if out.get("totals") and out["totals"]["source"] != "Queries.csv" and out["totals"]["clicks"]:
            out["notes"].append(f"Query rows account for {q_total['clicks']} of {out['totals']['clicks']} clicks; "
                                "the rest are queries Search Console does not show.")
        if brand_terms:
            terms = [_fold(t.strip()) for t in brand_terms if t.strip()]
            is_brand = lambda r: any(t in _fold(r["key"]) for t in terms)
            out["brand"] = {"terms": brand_terms,
                            "brand": totals([r for r in queries if is_brand(r)]),
                            "non_brand": totals([r for r in queries if not is_brand(r)])}
        out["top_queries"] = sorted(queries, key=lambda r: -r["impressions"])[:top]
    for kind, rows in (("queries", queries), ("pages", pages)):
        if not rows:
            continue
        out[f"almost_page_one_{kind}"] = sorted(
            [r for r in rows if r["impressions"] >= min_impressions and r["position"] is not None and 7.5 <= r["position"] <= 20.5],
            key=lambda r: -r["impressions"])[:top]
        flagged, medians = low_ctr(rows, min_impressions, ratio)
        out[f"low_ctr_{kind}"] = flagged[:top]
        out[f"ctr_medians_{kind}"] = medians
    if pages:
        out["top_pages"] = sorted(pages, key=lambda r: -r["impressions"])[:top]
    if any(t.get("assumed_order") for t in data.values()):
        out["notes"].append("The export holds two periods with no column named 'previous': "
                            "the first column set is treated as the current period. Check the headers.")
    comparisons = {}
    for kind in ("queries", "pages"):
        prev_rows = None
        if previous_data and kind in previous_data:
            prev_rows = previous_data[kind]["current"]
        elif kind in data and "previous" in data[kind]:
            prev_rows = data[kind]["previous"]
        if prev_rows is not None and kind in data:
            comparisons[kind] = compare(data[kind]["current"], prev_rows, min_impressions, top)
    if comparisons:
        out["comparison"] = comparisons
        if previous_data and "dates" in previous_data:
            out["previous_totals"] = dict(totals(previous_data["dates"]["current"]), source="previous Dates.csv")
        elif "dates" in data and "previous" in data["dates"]:
            out["previous_totals"] = dict(totals(data["dates"]["previous"]), source="Dates.csv, previous columns")
    return out


# ------------------------------------------------------------------ output ---

def _pct(x):
    return "—" if x is None else f"{x * 100:.1f}%"


def _row(r):
    pos = "—" if r.get("position") is None else f"{r['position']:.1f}"
    return f"{r['key']} · {r['impressions']} impr · {r['clicks']} clicks · CTR {_pct(r['ctr'])} · pos {pos}"


def print_report(out, ratio):
    t = out.get("totals")
    if t:
        print(f"# Search Console export ({t['source']})")
        print(f"Clicks {t['clicks']} · Impressions {t['impressions']} · CTR {_pct(t['ctr'])} · "
              f"Avg position {t['position'] if t['position'] is not None else '—'}")
    pt = out.get("previous_totals")
    if pt:
        print(f"Previous period ({pt['source']}): Clicks {pt['clicks']} · Impressions {pt['impressions']} · "
              f"CTR {_pct(pt['ctr'])} · Avg position {pt['position'] if pt['position'] is not None else '—'}")
    for note in out["notes"]:
        print(f"Note: {note}")
    if "brand" in out:
        b = out["brand"]
        print(f"\n## Brand and name queries ({', '.join(b['terms'])})")
        for label, g in (("Brand", b["brand"]), ("Non-brand", b["non_brand"])):
            print(f"{label}: {g['clicks']} clicks, {g['impressions']} impressions, "
                  f"{g['rows']} {'query' if g['rows'] == 1 else 'queries'}")
    for kind in ("queries", "pages"):
        rows = out.get(f"almost_page_one_{kind}")
        if rows is not None:
            print(f"\n## Almost page one: {kind} averaging positions 8-20, at least {out['min_impressions']} impressions")
            print("\n".join(f"- {_row(r)}" for r in rows) or "- none")
        rows = out.get(f"low_ctr_{kind}")
        if rows is not None:
            medians = out[f"ctr_medians_{kind}"]
            print(f"\n## Low CTR for position: {kind} below {ratio:g} × this site's median CTR in the same position band")
            if not medians:
                print("- not enough rows per position band to compare (needs 5 or more with enough impressions)")
            else:
                print("Site medians: " + ", ".join(f"pos {k}: {_pct(v)}" for k, v in sorted(medians.items())))
                print("\n".join(f"- {_row(r)} (band median {_pct(r['band_median_ctr'])})" for r in rows) or "- none")
    for kind, comp in out.get("comparison", {}).items():
        print(f"\n## Changes in {kind} against the previous period")
        for label in ("gains", "losses"):
            print(f"{label.capitalize()} (by impressions):")
            print("\n".join(f"- {c['key']}: {c['impressions_before']} → {c['impressions']} impr, "
                            f"{c['clicks_before']} → {c['clicks']} clicks" for c in comp[label]) or "- none")
        print("New: " + (", ".join(c["key"] for c in comp["new"]) or "none"))
        print("Lost: " + (", ".join(c["key"] for c in comp["lost"]) or "none"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export")
    ap.add_argument("--compare", help="an export for the previous period, same form")
    ap.add_argument("--brand", default="", help="comma-separated brand and name terms")
    ap.add_argument("--min-impressions", type=int, default=10)
    ap.add_argument("--ctr-ratio", type=float, default=0.5, help="flag CTR below this × the site's median for the band")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--queries")
    ap.add_argument("--pages")
    ap.add_argument("--dates")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    explicit = {"queries": args.queries, "pages": args.pages, "dates": args.dates}
    data = load_export(args.export, explicit)
    previous = load_export(args.compare) if args.compare else None
    brand = [t for t in args.brand.split(",") if t.strip()]
    out = report(data, previous, brand, args.min_impressions, args.top, args.ctr_ratio)
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print_report(out, args.ctr_ratio)
    return 0


if __name__ == "__main__":
    sys.exit(main())
