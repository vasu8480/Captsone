#!/usr/bin/env bash
# Capstone demo deploy: ./deploy.sh <env> <version>
set -euo pipefail
ENV="${1:?usage: deploy.sh <env> <version>}"
VERSION="${2:?usage: deploy.sh <env> <version>}"
BASE="./.state/$ENV"
mkdir -p "$BASE/releases/$VERSION"
if [ -L "$BASE/current" ]; then readlink "$BASE/current" > "$BASE/.previous"; fi
ln -sfn "releases/$VERSION" "$BASE/current"
echo "[$ENV] deployed $VERSION"
