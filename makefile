.PHONY: all clean install dev-install format lint test coverage build publish help

PYTHON := python3
PACKAGE := centralized_rate_limiter

help:
	@echo "Available commands:"
	@echo "  make install      - Install package for production"
	@echo "  make dev-install  - Install package with development dependencies"
	@echo "  make format       - Format code using black and isort"
	@echo "  make lint         - Run code quality checks (pylint, flake8)"
	@echo "  make test         - Run tests with pytest"
	@echo "  make coverage     - Generate test coverage report"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make build        - Build distribution packages"
	@echo "  make publish      - Publish package to PyPI"
	@echo "  make all          - Run all quality checks and tests"

install:
	$(PYTHON) -m pip install .

dev-install:
	$(PYTHON) -m pip install -e ".[dev]"

format:
	$(PYTHON) -m isort $(PACKAGE) tests
	$(PYTHON) -m black $(PACKAGE) tests
	$(PYTHON) -m pyupgrade --py37-plus **/*.py

lint:
	$(PYTHON) -m pylint $(PACKAGE) tests \
		--disable=C0114,C0115,C0116,R1725,C0103,W0621,W0603,R0914,E1101,W0622,R0903,W0702,W0212,W0102,R0912,R0915,C0301

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml
	@echo "Coverage report generated: coverage.xml"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/
	rm -rf **/*.pyc

build: clean
	$(PYTHON) -m build

publish: build
	$(PYTHON) -m twine check dist/*
	@echo "Ready to publish! Run 'python -m twine upload dist/*' to publish to PyPI"

all: dev-install format lint test coverage