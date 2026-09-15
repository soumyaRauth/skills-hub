#!/usr/bin/env bash
# Sourced by each case's scaffold.sh: copies one repository fixture into the
# empty eval workspace, so the agent under test sees a real project.
#   source "$(dirname "${BASH_SOURCE[0]}")/../fixture.sh" <skill>/<fixture>
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
src="$root/tests/fixtures/$1"
[ -d "$src" ] || { echo "fixture not found: $src" >&2; exit 1; }
cp -R "$src/." .
