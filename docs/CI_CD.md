# CI/CD Documentation

This document describes the continuous integration and deployment workflows for MCP-FRED.

## GitHub Actions Workflows

### CI Workflow (`.github/workflows/ci.yml`)

Runs on every push and pull request to `main` and `dev` branches.

**Jobs:**

1. **Test** (Matrix: Python 3.11 and 3.12)
   - ✅ Code formatting check (`ruff format --check`)
   - ✅ Linting check (`ruff check`)
   - ✅ Run full test suite with coverage
   - ✅ Verify 80% minimum coverage threshold
   - ✅ Upload coverage to Codecov (Python 3.12 only)

2. **Type Check**
   - ✅ Python syntax validation
   - ✅ Compile all Python files

**Status:** Required checks - all must pass before merging

### Security Workflow (`.github/workflows/security.yml`)

Runs on:
- Every push and pull request to `main` and `dev`
- Weekly schedule (Mondays at 9am UTC)

**Jobs:**

1. **Secret Scan**
   - 🔒 Scans for exposed secrets, API keys, tokens, passwords
   - 🔒 Uses Gitleaks with custom configuration (`.gitleaks.toml`)
   - 🔒 Checks entire git history

2. **Dependency Scan**
   - 🔒 Scans dependencies for known vulnerabilities (pip-audit)
   - 🔒 Checks for hardcoded secrets in source code
   - 🔒 Validates security patterns

**Status:** Required checks - must pass before merging

## Pre-Commit Hook

Local git hook that runs before each commit to ensure code quality.

### Installation

```bash
# Install the pre-commit hook
./scripts/install-pre-commit-hook.sh
```

### What It Checks

1. ✅ Code formatting (`ruff format --check`)
2. ✅ Linting (`ruff check`)
3. ✅ Full test suite (`pytest`)
4. ⚠️  Code coverage (warns if below 80%)

### Behavior

- **Blocks commits** if any check fails
- Provides clear error messages
- Suggests fix commands

### Uninstall

```bash
rm .git/hooks/pre-commit
```

## Development Workflow

### Before Committing

The pre-commit hook automatically runs checks. If you need to run manually:

```bash
# Run all checks
uv run ruff format --check .
uv run ruff check .
uv run pytest --cov=mcp_fred --cov-report=term-missing

# Auto-fix formatting and linting issues
uv run ruff format .
uv run ruff check --fix .
```

### Pull Request Process

1. Create feature branch from `dev`
2. Make changes and commit (pre-commit hook runs)
3. Push to remote
4. Open PR to `dev` branch
5. Wait for CI/CD checks to pass:
   - ✅ All tests pass
   - ✅ Code formatting correct
   - ✅ No linting errors
   - ✅ 80%+ coverage
   - ✅ No security issues
6. Request review
7. Merge after approval

### Branch Protection Rules

**`main` branch:**
- Require pull request reviews
- Require status checks to pass:
  - CI tests (Python 3.11, 3.12)
  - Security scans
- Require signed commits
- Require linear history

**`dev` branch:**
- Require status checks to pass
- Require signed commits

## Troubleshooting

### Pre-commit Hook Fails

**Formatting issues:**
```bash
uv run ruff format .
git add .
git commit
```

**Linting issues:**
```bash
uv run ruff check --fix .
git add .
git commit
```

**Test failures:**
```bash
# Run tests to see failures
uv run pytest -v

# Fix tests
# Then commit again
```

### CI Workflow Fails

Check the GitHub Actions logs:
1. Go to repository → Actions tab
2. Click on failed workflow run
3. Review job logs
4. Fix issues locally
5. Push again

### Security Scan Fails

**False positive:**
- Add to `.gitleaks.toml` allowlist
- Document why it's a false positive

**Real secret exposed:**
1. Remove secret from code
2. Rotate/revoke the exposed secret
3. Use environment variables instead
4. Commit the fix

## Coverage Requirements

- **Minimum:** 80% code coverage
- **Measured by:** pytest-cov
- **Enforced:** CI workflow fails if below threshold

Exclude from coverage:
- `__main__.py` files (entry points)
- Test files themselves

## Best Practices

1. ✅ Always run pre-commit hook (install it!)
2. ✅ Fix linting/formatting before pushing
3. ✅ Write tests for new features
4. ✅ Keep coverage above 80%
5. ✅ Never commit secrets/API keys
6. ✅ Sign all commits
7. ✅ Keep dependencies updated
8. ✅ Review security scan results

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
