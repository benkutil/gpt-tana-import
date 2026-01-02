.PHONY: help install install-dev test lint format type-check security check clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .

test: ## Run tests with coverage
	pytest --cov=src/tana_import --cov-report=term-missing --cov-report=html

test-verbose: ## Run tests with verbose output
	pytest -v --cov=src/tana_import --cov-report=term-missing

lint: ## Run all linters
	black --check src tests
	isort --check-only src tests
	flake8 src tests
	pylint src || pylint-exit $$?

format: ## Auto-format code
	black src tests
	isort src tests

type-check: ## Run type checking
	mypy src

security: ## Run security scans
	bandit -r src -c .bandit
	@echo "Running safety check (may fail on system packages)..."
	@safety check --json || true
	@echo "Running pip-audit (may fail on system packages)..."
	@pip-audit || true

check: ## Run all quality checks
	@./scripts/check-all.sh

clean: ## Clean up generated files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true
