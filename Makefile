.PHONY: install build validate test lint check

install:
	python -m pip install -r requirements-dev.txt

build:
	python scripts/build_readme.py

validate:
	python scripts/validate.py

test:
	python -m pytest

lint:
	python -m ruff check scripts tests

check: validate
	python scripts/build_readme.py --check
	python -m pytest
	python -m ruff check scripts tests
