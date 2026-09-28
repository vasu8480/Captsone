# Capstone Starter App

A practical CI/CD capstone: a tiny calculator API with enough runtime surface to test linting,
testing, container builds, release tagging, staged deployment, smoke checks, and rollback.

## Why this is a better capstone

- It has a real HTTP surface instead of only a Python module.
- It exposes release metadata, so tags and deployments are visible at runtime.
- It includes container, security, release, and deploy workflows people can inspect and extend.
- It stays small enough to finish in one sitting.

## API

- `/` returns service metadata and available endpoints.
- `/health` returns liveness information.
- `/ready` returns readiness information.
- `/operations` returns the supported calculator operations.
- `/calculate?op=add&a=2&b=3` performs a calculation.

## Local checks

```bash
cd starter-app
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python -m src.app
curl http://127.0.0.1:8000/
black --check src tests
flake8 src tests --max-line-length=100
pytest
```

## Docker

```bash
cd starter-app
docker build -t starter-app:local .
docker run --rm -p 8000:8000 starter-app:local
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/operations
curl "http://127.0.0.1:8000/calculate?op=add&a=2&b=3"
```

## Quick start commands

```bash
cd starter-app
make install
make test
make run
make docker-build
make docker-run
```

## What you build (see ../module-08-labs.md)

- `.github/actions/setup/action.yml` — composite setup action.
- `.github/workflows/ci.yml` — matrix tests + lint + cache.
- `.github/workflows/security.yml` — pip-audit + CodeQL.
- `.github/workflows/release.yml` — tag → artifact + Release.
- `.github/workflows/deploy.yml` — staging → approval → prod → smoke → rollback.
- Branch protection on `main` requiring the checks above.

## Scripts

- `scripts/deploy.sh <env> <version>` — demo deploy (symlink current → release).
- `scripts/rollback.sh` — restore previous release.
- `scripts/smoke.sh <url>` — health check (curl); non-2xx exits non-zero.

## Release and deploy flow

- Tagging `vX.Y.Z` triggers the release workflow.
- The release workflow creates a source archive and a Docker image tarball.
- The deploy workflow demonstrates `staging` then `production`, with smoke tests and rollback.
- The running service exposes `APP_VERSION` and `APP_ENV` so people can verify what is deployed.

## Files people can learn from

- `src/app.py` shows a minimal production-shaped HTTP service.
- `Dockerfile` shows versioned image metadata and runtime defaults.
- `.github/workflows/*.yml` covers CI, security, release, and deploy concerns.
- `scripts/*.sh` demonstrates deploy, smoke, and rollback automation.
