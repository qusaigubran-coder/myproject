install:
	pip install -e .
	pip install pytest ruff mypy pre-commit

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

check:
	ruff check .
	pytest
	mypy src
