#!/usr/bin/env bash
# Stop hook for the project-knowledge skill: once LEARN_EVERY (default 5)
# commits land past the knowledge cursor, ask Claude to bring the knowledge up
# to date before it stops. Pure bash, git and grep, so it costs no tokens until
# it fires, and it fires at most once per HEAD.
#
# Opt-in per repository: it does nothing where .agents/knowledge/ is absent, so
# installing it globally never starts a full scan in a repo nobody asked about.
input=$(cat)
grep -q '"stop_hook_active": *true' <<<"$input" && exit 0
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
dir="$root/.agents/knowledge"
[ -d "$dir" ] || exit 0
head=$(git -C "$root" rev-parse HEAD 2>/dev/null) || exit 0
[ "$(cat "$dir/.learn-nagged" 2>/dev/null)" = "$head" ] && exit 0
last=$(grep -o '"last_learned_commit": *"[0-9a-f]*"' "$dir/.learn-state.json" 2>/dev/null | grep -o '[0-9a-f]\{40\}')
if [ -n "$last" ] && git -C "$root" cat-file -e "$last^{commit}" 2>/dev/null; then
  n=$(git -C "$root" rev-list --count "$last..HEAD")
  [ "$n" -lt "${LEARN_EVERY:-5}" ] && exit 0
  what="Project knowledge is $n commits behind HEAD. Run the project-knowledge skill now (incremental from .agents/knowledge/.learn-state.json)"
else
  what="Project knowledge has never been learned here. Run the project-knowledge skill now (first run)"
fi
echo "$head" > "$dir/.learn-nagged"
printf '{"decision":"block","reason":"%s, then give the user its few-line report."}\n' "$what"
