#!/bin/bash
# Run all quality checks for the project

set -e  # Exit on error

echo "==================================="
echo "Running all quality checks..."
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        echo "Run: pip install -r requirements-dev.txt"
        exit 1
    fi
}

run_check() {
    echo -e "${YELLOW}Running $1...${NC}"
    if $2; then
        echo -e "${GREEN}✓ $1 passed${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}✗ $1 failed${NC}"
        echo ""
        return 1
    fi
}

# Check if required tools are installed
check_command black
check_command isort
check_command flake8
check_command pylint
check_command mypy
check_command bandit
check_command pytest

# Track failures
FAILED=0

# Code Formatting
run_check "black (formatting)" "black --check src tests" || FAILED=$((FAILED + 1))
run_check "isort (import sorting)" "isort --check-only src tests" || FAILED=$((FAILED + 1))

# Linting
run_check "flake8" "flake8 src tests" || FAILED=$((FAILED + 1))
run_check "pylint" "pylint src" || FAILED=$((FAILED + 1))

# Type Checking
run_check "mypy (type checking)" "mypy src" || FAILED=$((FAILED + 1))

# Security
run_check "bandit (security)" "bandit -r src -c .bandit" || FAILED=$((FAILED + 1))

# Tests
run_check "pytest (tests)" "pytest --cov=src/tana_import --cov-report=term-missing" || FAILED=$((FAILED + 1))

# Optional checks (don't fail on error)
echo -e "${YELLOW}Running optional checks...${NC}"
echo ""

echo "Safety check (dependency vulnerabilities):"
safety check --json || echo -e "${YELLOW}⚠ Safety check failed or found issues${NC}"
echo ""

echo "pip-audit (package vulnerabilities):"
pip-audit || echo -e "${YELLOW}⚠ pip-audit failed or found issues${NC}"
echo ""

# Summary
echo "==================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All quality checks passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}$FAILED check(s) failed ✗${NC}"
    exit 1
fi
