.PHONY: install build validate test lint check site-check census census-extensions audit-report audit-check pending-review source-fetch

install:
	python -m pip install -r requirements-dev.txt

build:
	python scripts/build_readme.py

census:
	python scripts/build_conference_census.py

census-extensions:
	python scripts/refresh_researchr_extensions.py

audit-report:
	python scripts/build_audit_report.py

audit-check:
	python scripts/validate_audit.py

pending-review:
	python scripts/update_pending_review.py

source-fetch:
	python scripts/fetch_iclr_sources.py $(SOURCE_ARGS)

validate:
	python scripts/validate.py

test:
	python -m pytest

lint:
	python -m ruff check scripts tests
	python -m ruff format --check scripts tests

check: validate
	python scripts/build_readme.py --check
	python scripts/check_links.py
	python scripts/validate_audit.py
	python -m pytest
	python -m ruff check scripts tests
	python -m ruff format --check scripts tests

site-check:
	npm --prefix website run lint
	npm --prefix website test
	npm --prefix website audit --omit=dev --audit-level=high
