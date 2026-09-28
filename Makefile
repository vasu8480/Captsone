PYTHON ?= python

.PHONY: install lint test run docker-build docker-run smoke

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

lint:
	black --check src tests
	flake8 src tests --max-line-length=100

test:
	pytest -v

run:
	$(PYTHON) -m src.app

docker-build:
	docker build --build-arg VERSION=local -t starter-app:local .

docker-run:
	docker run --rm -p 8000:8000 -e APP_ENV=local-docker starter-app:local

smoke:
	./scripts/smoke.sh http://127.0.0.1:8000