USE_UVLOOP             ?= 0
PROTOCOL               ?= 2
CLUSTER_URL            ?= valkey://localhost:16379/0
ADDITIONAL_PYTEST_ARGS ?=

ifeq ($(USE_UVLOOP), 1)
	UVLOOP_ARG          := --uvloop
	UVLOOP_REPORT_INFIX := -uvloop
else
	UVLOOP_ARG          := --no-uvloop
endif

.PHONY: devenv stop-devenv build-docs linters standalone-tests cluster-tests all-tests clean package

all: help

help:
	@echo "Please use \"make <target>\" where <target> is one of"
	@echo "  clean            to clean the project and stop development environment"
	@echo "  devenv           to start development environment (requires docker-compose)"
	@echo "  stop-devenv      to stop development environment"
	@echo "  build-docs       to build the sphinx documentation"
	@echo "  docs             is an alias for build-docs"
	@echo "  linters          to run code linters"
	@echo "  standalone-tests to run standalone tests"
	@echo "  cluster-tests    to run cluster tests"
	@echo "  tests            to run standalone and cluster tests"
	@echo "  all-tests        to run all linters and tests"
	@echo "  package          to build the package"

.check-virtualenv:
ifndef VIRTUAL_ENV
	@echo "**************************************************************"
	@echo "*** WARNING: it is highliy recommended to use a virtualenv ***"
	@echo "**************************************************************"
endif

clean: stop-devenv
	rm -rf build
	rm -rf dist
	docker compose --profile all rm -s -f

devenv: clean
	docker compose --profile all up -d

stop-devenv:
	docker compose --profile all down

build-docs docs: .check-virtualenv
	pip install --group docs
	make -C docs html

linters: .check-virtualenv
	flake8 tests valkey
	black --target-version py37 --check --diff tests valkey
	isort --check-only --diff tests valkey
	vulture valkey whitelist.py --min-confidence 80
	flynt --fail-on-change --dry-run tests valkey

standalone-tests: .check-virtualenv
	pytest \
		--protocol=$(PROTOCOL) \
		--cov=./ \
		--cov-report=xml:coverage_valkey.xml \
		-W always \
		-m 'not onlycluster' \
		--junit-xml=standalone$(UVLOOP_REPORT_INFIX)-results.xml \
		$(UVLOOP_ARG) $(ADDITIONAL_PYTEST_ARGS)

cluster-tests: .check-virtualenv
	pytest \
		--protocol=$(PROTOCOL) \
		--cov=./ \
		--cov-report=xml:coverage_cluster.xml \
		-W always \
		-m 'not onlynoncluster and not valkeymod' \
		--valkey-url=$(CLUSTER_URL) \
		--junit-xml=cluster$(UVLOOP_REPORT_INFIX)-results.xml \
		$(UVLOOP_ARG) $(ADDITIONAL_PYTEST_ARGS)

package: .check-virtualenv
	hatchling build

tests: standalone-tests cluster-tests

all-tests: linters tests
