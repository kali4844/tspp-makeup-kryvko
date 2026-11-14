.PHONY: install lint test check

install:
	pip install -r requirements.txt

lint:
	ruff check .

test:
	python -m pytest -q

check: lint test
