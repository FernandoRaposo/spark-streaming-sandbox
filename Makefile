PIP := .env/bin/pip
PYTHON := .env/bin/python
PYTEST := .env/bin/pytest
PYLINT := .env/bin/pylint
MYPY := .env/bin/mypy

MYPY_OPTIONS = --ignore-missing-imports
PYTEST_OPTIONS = -v
PYLINT_OPTIONS = --exit-zero

DOCKERFILE = Dockerfile
VERSION ?= master

# create virtual environment
.env:
	virtualenv .env -p python3

# install runtime dependencies, one at a time to avoid dependencies issues
install: .env
	$(PIP) install -r requirements.txt

# install dev dependencies along with runtime dependencies
develop: install
	$(PIP) install -r requirements-dev.txt

test: develop
	@echo "Running tests using pytest"
	$(PYTEST) $(PYTEST_OPTIONS) tests/*

	@echo "Checking types using mypy"
	$(MYPY) $(MYPY_OPTIONS) .

	@echo "Running linter"
	$(PYLINT) $(PYLINT_OPTIONS) *.py

docker-build: test
	docker build -f $(DOCKERFILE) -t schiphol_assessment:$(VERSION) .

run:
	@mkdir -p results
	docker run -it\
		--mount type=bind,source="$(shell pwd)"/results,target=/app/results \
		--entrypoint ./commands.sh \
		schiphol_assessment:master
