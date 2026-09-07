#!/usr/bin/env bash
#
# Validates every standards registry shipped by a skill in this repository.
#
# A registry is any skills/*/registry/ directory containing registry.yaml. The
# schema lives in that file rather than in this script, so adding a category, a
# type, or an authority is a registry edit and not a code change.
#
# Checked: unique ids, required and unknown fields, enum membership, category
# matching its directory, ISO-8601 dates that are not in the future, official
# URLs on the publishing authority's own domains, control references that
# resolve, and verification sources present when an entry claims one.
#
# Not checked: whether a URL is reachable. That needs the network, and a
# validator that fails when a standards body reorganizes its site is a
# validator people switch off.
#
# Usage: ./scripts/validate-registry.sh
# Exit:  0 = all checks passed, 1 = at least one failure.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
  printf '  \033[2mskip\033[0m PyYAML unavailable; registry not validated\n'
  exit 0
fi

REGISTRIES=$(find skills -mindepth 3 -maxdepth 3 -name registry.yaml -path '*/registry/*' 2>/dev/null | sort)
if [ -z "$REGISTRIES" ]; then
  printf '  \033[2mskip\033[0m no standards registry found\n'
  exit 0
fi

python3 - $REGISTRIES <<'PY'
import datetime, os, re, sys
from urllib.parse import urlparse

import yaml

