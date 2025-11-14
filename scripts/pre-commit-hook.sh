#!/usr/bin/env bash
# Pre-commit hook for MCP-FRED
# Runs code formatting, linting, and tests before allowing commits
# Install: cp scripts/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -e

echo "🔍 Running pre-commit checks..."
echo

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed"
    echo "   Install with: brew install uv (macOS) or pip install uv"
    exit 1
fi

# Check code formatting
echo "📋 Checking code formatting..."
if ! uv run ruff format --check .; then
    echo
    echo "❌ Code formatting check failed!"
    echo "   Run: uv run ruff format ."
    echo "   Then stage the changes and commit again"
    exit 1
fi
echo "✅ Code formatting passed"
echo

# Run linting
echo "🔎 Running linting checks..."
if ! uv run ruff check .; then
    echo
    echo "❌ Linting check failed!"
    echo "   Run: uv run ruff check --fix ."
    echo "   Review the changes, stage them, and commit again"
    exit 1
fi
echo "✅ Linting passed"
echo

# Run tests
echo "🧪 Running tests..."
if ! uv run pytest --cov=mcp_fred --cov-report=term-missing -q; then
    echo
    echo "❌ Tests failed!"
    echo "   Fix the failing tests before committing"
    exit 1
fi
echo "✅ All tests passed"
echo

# Check coverage
echo "📊 Checking code coverage..."
coverage_percent=$(uv run coverage report --format=total 2>/dev/null || echo "0")
if ! python3 -c "exit(0 if float('$coverage_percent') >= 80 else 1)" 2>/dev/null; then
    echo "⚠️  Warning: Coverage ${coverage_percent}% is below 80% threshold"
    echo "   Consider adding more tests"
    # Don't fail on coverage, just warn
fi
echo

echo "✅ All pre-commit checks passed!"
echo "   Proceeding with commit..."
echo
