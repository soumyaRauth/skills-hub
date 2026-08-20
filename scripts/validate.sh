#!/usr/bin/env bash
#
# Validates the structure and metadata of every skill in this repository.
#
# Skills are discovered automatically from skills/*/ — adding a new one requires
# no change here. Uses the `skills-ref` validator when it is available, and
# always runs the built-in checks so the script is useful without it.
#
# Usage: ./scripts/validate.sh
# Exit:  0 = all checks passed, 1 = at least one failure.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAILURES=0
WARNINGS=0

pass() { printf '  \033[32mok\033[0m   %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; FAILURES=$((FAILURES + 1)); }
warn() { printf '  \033[33mwarn\033[0m %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }
skip() { printf '  \033[2mskip\033[0m %s\n' "$1"; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

require_file() {
  if [ -f "$1" ]; then pass "$1"; else fail "missing file: $1"; fi
}

# ---------------------------------------------------------------- structure --

head_ "Repository structure"
for f in README.md CONTRIBUTING.md LICENSE CHANGELOG.md \
         scripts/validate.sh .github/workflows/validate.yml tests/README.md; do
  require_file "$f"
done

if [ -n "$(find .github/ISSUE_TEMPLATE -name '*.md' -print -quit 2>/dev/null)" ]; then
  pass ".github/ISSUE_TEMPLATE/ has at least one template"
else
  fail "no issue templates found in .github/ISSUE_TEMPLATE/"
fi

if grep -q 'npx skills add' README.md 2>/dev/null; then
  pass "top-level README documents installation"
else
  fail "top-level README is missing an 'npx skills add' installation command"
fi

# ------------------------------------------------------------------ skills --

SKILLS=()
while IFS= read -r d; do SKILLS+=("$(basename "$d")"); done \
  < <(find skills -mindepth 1 -maxdepth 1 -type d | sort)

if [ "${#SKILLS[@]}" -eq 0 ]; then
  head_ "Skills"
  fail "no skills found under skills/"
fi

for skill in "${SKILLS[@]}"; do
  dir="skills/$skill"
  skill_file="$dir/SKILL.md"

  head_ "Skill: $skill"
  require_file "$skill_file"
  require_file "$dir/README.md"

  # -- frontmatter --
  if [ -f "$skill_file" ]; then
    if [ "$(head -n 1 "$skill_file")" = "---" ]; then
      pass "opens with a frontmatter delimiter"
    else
      fail "$skill_file must start with '---' on line 1"
    fi

    fm_end=$(awk 'NR>1 && $0=="---" {print NR; exit}' "$skill_file")
    if [ -z "$fm_end" ]; then
      fail "frontmatter block is never closed with '---'"
    else
      frontmatter=$(awk -v end="$fm_end" 'NR>1 && NR<end' "$skill_file")
      name=$(printf '%s\n' "$frontmatter" | awk '/^name:/ {sub(/^name: */,""); print; exit}')
      description=$(printf '%s\n' "$frontmatter" | awk '/^description:/ {sub(/^description: */,""); print; exit}')

      if [ -z "$name" ]; then
        fail "frontmatter is missing a 'name' field"
      elif [ "$name" = "$skill" ]; then
        pass "name matches its directory: $name"
      else
        fail "name '$name' does not match directory '$skill'"
      fi

      if printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
        pass "name is valid kebab-case"
      else
        fail "name must be lowercase kebab-case: '$name'"
      fi

      if [ -z "$description" ]; then
        fail "frontmatter is missing a 'description' field"
      else
        desc_len=${#description}
        pass "description present (${desc_len} characters)"
        [ "$desc_len" -lt 40 ] && warn "description is very short; agents select skills by description"
        [ "$desc_len" -gt 1024 ] && fail "description is $desc_len characters; keep it under 1024"
        if printf '%s' "$description" | grep -qiE '\b(use when|use this|use before|use after)\b'; then
          pass "description states when to use the skill"
        else
          warn "description does not say when the skill applies"
        fi
      fi

      unknown=$(printf '%s\n' "$frontmatter" | grep -E '^[a-zA-Z-]+:' \
        | grep -vE '^(name|description|license|allowed-tools|metadata):' || true)
      if [ -z "$unknown" ]; then
        pass "no unexpected frontmatter keys"
      else
        warn "unexpected frontmatter keys: $(printf '%s' "$unknown" | tr '\n' ' ')"
      fi

      body_lines=$(awk -v end="$fm_end" 'NR>end && NF' "$skill_file" | wc -l | tr -d ' ')
      if [ "$body_lines" -gt 20 ]; then
        pass "skill body is non-empty ($body_lines non-blank lines)"
      else
        fail "skill body looks empty or truncated ($body_lines non-blank lines)"
      fi
    fi
  fi

  # -- references --
  if [ -d "$dir/references" ]; then
    ref_count=$(find "$dir/references" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
    if [ "$ref_count" -gt 0 ]; then
      pass "$ref_count reference document(s)"
    else
      fail "$dir/references/ contains no markdown files"
    fi

    orphans=0
    for ref in "$dir"/references/*.md; do
      [ -e "$ref" ] || continue
      base=$(basename "$ref")
      case "$base" in *.template.md) continue ;; esac
      if ! grep -qF "$base" "$skill_file" "$dir/README.md" 2>/dev/null; then
        fail "orphan reference: $ref is never linked from SKILL.md or the skill README"
        orphans=$((orphans + 1))
      fi
    done
    [ "$orphans" -eq 0 ] && pass "no orphan reference files"

    missing=0
    while IFS= read -r target; do
      [ -e "$dir/$target" ] && continue
      # A reference shipping a .template.md counterpart is opt-in (teams copy it
      # in), so SKILL.md may reference it conditionally without it existing.
      [ -e "$dir/${target%.md}.template.md" ] && continue
      fail "$skill_file points to a missing $target"
      missing=$((missing + 1))
    done < <(grep -oE 'references/[a-z0-9-]+\.md' "$skill_file" 2>/dev/null | sort -u)
    [ "$missing" -eq 0 ] && pass "every reference named in SKILL.md exists"
  else
    fail "missing directory: $dir/references"
  fi

  # -- examples --
  if [ -d "$dir/examples" ]; then
    ex_count=$(find "$dir/examples" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
    if [ "$ex_count" -ge 3 ]; then
      pass "$ex_count example(s)"
    else
      fail "expected at least 3 examples in $dir/examples, found $ex_count"
    fi
  else
    fail "missing directory: $dir/examples"
  fi

  # -- docs --
  if grep -q "npx skills add .* --skill $skill" "$dir/README.md" 2>/dev/null; then
    pass "skill README documents its install command"
  else
    fail "$dir/README.md is missing 'npx skills add ... --skill $skill'"
  fi

  if grep -q -- "--skill $skill" README.md 2>/dev/null; then
    pass "skill is listed in the top-level README"
  else
    warn "top-level README does not mention --skill $skill"
  fi

  # -- fixtures --
  if [ -d "tests/fixtures/$skill" ] && [ -n "$(find "tests/fixtures/$skill" -type f -print -quit)" ]; then
    fx=$(find "tests/fixtures/$skill" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    pass "$fx test fixture(s) under tests/fixtures/$skill"
  else
    warn "no test fixtures found at tests/fixtures/$skill"
  fi

  if grep -q "$skill" tests/README.md 2>/dev/null; then
    pass "documented in tests/README.md"
  else
    warn "tests/README.md does not mention $skill"
  fi
done

# ------------------------------------------------------------ link checking --

head_ "Internal markdown links"
broken=0
checked=0
while IFS= read -r md; do
  dir=$(dirname "$md")
  while IFS= read -r target; do
    [ -z "$target" ] && continue
    case "$target" in http://*|https://*|mailto:*|\#*) continue ;; esac
    target=${target%%#*}
    [ -z "$target" ] && continue
    checked=$((checked + 1))
    if [ ! -e "$dir/$target" ] && [ ! -e "$target" ]; then
      fail "broken link in $md -> $target"
      broken=$((broken + 1))
    fi
  done < <(grep -oE '\]\([^)]+\)' "$md" | sed -E 's/^\]\(//; s/\)$//' | sed -E 's/ +".*"$//')
done < <(find . -name '*.md' -not -path './node_modules/*' -not -path './.git/*')
[ "$broken" -eq 0 ] && pass "$checked relative link(s) resolve"

# ----------------------------------------------------------------- hygiene --

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

# Production Guard forbids invented scores; make sure the docs never model one.
score_hits=$(grep -rInE -B3 'Code quality: *[0-9]+%|Overall: *[0-9]+%|Security: *[0-9]+%' \
  skills/ 2>/dev/null \
  | awk -v RS='--\n' '!/never|Never|not |Not |avoid|Avoid|instead|Instead|prohibited|forbidden/ && /%/' || true)
if [ -z "$score_hits" ]; then
  pass "no invented quality scores in skill documentation"
else
  fail "invented score found in skill docs:"
  printf '%s\n' "$score_hits" | sed 's/^/       /'
fi

if [ -x scripts/validate.sh ]; then
  pass "scripts/validate.sh is executable"
else
  fail "scripts/validate.sh is not executable (chmod +x scripts/validate.sh)"
fi

# --------------------------------------------------------------- skills-ref --

head_ "External validator"
if command -v skills-ref >/dev/null 2>&1; then
  for skill in "${SKILLS[@]}"; do
    if skills-ref validate "skills/$skill"; then
      pass "skills-ref: $skill"
    else
      fail "skills-ref validation failed for $skill"
    fi
  done
else
  skip "skills-ref not installed; built-in checks used instead"
fi

# ----------------------------------------------------------------- summary ---

printf '\n'
if [ "$FAILURES" -eq 0 ]; then
  printf '\033[32mAll checks passed\033[0m — %d skill(s), %d warning(s)\n' "${#SKILLS[@]}" "$WARNINGS"
  exit 0
fi
printf '\033[31m%d check(s) failed\033[0m (%d warning(s))\n' "$FAILURES" "$WARNINGS"
exit 1