GREEN, RED, YELLOW, DIM, BOLD, OFF = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[1m", "\033[0m"
failures = warnings = 0

def ok(msg):   print(f"  {GREEN}ok{OFF}   {msg}")
def bad(msg):
    global failures
    failures += 1
    print(f"  {RED}FAIL{OFF} {msg}")
def warn(msg):
    global warnings
    warnings += 1
    print(f"  {YELLOW}warn{OFF} {msg}")

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH = re.compile(r"^\d{4}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+([.-][a-z0-9]+)*$")
TODAY = datetime.date.today()
STALE_DAYS = 365

def parse_date(value):
    if DATE.match(value):
        return datetime.date.fromisoformat(value)
    if MONTH.match(value):
        return datetime.date.fromisoformat(value + "-01")
    return None

for index_path in sys.argv[1:]:
    root = os.path.dirname(index_path)
    print(f"\n{BOLD}Registry: {root}{OFF}")

    try:
        index = yaml.safe_load(open(index_path))
    except yaml.YAMLError as exc:
        bad(f"{index_path} is not valid YAML: {exc}")
        continue

    missing = [k for k in ("categories", "types", "statuses", "authorities",
                           "required_fields", "repository_evidence_levels")
               if k not in index]
    if missing:
        bad(f"registry.yaml is missing: {', '.join(missing)}")
        continue
    ok("registry.yaml declares its own schema")

    categories = set(index["categories"])
    types = set(index["types"])
    statuses = set(index["statuses"])
    evidence_levels = set(index["repository_evidence_levels"])
    required = list(index["required_fields"])
    optional = set(index.get("optional_fields", []))
    allowed = set(required) | optional
    authorities = {a: set(d) for a, d in index["authorities"].items()}

    # -- controls --
    controls_path = os.path.join(root, "controls.yaml")
    control_ids = set()
    if not os.path.exists(controls_path):
        bad("controls.yaml is missing; findings have nothing to normalize against")
    else:
        controls = yaml.safe_load(open(controls_path)).get("controls", [])
        for c in controls:
            for field in ("id", "name", "question", "evidence"):
                if field not in c:
                    bad(f"control {c.get('id', '?')} is missing '{field}'")
            cid = c.get("id", "")
            if cid in control_ids:
                bad(f"duplicate control id: {cid}")
            if cid and not ID.match(cid):
                bad(f"control id is not kebab-case: {cid}")
            control_ids.add(cid)
        ok(f"{len(control_ids)} control(s), ids unique")

    # -- entries --
    seen_ids = {}
    entries = 0
    unverified = 0
    for category in sorted(os.listdir(root)):
        cat_dir = os.path.join(root, category)
        if not os.path.isdir(cat_dir):
            continue
        if category not in categories:
            bad(f"directory '{category}/' is not a category declared in registry.yaml")
            continue
        for name in sorted(os.listdir(cat_dir)):
            if not name.endswith((".yaml", ".yml")):
                continue
            path = os.path.join(cat_dir, name)
            entries += 1
            try:
                e = yaml.safe_load(open(path))
            except yaml.YAMLError as exc:
                bad(f"{path} is not valid YAML: {exc}")
                continue
            if not isinstance(e, dict):
                bad(f"{path} does not contain a mapping")
                continue

            for field in required:
                if field not in e or e[field] in (None, "", [], {}):
                    bad(f"{path} is missing required field '{field}'")
            for field in e:
                if field not in allowed:
                    bad(f"{path} has unknown field '{field}' — add it to "
                        f"optional_fields in registry.yaml if it is intended")

            eid = e.get("id", "")
            if eid:
                if not ID.match(eid):
                    bad(f"{path}: id '{eid}' is not kebab-case")
                if eid in seen_ids:
                    bad(f"duplicate id '{eid}' in {path} and {seen_ids[eid]}")
                seen_ids[eid] = path
                if os.path.splitext(name)[0] != eid:
                    warn(f"{path}: filename does not match id '{eid}'")

            if e.get("category") != category:
                bad(f"{path}: category '{e.get('category')}' does not match "
                    f"directory '{category}'")
            if e.get("type") not in types:
                bad(f"{path}: type '{e.get('type')}' is not declared in registry.yaml")
            if e.get("status") not in statuses:
                bad(f"{path}: status '{e.get('status')}' is not declared in registry.yaml")

            assessment = e.get("assessment") or {}
            if not isinstance(assessment, dict):
                bad(f"{path}: assessment must be a mapping")
            elif assessment.get("repository_evidence") not in evidence_levels:
                bad(f"{path}: assessment.repository_evidence "
                    f"'{assessment.get('repository_evidence')}' is not a declared level")

            authority = e.get("authority")
            domains = authorities.get(authority)
            if authority and domains is None:
                bad(f"{path}: authority '{authority}' has no domains in registry.yaml")
            url = e.get("official_url", "")
            if url:
                parsed = urlparse(url)
                if parsed.scheme != "https":
                    bad(f"{path}: official_url is not https")
                elif domains and not any(
                    parsed.hostname == d or (parsed.hostname or "").endswith("." + d)
                    for d in domains
                ):
                    bad(f"{path}: official_url host '{parsed.hostname}' is not a "
                        f"domain of {authority} — an official source must come from "
                        f"the body that publishes the standard")

            for field in ("last_verified", "publication_date"):
                value = e.get(field)
                if value is None:
                    continue
                parsed_date = parse_date(str(value))
                if parsed_date is None:
                    bad(f"{path}: {field} '{value}' is not YYYY-MM-DD or YYYY-MM")
                elif parsed_date > TODAY:
                    bad(f"{path}: {field} '{value}' is in the future")
                elif field == "last_verified" and (TODAY - parsed_date).days > STALE_DAYS:
                    warn(f"{path}: last_verified is {(TODAY - parsed_date).days} days "
                         f"old — re-check the version and status against {authority}")

            verification = e.get("verification") or {}
            method = verification.get("method") if isinstance(verification, dict) else None
            if method not in ("authoritative-source", "bundled-knowledge"):
                bad(f"{path}: verification.method must be 'authoritative-source' "
                    f"or 'bundled-knowledge'")
            elif method == "authoritative-source":
                src = verification.get("source", "")
                if not src.startswith("https://"):
                    bad(f"{path}: verification.method is authoritative-source but "
                        f"no https source URL is recorded")
                elif domains and not any(
                    (urlparse(src).hostname or "") == d
                    or (urlparse(src).hostname or "").endswith("." + d)
                    for d in domains
                ):
                    bad(f"{path}: verification.source is not on a domain of {authority}")
            else:
                unverified += 1

            refs = e.get("controls") or []
            if not isinstance(refs, list) or not refs:
                bad(f"{path}: controls must be a non-empty list")
            else:
                for c in refs:
                    if control_ids and c not in control_ids:
                        bad(f"{path}: control '{c}' does not exist in controls.yaml")

            for field in ("summary", "claim_boundary"):
                text = e.get(field)
                if isinstance(text, str) and len(text.strip()) < 40:
                    warn(f"{path}: {field} is very short; it is what keeps reports "
                         f"defensible")

    if entries:
        ok(f"{entries} standard entr{'y' if entries == 1 else 'ies'} across "
           f"{len(categories)} declared categor{'y' if len(categories) == 1 else 'ies'}")
        ok(f"{entries - unverified} verified against an authoritative source, "
           f"{unverified} carried from bundled knowledge")
    else:
        bad("registry contains no standard entries")

print()
if failures:
    print(f"{RED}{failures} registry check(s) failed{OFF} ({warnings} warning(s))")
    sys.exit(1)
print(f"{GREEN}Registry checks passed{OFF} ({warnings} warning(s))")
PY
