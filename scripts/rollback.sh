#!/usr/bin/env bash
# Capstone demo rollback: ./rollback.sh [env]  (default: production)
set -euo pipefail
ENV="${1:-production}"
BASE="./.state/$ENV"
if [ ! -f "$BASE/.previous" ]; then
  echo "[$ENV] no previous release to roll back to" >&2
  exit 1
fi
ln -sfn "$(cat "$BASE/.previous")" "$BASE/current"
echo "[$ENV] rolled back to $(cat "$BASE/.previous")"
