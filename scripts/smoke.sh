#!/usr/bin/env bash
# Capstone smoke test: ./smoke.sh <url>
# Exits non-zero on a non-2xx response so the workflow can trigger rollback.
set -euo pipefail
URL="${1:?usage: smoke.sh <url>}"
echo "Smoke testing $URL ..."
curl -fsS "$URL/health" >/dev/null
echo "Smoke test passed"
