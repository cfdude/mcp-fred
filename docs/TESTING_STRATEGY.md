# MCP-FRED Testing Strategy

This document explains how we keep the MCP-FRED codebase reliable. It covers the
available test suites, the mocking patterns we rely on, coverage expectations,
and how to add new tests without breaking the existing workflow.

## Test Taxonomy

| Suite | Location | Purpose |
|-------|----------|---------|
| **Unit Tests** | `tests/test_api`, `tests/test_utils` | Verify API client behaviour, response models, and helper utilities in isolation. |
| **Tool-Level Integration** | `tests/test_tools` | Exercise the public MCP tools (category, release, maps, project, etc.) with mocked FRED responses and file system state. |
| **Scenario Tests** | `tests/test_tools` (async job cases) | Drive async job flows for series/maps tools, covering job creation → retry → completion/cancellation. |
| **Transport Smoke Tests** | `tests/test_transports` | Validate STDIO/HTTP transport wiring and CLI command surfaces. |

## Fixtures and Mocking

- **HTTP mocking:** We use [`respx`](https://lundberg.github.io/respx/) to intercept
  `httpx` calls in API client and tool tests. Routes live inside the test body; when
  a test needs richer data we place JSON samples in `tests/fixtures/`.
- **GeoFRED fixtures:** Representative map payloads reside in
  `tests/fixtures/maps/` (shape values, series groups, regional and series data).
  These fixtures drive both the tool tests and JSON→CSV converter assertions.
- **Server context:** `tests/conftest.py` exposes an async `server_context`
  fixture that wires the FRED client, background worker, and job manager. The
  fixture automatically stops the worker after each test to avoid lingering
  tasks on event loop shutdown.
- **File system:** Tool tests create temporary project directories under
  `fred-data/`. Every test cleans up after itself so repeated runs stay idempotent.

## Running the Test Suite

```bash
# Lint + type safety
python3 -m ruff check .

# Format when needed
python3 -m ruff format .

# Full test run with coverage gates (>= 80%)
python3 -m pytest

# Focused runs
python3 -m pytest tests/test_tools/test_tools.py -k maps
python3 -m pytest tests/test_utils/test_job_manager.py
```

Pytest options (verbosity, markers) come from `pyproject.toml`. Async tests use
`pytest-asyncio` in auto mode, so you do **not** need to pass the event loop
explicitly.

## Coverage Expectations

- Coverage is enforced at **80%** via `--cov-fail-under=80` in `pyproject.toml`.
- HTML reports land in `htmlcov/` for manual inspection. Use them when touching
  low-level helpers (token estimator, job manager) to ensure edge paths remain covered.

## Adding New Tests

1. Pick the suite that matches your change (unit/tool/transport).
2. Prefer fixtures over inline data for large payloads (see `tests/fixtures/maps`).
3. Use `respx` for HTTP behaviour, `monkeypatch` for async workers/job manager hooks.
4. Always run `ruff check` and `pytest` before raising a PR or handing work back
   to the user.
5. When adding async job scenarios, assert the job status, retry counts, and
   stored artifacts (file paths, errors) so regressions surface quickly.

## Related Documentation

- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) – Setup, linting, and server workflows.
- [ARCHITECTURE.md](ARCHITECTURE.md#large-data-handling-strategy) – Details on
  async job processing and large data handling.
- [SERIES_MAPS_GUIDE.md](SERIES_MAPS_GUIDE.md) – Patterns for series/maps tools,
  including file output recommendations.
- [DESIGN_NOTES.md](DESIGN_NOTES.md) – Upcoming enhancements and testing TODOs.
