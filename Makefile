export SHELL := /bin/bash

test:
	python -m pytest -n auto --cov=seaborn --cov=tests --cov-config=setup.cfg --timeout=60 tests

lint:
	python -m flake8 seaborn/ tests/

typecheck:
	python -m mypy --follow-imports=skip seaborn/_core seaborn/_marks seaborn/_stats
