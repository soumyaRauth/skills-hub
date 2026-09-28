#!/usr/bin/env bash
# Runs the activation suite with the standing instruction appended to every
# case's system prompt, without editing the cases. Arguments pass through to
# `claude plugin eval`, e.g.:
#   scripts/eval-with-instruction.sh --runs 1 --scaffold --allow-tools Write Edit --ablation none --no-publish
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$root/eval-instruction" # ponytail: must sit below the plugin for --eval-dir
rm -rf "$tmp"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp"
cp -R "$root/evals/activation" "$tmp/activation"

block="$(sed 's/^/    /' "$root/integrations/claude-code/CLAUDE.md")"
for f in "$tmp"/activation/*/case.yaml; do
  grep -q '^  append_system_prompt:' "$f" && { echo "already set: $f" >&2; exit 1; }
  BLOCK="$block" awk '{ print } /^execution:$/ { print "  append_system_prompt: |"; print ENVIRON["BLOCK"] }' "$f" > "$f.new"
  mv "$f.new" "$f"
done

out="$root/evals/results/$(date -u +%Y-%m-%dT%H-%M-%SZ)-instruction"
cd "$root"
claude plugin eval . --eval-dir eval-instruction --output-dir "$out" "$@"
