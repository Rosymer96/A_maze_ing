SHELL  := /bin/bash

VENV   := .venv
PYTHON := $(shell pwd)/$(VENV)/bin/python3
PIP    := $(shell pwd)/$(VENV)/bin/pip
FLAKE8 := $(VENV)/bin/flake8
MYPY   := $(VENV)/bin/mypy

.PHONY: install run debug clean lint lint-strict build

install:
	@echo "Setting up virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	@$(PIP) install --upgrade pip > /dev/null 2>&1
	@$(PIP) install -e ".[dev]" > /dev/null 2>&1
	@echo "Done."

run:
	@clear
	@$(PYTHON) a_maze_ing.py $(filter-out $@, $(MAKECMDGOALS))

debug:
	@$(PYTHON) -m pdb a_maze_ing.py $(filter-out $@, $(MAKECMDGOALS))

%:
	@:

lint:
	@$(MYPY) . --exclude='\.venv' --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@$(FLAKE8) . --exclude=.venv,__pycache__

lint-strict:
	@$(MYPY) . --exclude='\.venv' --strict
	@$(FLAKE8) . --exclude=.venv,__pycache__

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .mypy_cache build *.egg-info

build:
	@$(PYTHON) -m build
	@cp dist/mazegen-1.0.0-py3-none-any.whl .
