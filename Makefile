.PHONY: install run debug clean lint lint-strict build

install:
	@pip install -e ".[dev]"

run:
	@clear
	@python3 a_maze_ing.py config.txt

debug:
	@python3 -m pdb a_maze_ing.py config.txt

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	@rm -rf .mypy_cache build *.egg-info

build: install
	@python3 -m build
	@cp dist/mazegen-1.0.0-py3-none-any.whl .