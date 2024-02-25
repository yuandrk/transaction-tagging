.ONESHELL:

SHELL := /bin/bash
DATE_ID := $(shell date +"%y.%m.%d")
# Get package name from pwd
PACKAGE_NAME := $(shell basename $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
.DEFAULT_GOAL := help

# UPDATE ME
DOCKER_IMAGE = $(shell basename $(CURDIR))-$(shell git describe --tags --always)-$(ARCH)
REGISTRY ?= ghcr.io/yuandrk
MAIN_FILE = main.py
KUBERNETES_DIR = kubernetes
DOCS_DIR = docs/src
ARCH ?= amd64 

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef

define PRINT_HELP_PYSCRIPT
import re, sys

class Style:
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    WHITE = '\033[37m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'

print(f"{Style.BOLD}Please use `make <target>` where <target> is one of{Style.ENDC}")
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if line.startswith("# -------"):
		print(f"\n{Style.RED}{line}{Style.ENDC}")
	if match:
		target, help_msg = match.groups()
		if not target.startswith('--'):
			print(f"{Style.BOLD+Style.GREEN}{target:20}{Style.ENDC} - {help_msg}")
endef

export BROWSER_PYSCRIPT
export PRINT_HELP_PYSCRIPT
# See: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS
export PYTHONWARNINGS=ignore
BROWSER := $(PYTHON) -c "$$BROWSER_PYSCRIPT"


# If you want a specific Python interpreter define it as an envvar
# $ export PYTHON_ENV=
ifdef PYTHON_ENV
	PYTHON := $(PYTHON_ENV)
else
	PYTHON := python3
endif

#################################### Functions ###########################################
# Function to check if package is installed else install it.
define install-pkg-if-not-exist
	@for pkg in ${1} ${2} ${3}; do \
		if ! command -v "$${pkg}" >/dev/null 2>&1; then \
			echo "installing $${pkg}"; \
			$(PYTHON) -m pip install $${pkg}; \
		fi;\
	done
endef

# Function to create python virtualenv if it doesn't exist
define create-venv
	$(call install-pkg-if-not-exist,virtualenv)

	@if [ ! -d ".$(PACKAGE_NAME)_venv" ]; then \
		$(PYTHON) -m virtualenv ".$(PACKAGE_NAME)_venv" -p $(PYTHON) -q; \
		echo "\".$(PACKAGE_NAME)_venv\": Created successfully!"; \
	fi;
	@echo "Source virtual environment before tinkering"
	@echo "Manually run: \`source .$(PACKAGE_NAME)_venv/bin/activate\`"
endef

define add-gitignore
	PKGS=venv,python,JupyterNotebooks,SublimeText,VisualStudioCode,vagrant
	curl -sL https://www.gitignore.io/api/$${PKGS} > .gitignore
endef

help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# ------------------------------------ Boilerplate Code ----------------------------------
boilerplate:  ## Add simple 'README.md' and .gitignore
	@echo "# $(PACKAGE_NAME)" | sed 's/_/ /g' >> README.md
	@$(call add-gitignore)

# -------------------------------- Builds and Installations -----------------------------

# You can easily chain a number of targets
bootstrap: clean install-hooks dev docs ## Installs development packages, hooks and generate docs for development

build-image:  ## Build docker image from local Dockerfile.
	docker build  --build-arg ARCH=$(ARCH) -f Dockerfile --no-cache -t $(REGISTRY)/$(DOCKER_IMAGE) .

build-cached-image:  ## Build cached docker image from local Dockerfile.
	docker build  --build-arg ARCH=$(ARCH)  -f Dockerfile -t $(REGISTRY)/$(DOCKER_IMAGE) .

push-image:
	docker push $(REGISTRY)/$(DOCKER_IMAGE) 

dev-venv: venv ## Install the package in development mode including all dependencies inside a virtualenv (container).
	@$(PYTHON_VENV) -m pip install .[dev];
	echo -e "\n--------------------------------------------------------------------"
	echo -e "Usage:\nPlease run:\n\tsource .$(PACKAGE_NAME)_venv/bin/activate;"
	echo -e "\t$(PYTHON) -m pip install .[dev];"
	echo -e "Start developing..."

install: clean ## Check if package exist, if not install the package
	@$(PYTHON) -c "import $(PACKAGE_NAME)" >/dev/null 2>&1 || $(PYTHON) -m pip install .;

venv:  ## Create virtualenv environment on local directory.
	@$(create-venv)
	echo 
# ---------------------------------- Python Packaging ------------------------------------
dist: clean ## Builds source and wheel package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

# -------------------------------------- Project Execution -------------------------------
run-in-docker:  ## Run python app in a docker container
	docker run --rm -ti --volume "$(CURDIR)":/app $(DOCKER_IMAGE) \
	bash -c "$(PYTHON) $(MAIN_FILE)"

get-logs-container:  ## Get logs of running container
	docker logs -f $$(docker ps | grep $(DOCKER_IMAGE) | tr " " "\n" | tail -1)

run:  ## Run Python app
	$(PYTHON) $(MAIN_FILE)

# -------------------------------------- Deployment --------------------------------------
deploy-app:  ## Deploy App with Kubernetes manifests
	kubectl apply -f $(KUBERNETES_DIR)

pod-logs:  ## Get logs from all running pods on a defined namespace
	@if [ ! ${pod_namespace} ]; then \
		echo "Usage:"; \
		echo "$(MAKE) $@ pod_namespace=\"<namespace>\""; \
	else \
		for POD in $$(kubectl get pods -n ${pod_namespace} | cut -f 1 -d ' ' | grep ^[a-z]); do \
			echo '----------------------------------------'; \
			echo "-------- logs for $${POD} ---------------"; \
			echo '----------------------------------------'; \
			kubectl logs -n ${pod_namespace} $${POD}; \
		done; \
	fi;

port-forward:  ## Forward local ports to a pod in a namespace
	@if [ ! ${pod_namespace} ]; then \
		echo "Usage:"; \
		echo "$(MAKE) $@ pod_namespace=\"<namespace>\" ports=4111:3111"; \
	else \
		kubectl port-forward -n ${pod_namespace} $$(kubectl get pods -n ${pod_namespace} | cut -f 1 -d ' ' | grep ^[a-z]) ${ports}; \
	fi

pods-status:  ## Check running pods on sandbox namespace
	@if [ ! ${pod_namespace} ]; then \
		echo "Usage:"; \
		echo "$(MAKE) $@ pod_namespace=\"<namespace>\""; \
	else \
		kubectl get pods -o wide -n ${pod_namespace}; \
	fi

pods-services:  ## Check all running services on pods on sandbox namespace
	@if [ ! ${pod_namespace} ]; then \
		echo "Usage:"; \
		echo "$(MAKE) $@ pod_namespace=\"<namespace>\""; \
	else \
		kubectl get svc -o wide -n ${pod_namespace}; \
	fi

# -------------------------------------- Clean Up  --------------------------------------
.PHONY: clean
clean: clean-build clean-docs clean-pyc clean-test clean-docker ## Remove all build, test, coverage and Python artefacts

clean-build: ## Remove build artefacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	find . -name '*.xml' -exec rm -fr {} +

clean-docs: ## Remove docs/_build artefacts, except PDF and singlehtml
	# Do not delete <module>.pdf and singlehtml files ever, but can be overwritten.
	find docs/compiled_docs ! -name "$(PACKAGE_NAME).pdf" ! -name 'index.html' -type f -exec rm -rf {} +
	rm -rf docs/compiled_docs/doctrees
	rm -rf docs/compiled_docs/html
	rm -rf $(DOCS_DIR)/modules.rst
	rm -rf $(DOCS_DIR)/$(PACKAGE_NAME)*.rst
	rm -rf $(DOCS_DIR)/README.md

clean-pyc: ## Remove Python file artefacts
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Remove test and coverage artefacts
	rm -fr .$(PACKAGE_NAME)_venv
	rm -fr .tox/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-docker:  ## Remove docker image
	if docker images | grep $(DOCKER_IMAGE); then \
	 	docker rmi $(DOCKER_IMAGE) || true;\
	fi;

# -------------------------------------- Code Style  -------------------------------------

lint: ## Check style with `flake8` and `mypy`
	@$(PYTHON) -m flake8 --max-line-length 90 $(PACKAGE_NAME)
	# find . -name "*.py" | xargs pre-commit run -c .configs/.pre-commit-config.yaml flake8 --files
	# @$(PYTHON) -m mypy
	# @yamllint .

checkmake:  ## Check Makefile style with `checkmake`
	docker run --rm -v $(CURDIR):/data cytopia/checkmake Makefile

formatter: ## Format style with `black` and sort imports with `isort`
	$(call install-pkg-if-not-exist,black,isort)
	@isort -m 3 -tc -rc .
	@black -l 90 .
# 	find . -name "*.py" | xargs pre-commit run -c .configs/.pre-commit-config.yaml isort --files

#  ---------------------------------- Git Hooks ------------------------------------------

install-hooks: ## Install `pre-commit-hooks` on local directory [see: https://pre-commit.com]
	$(PYTHON) -m pip install pre-commit
	pre-commit install --install-hooks -c .configs/.pre-commit-config.yaml

pre-commit: ## Run `pre-commit` on all files
	pre-commit run --all-files -c .configs/.pre-commit-config.yaml

# ---------------------------------------- Tests -----------------------------------------
test: ## Run tests quickly with pytest
	$(PYTHON) -m pytest -sv
	# $(PYTHON) -m nose -sv

# ---------------------------------Test Coverage -----------------------------------------
coverage: ## Check code coverage quickly with pytest
	coverage run --source=$(PACKAGE_NAME) -m pytest -s .
	coverage xml
	coverage report -m
	coverage html

coveralls: ## Upload coverage report to coveralls.io
	coveralls --coveralls_yaml .coveralls.yml || true

view-coverage: ## View code coverage
	$(BROWSER) htmlcov/index.html

# ---------------------------- Changelog Generation ----------------------
changelog: ## Generate changelog for current repo
	docker run -it --rm -v "$(CURDIR)":/usr/local/src/your-app mmphego/git-changelog-generator

# ---------------------------- Documentation Generation ----------------------
.PHONY: --docs-depencencies
--docs-depencencies: ## Check if sphinx is installed, then generate Sphinx HTML documentation dependencies.
	$(call install-pkg-if-not-exist,sphinx-apidoc)
	sphinx-apidoc -o $(DOCS_DIR) $(PACKAGE_NAME)
	sphinx-autogen $(DOCS_DIR)/*.rst
	cp README.md $(DOCS_DIR)
	cp docs/CONTRIBUTING.md $(DOCS_DIR)
	sed -i 's/docs\///g' $(DOCS_DIR)/README.md


complete-docs: --docs-depencencies ## Generate a complete Sphinx HTML documentation, including API docs.
	$(MAKE) -C $(DOCS_DIR) html
	@echo "\n\nNote: Documentation located at: ";\
	echo "${PWD}/docs/compiled_docs/html/index.html";\

docs: --docs-depencencies ## Generate a single Sphinx HTML documentation, with limited API docs.
	$(MAKE) -C $(DOCS_DIR) singlehtml;
	mv docs/compiled_docs/singlehtml/index.html docs/compiled_docs/;
	rm -rf docs/compiled_docs/singlehtml;
	rm -rf docs/compiled_docs/doctrees;
	@echo "\n\nNote: Documentation located at: ";\
	echo "${PWD}/docs/compiled_docs/index.html";\

pdf-doc: --docs-depencencies ## Generate a Sphinx PDF documentation, with limited including API docs. (Optional)
	@if command -v latexmk >/dev/null 2>&1; then \
		$(MAKE) -C $(DOCS_DIR) latex; \
		if [ -d "docs/compiled_docs/latex" ]; then \
			$(MAKE) -C docs/compiled_docs/latex all-pdf LATEXMKOPTS=-quiet; \
			mv docs/compiled_docs/latex/$(PACKAGE_NAME).pdf docs; \
			rm -rf docs/compiled_docs/latex; \
			rm -rf docs/compiled_docs/doctrees; \
		fi; \
		echo "\n\nNote: Documentation located at: "; \
		echo "${PWD}/docs/$(PACKAGE_NAME).pdf"; \
	else \
		@echo "Note: Untested on WSL/MAC"; \
		@echo "  Please install the following packages in order to generate a PDF documentation.\n"; \
		@echo "  On Debian run:"; \
		@echo "    sudo apt install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk"; \
	fi \