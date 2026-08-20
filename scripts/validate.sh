#!/usr/bin/env bash
#
# Validates the structure and metadata of the skills in this repository.
#
# Uses the `skills-ref` validator when it is available, and always runs the
# built-in checks so the script is useful without it.
#
# Usage: ./scripts/validate.sh
# Exit:  0 = all checks passed, 1 = at least one failure.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SKILL_DIR="skills/impact-map"
SKILL_FILE="$SKILL_DIR/SKILL.md"

FAILURES=0
WARNINGS=0

pass() { printf '  \033[32mok\033[0m   %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; FAILURES=$((FAILURES + 1)); }
warn() { printf '  \033[33mwarn\033[0m %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

require_file() {
  if [ -f "$1" ]; then pass "$1"; else fail "missing file: $1"; fi
}

require_dir() {
  if [ -d "$1" ]; then pass "$1/"; else fail "missing directory: $1"; fi
}

# ---------------------------------------------------------------- structure --

head_ "Repository structure"
for f in README.md CONTRIBUTING.md LICENSE CHANGELOG.md \
         scripts/validate.sh .github/workflows/validate.yml \
         .github/ISSUE_TEMPLATE/new-skill.md tests/README.md; do
  require_file "$f"
done

head_ "Skill files"
require_file "$SKILL_FILE"
require_file "$SKILL_DIR/README.md"
for f in report-schema dependency-analysis hidden-coupling framework-detection; do
  require_file "$SKILL_DIR/references/$f.md"
done

head_ "Examples"
require_dir "$SKILL_DIR/examples"
if [ -d "$SKILL_DIR/examples" ]; then
  example_count=$(find "$SKILL_DIR/examples" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
  if [ "$example_count" -ge 4 ]; then
    pass "$example_count example(s) present (minimum 4)"
  else
    fail "expected at least 4 examples, found $example_count"
  fi
fi

head_ "Test fixtures"
for d in simple-node nextjs laravel mixed-architecture; do
  require_dir "tests/fixtures/$d"
  if [ -d "tests/fixtures/$d" ] && [ -z "$(find "tests/fixtures/$d" -type f -print -quit)" ]; then
    fail "fixture is empty: tests/fixtures/$d"
  fi
done

# -------------------------------------------------------------- frontmatter --

head_ "SKILL.md frontmatter"
if [ ! -f "$SKILL_FILE" ]; then
  fail "cannot validate frontmatter, $SKILL_FILE is missing"
else
  if [ "$(head -n 1 "$SKILL_FILE")" = "---" ]; then
    pass "opens with a frontmatter delimiter"
  else
    fail "$SKILL_FILE must start with '---' on line 1"
  fi

  fm_end=$(awk 'NR>1 && $0=="---" {print NR; exit}' "$SKILL_FILE")
  if [ -n "$fm_end" ]; then
    pass "frontmatter block is closed (line $fm_end)"
    frontmatter=$(awk -v end="$fm_end" 'NR>1 && NR<end' "$SKILL_FILE")

    name=$(printf '%s\n' "$frontmatter" | awk -F': *' '/^name:/ {sub(/^name: */,""); print; exit}')
    description=$(printf '%s\n' "$frontmatter" | awk '/^description:/ {sub(/^description: */,""); print; exit}')

    if [ -n "$name" ]; then
      pass "name: $name"
    else
      fail "frontmatter is missing a 'name' field"
    fi

    if [ "$name" = "impact-map" ]; then
      pass "name matches the expected skill name"
    else
      fail "expected name 'impact-map', found '${name:-<empty>}'"
    fi

    if [ "$name" = "$(basename "$SKILL_DIR")" ]; then
      pass "name matches its directory"
    else
      fail "name '$name' does not match directory '$(basename "$SKILL_DIR")'"
    fi

    if printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
      pass "name is valid kebab-case"
    else
      fail "name must be lowercase kebab-case: '$name'"
    fi

    if [ -n "$description" ]; then
      desc_len=${#description}
      pass "description present (${desc_len} characters)"
      if [ "$desc_len" -lt 40 ]; then
        warn "description is very short; agents select skills by description"
      fi
      if [ "$desc_len" -gt 1024 ]; then
        fail "description is $desc_len characters; keep it under 1024"
      fi
      if printf '%s' "$description" | grep -qiE '\b(use when|use this)\b'; then
        pass "description states when to use the skill"
      else
        warn "description does not say when the skill applies"
      fi
    else
      fail "frontmatter is missing a 'description' field"
    fi

    unknown=$(printf '%s\n' "$frontmatter" \
      | grep -E '^[a-zA-Z-]+:' \
      | grep -vE '^(name|description|license|allowed-tools|metadata):' || true)
    if [ -z "$unknown" ]; then
      pass "no unexpected frontmatter keys"
    else
      warn "unexpected frontmatter keys: $(printf '%s' "$unknown" | tr '\n' ' ')"
    fi

    body_lines=$(awk -v end="$fm_end" 'NR>end && NF' "$SKILL_FILE" | wc -l | tr -d ' ')
    if [ "$body_lines" -gt 20 ]; then
      pass "skill body is non-empty ($body_lines non-blank lines)"
    else
      fail "skill body looks empty or truncated ($body_lines non-blank lines)"
    fi
  else
    fail "frontmatter block is never closed with '---'"
  fi
fi

# --------------------------------------------------------------- doc checks --

head_ "Documentation"
if grep -q 'npx skills add' "$SKILL_DIR/README.md" 2>/dev/null; then
  pass "skill README documents installation"
else
  fail "skill README is missing an 'npx skills add' installation command"
fi

if grep -q 'npx skills add' README.md 2>/dev/null; then
  pass "top-level README documents installation"
else
  fail "top-level README is missing an 'npx skills add' installation command"
fi

for ref in report-schema dependency-analysis hidden-coupling framework-detection; do
  if grep -q "references/$ref.md" "$SKILL_FILE" 2>/dev/null; then
    pass "SKILL.md references references/$ref.md"
  else
    warn "SKILL.md never points to references/$ref.md"
  fi
done

# Every reference must be reachable, or it is dead weight the agent never loads.
orphans=0
for ref in "$SKILL_DIR"/references/*.md; do
  [ -e "$ref" ] || continue
  base=$(basename "$ref")
  case "$base" in *.template.md) continue ;; esac
  if ! grep -qF "$base" "$SKILL_FILE" "$SKILL_DIR/README.md" 2>/dev/null; then
    fail "orphan reference: $ref is never linked from SKILL.md or the skill README"
    orphans=$((orphans + 1))
  fi
done
[ "$orphans" -eq 0 ] && pass "no orphan reference files"

# ------------------------------------------------------------ link checking --

head_ "Internal markdown links"
broken=0
checked=0
while IFS= read -r md; do
  dir=$(dirname "$md")
  while IFS= read -r target; do
    [ -z "$target" ] && continue
    case "$target" in
      http://*|https://*|mailto:*|\#*) continue ;;
    esac
    target=${target%%#*}
    [ -z "$target" ] && continue
    checked=$((checked + 1))
    if [ ! -e "$dir/$target" ] && [ ! -e "$target" ]; then
      fail "broken link in $md -> $target"
      broken=$((broken + 1))
    fi
  done < <(grep -oE '\]\([^)]+\)' "$md" | sed -E 's/^\]\(//; s/\)$//' | sed -E 's/ +".*"$//')
done < <(find . -name '*.md' -not -path './node_modules/*' -not -path './.git/*')
if [ "$broken" -eq 0 ]; then
  pass "$checked relative link(s) resolve"
fi

# --------------------------------------------------------------- hygiene ----

head_ "Hygiene"
secret_hits=$(grep -rInE \
  -e 'AKIA[0-9A-Z]{16}' \
  -e 'BEGIN [A-Z ]*PRIVATE KEY' \
  -e 'ghp_[A-Za-z0-9]{30,}' \
  -e 'xox[baprs]-[A-Za-z0-9-]{10,}' \
  . --exclude-dir=.git --exclude=validate.sh 2>/dev/null || true)
if [ -z "$secret_hits" ]; then
  pass "no obvious secret patterns"
else
  fail "possible secret material found:"
  printf '%s\n' "$secret_hits" | sed 's/^/       /'
fi

path_hits=$(grep -rInE '(/home/[a-z]|/Users/[a-z]|C:\\\\Users)' \
  . --exclude-dir=.git --exclude=validate.sh 2>/dev/null || true)
if [ -z "$path_hits" ]; then
  pass "no hardcoded local paths"
else
  fail "hardcoded local path(s) found:"
  printf '%s\n' "$path_hits" | sed 's/^/       /'
fi

if [ -x scripts/validate.sh ]; then
  pass "scripts/validate.sh is executable"
else
  fail "scripts/validate.sh is not executable (chmod +x scripts/validate.sh)"
fi

# ------------------------------------------------------------- skills-ref ----

head_ "External validator"
if command -v skills-ref >/dev/null 2>&1; then
  if skills-ref validate "$SKILL_DIR"; then
    pass "skills-ref validation passed"
  else
    fail "skills-ref validation failed"
  fi
else
  printf '  \033[2mskip\033[0m skills-ref not installed; built-in checks used instead\n'
fi

# ----------------------------------------------------------------- summary ---

printf '\n'
if [ "$FAILURES" -eq 0 ]; then
  printf '\033[32mAll checks passed\033[0m (%d warning(s))\n' "$WARNINGS"
  exit 0
fi
printf '\033[31m%d check(s) failed\033[0m (%d warning(s))\n' "$FAILURES" "$WARNINGS"
exit 1
