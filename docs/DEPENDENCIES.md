# MCP-FRED Dependencies

**Detailed explanation of every dependency and why it was chosen**

---

## Overview

This document explains the rationale behind each dependency in the MCP-FRED project. Understanding these choices helps with:
- Security audits and vulnerability assessments
- Dependency updates and version management
- Architecture decisions and tradeoffs
- Contribution guidelines

**Total Dependencies:** 12 (7 core + 5 development)

---

## Core Dependencies (Runtime)

### 1. FastAPI

**Version Required:** Latest stable (>= 0.100.0)

**Purpose:** Web framework for HTTP transport and async request handling

**Why FastAPI?**
- **Async-first design**: Built on asyncio for high performance
- **Type safety**: Uses Pydantic for request/response validation
- **OpenAPI integration**: Auto-generates API documentation
- **MCP compatibility**: Supports streamable HTTP transport
- **Modern Python**: Leverages Python 3.11+ features

**Alternatives Considered:**
- Flask: No native async support, older architecture
- Django: Too heavy for our needs, overkill for MCP server
- Starlette: FastAPI is built on Starlette, but FastAPI adds convenience

**Used For:**
- HTTP transport implementation (`src/mcp_fred/transports/http.py`)
- Request/response handling
- Optional SSE streaming support

---

### 2. Python MCP SDK

**Version Required:** Latest stable

**Purpose:** Official Model Context Protocol implementation

**Why Python MCP SDK?**
- **Official SDK**: Maintained by Anthropic/MCP team
- **Protocol compliance**: Ensures MCP specification adherence
- **STDIO support**: Native support for local communication
- **Type safety**: Typed interfaces for tools and resources
- **Best practices**: Follows MCP patterns and conventions

**Alternatives Considered:**
- Custom implementation: High risk of spec deviation, more work
- Third-party SDKs: Not officially supported

**Used For:**
- MCP server implementation (`src/mcp_fred/server.py`)
- Tool registration and discovery
- STDIO transport (`src/mcp_fred/transports/stdio.py`)
- JSON-RPC message handling

---

### 3. httpx

**Version Required:** >= 0.24.0

**Purpose:** Async HTTP client for FRED API requests

**Why httpx?**
- **Async support**: Native asyncio for non-blocking I/O
- **HTTP/2 support**: Modern protocol for better performance
- **Connection pooling**: Efficient for multiple requests
- **Familiar API**: Similar to requests, easy to learn
- **Type hints**: Fully typed for better IDE support

**Alternatives Considered:**
- requests: No async support (blocking I/O)
- aiohttp: More complex API, httpx more intuitive

**Used For:**
- FRED API client (`src/mcp_fred/api/client.py`)
- All API endpoint implementations (`src/mcp_fred/api/endpoints/`)
- Rate limiting and retry logic

---

### 4. pydantic

**Version Required:** >= 2.0.0

**Purpose:** Data validation and settings management

**Why Pydantic?**
- **Runtime validation**: Catches errors at runtime, not just type checking
- **Type safety**: Enforces types for API responses
- **Settings management**: Perfect for environment variable handling
- **JSON serialization**: Built-in JSON encoding/decoding
- **FastAPI integration**: FastAPI uses Pydantic natively

**Alternatives Considered:**
- dataclasses: No runtime validation
- attrs: Less mature ecosystem
- marshmallow: More verbose, less modern

**Used For:**
- Configuration management (`src/mcp_fred/config.py`)
- API response models (`src/mcp_fred/api/models/responses.py`)
- Tool parameter validation
- Environment variable parsing

---

### 5. python-dotenv

**Version Required:** >= 1.0.0

**Purpose:** Load environment variables from `.env` file

**Why python-dotenv?**
- **Development convenience**: Manage local config without system env vars
- **Standard pattern**: Industry-standard for Python projects
- **Simple API**: One function call to load
- **No dependencies**: Lightweight library

**Alternatives Considered:**
- Manual parsing: Reinventing the wheel
- Environment variables only: Less convenient for development

**Used For:**
- Loading `.env` file in development
- Configuration management (`src/mcp_fred/config.py`)
- Local testing and development

**Production Note:** Not used in production; MCP clients pass env vars directly

---

### 6. tiktoken

**Version Required:** >= 0.5.0

**Purpose:** Accurate token counting for AI context management

**Why tiktoken?**
- **Accuracy**: OpenAI's official tokenization library
- **Lightweight**: Only ~2.7 MB installed (acceptable overhead)
- **Multiple encodings**: Supports Claude, GPT-4, GPT-3.5 approximations
- **Fast**: Implemented in Rust for performance
- **Well-maintained**: Official OpenAI library

**Alternatives Considered:**
- transformers: 2+ GB install size (too heavy)
- Custom estimation: Inaccurate, unreliable
- Character count: Very inaccurate for token limits

**Critical Use Case:**
Conservative token estimation (Phase 0.4 decision):
- Claude Sonnet: 50K safe limit (assume 75% context used)
- GPT-4: 25K safe limit
- Prevents context overflow from large FRED datasets

**Used For:**
- Token estimation (`src/mcp_fred/utils/token_estimator.py`)
- Auto vs file output decision
- Large dataset detection (>10K observations)

---

### 7. FastMCP (or equivalent MCP helper)

**Version Required:** Latest stable

**Purpose:** Simplified MCP server creation and tool registration

**Why FastMCP?**
- **Convenience**: Reduces boilerplate for MCP servers
- **Decorators**: Clean syntax for tool registration
- **Type safety**: Typed tool parameters
- **Best practices**: Enforces MCP patterns

**Note:** Exact package name depends on official MCP SDK structure

**Used For:**
- Server initialization (`src/mcp_fred/server.py`)
- Tool decorators and registration
- Transport configuration

---

## Development Dependencies (Not in Production)

### 8. ruff

**Version Required:** >= 0.1.0

**Purpose:** Fast Python linter and formatter (replaces flake8, black, isort)

**Why Ruff?**
- **Speed**: 10-100x faster than alternatives (written in Rust)
- **All-in-one**: Linting + formatting + import sorting
- **Configuration**: Single tool instead of 3+ tools
- **Modern**: Supports Python 3.11+ features
- **Growing adoption**: Rapidly becoming industry standard

**Alternatives Considered:**
- flake8 + black + isort: Slower, multiple configs
- pylint: Slower, more opinionated
- autopep8: Only formatting, not linting

**Configuration:** `pyproject.toml`

**Used For:**
- Code linting: `ruff check .`
- Code formatting: `ruff format .`
- Import sorting
- Pre-commit checks

---

### 9. pytest

**Version Required:** >= 7.0.0

**Purpose:** Testing framework

**Why pytest?**
- **Simple syntax**: No boilerplate (unlike unittest)
- **Fixtures**: Reusable test setup
- **Parametrization**: Test multiple inputs easily
- **Plugin ecosystem**: Rich ecosystem (pytest-cov, pytest-asyncio)
- **Industry standard**: Most popular Python testing framework

**Alternatives Considered:**
- unittest: More verbose, built-in but less convenient
- nose: Deprecated
- doctest: Too limited for comprehensive testing

**Used For:**
- All testing (`tests/`)
- Unit tests, integration tests
- Coverage reporting (with pytest-cov)

**Testing Philosophy (Phase 1 decision):**
- 80% code coverage minimum
- Focus on unit tests (primary)
- Integration tests as needed
- Mock FRED API (no real API calls)

---

### 10. pytest-asyncio

**Version Required:** >= 0.21.0

**Purpose:** Async test support for pytest

**Why pytest-asyncio?**
- **Async testing**: Required for testing async functions
- **Fixture support**: Async fixtures for setup/teardown
- **Event loop management**: Handles asyncio event loops in tests

**Alternatives Considered:**
- Manual asyncio.run(): More boilerplate
- trio: Different async framework

**Used For:**
- Testing async API client methods
- Testing async tool implementations
- Testing background job processing

---

### 11. pytest-cov

**Version Required:** >= 4.0.0

**Purpose:** Code coverage reporting for pytest

**Why pytest-cov?**
- **Pytest integration**: Seamless integration with pytest
- **Multiple formats**: HTML, XML, terminal reports
- **Coverage goals**: Track 80% coverage requirement
- **CI/CD ready**: Works with GitHub Actions, etc.

**Alternatives Considered:**
- coverage.py: pytest-cov wraps this, easier to use
- Manual coverage: Less convenient

**Used For:**
- Coverage reporting: `pytest --cov=mcp_fred --cov-report=html`
- Coverage enforcement in CI/CD
- Identifying untested code

---

### 12. respx

**Version Required:** >= 0.20.0

**Purpose:** Mock httpx requests for testing

**Why respx?**
- **httpx-specific**: Designed specifically for mocking httpx (our HTTP client)
- **Async support**: Full asyncio support for async client testing
- **Pattern matching**: Flexible request matching (URL, headers, body)
- **Simple API**: Clean, intuitive mocking syntax
- **Well-maintained**: Active development, good documentation

**Alternatives Considered:**
- httpx built-in mocking: Limited, respx more feature-rich
- responses library: Only works with requests, not httpx
- Manual mocking: More boilerplate, harder to maintain

**Used For:**
- Mocking FRED API responses in tests
- Testing retry logic (429 rate limits, 5xx errors)
- Testing error handling (401, 404, etc.)
- Testing circuit breaker state transitions
- Verifying request parameters sent to FRED API

---

## Dependency Management Strategy

### Version Pinning

**Strategy:** Minimum version requirements with compatibility ranges

```txt
# requirements.txt format
fastapi>=0.100.0,<1.0.0
httpx>=0.24.0,<1.0.0
pydantic>=2.0.0,<3.0.0
python-dotenv>=1.0.0
tiktoken>=0.5.0,<1.0.0
ruff>=0.1.0
pytest>=7.0.0,<8.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
```

**Rationale:**
- Minimum versions ensure required features
- Upper bounds prevent breaking changes
- Leave room for patch/minor updates

### Security Updates

**Process:**
1. Monitor security advisories (GitHub Dependabot)
2. Test updates in development first
3. Update requirements.txt
4. Run full test suite
5. Document in CHANGELOG.md

### Dependency Audits

**Frequency:** Before each release

**Tools:**
```bash
# Check for vulnerabilities
pip-audit

# Check for outdated packages
pip list --outdated

# Check dependency tree
pipdeptree
```

---

## Why These Dependencies?

### Design Principles

1. **Minimal dependencies**: Only what we actually need
2. **Modern Python**: Leverage 3.11+ features
3. **Async-first**: Non-blocking I/O for performance
4. **Type safety**: Runtime validation and IDE support
5. **Developer experience**: Fast tools, good DX
6. **Well-maintained**: Active projects, good track records

### Avoided Dependencies

**What we DON'T use and why:**

❌ **pandas/numpy**: Too heavy for our needs, overkill for CSV conversion
❌ **SQLAlchemy**: No database, all data from FRED API
❌ **Redis**: In-memory job storage sufficient, Redis optional for production
❌ **Celery**: Background worker simpler with asyncio
❌ **Django**: Too heavy, FastAPI sufficient
❌ **transformers**: 2+ GB, tiktoken at 2.7 MB is better

---

## Dependency Size Analysis

**Install Sizes (approximate):**

| Dependency | Size | Justification |
|------------|------|---------------|
| FastAPI | ~15 MB | Core framework, worth it |
| MCP SDK | ~5 MB | Required for MCP |
| httpx | ~3 MB | Async HTTP client |
| pydantic | ~8 MB | Validation + settings |
| python-dotenv | <1 MB | Tiny utility |
| tiktoken | **2.7 MB** | Acceptable for token accuracy |
| ruff | ~20 MB | Dev only, fast tooling |
| pytest | ~5 MB | Dev only, testing |
| pytest-asyncio | <1 MB | Dev only, async tests |
| pytest-cov | ~2 MB | Dev only, coverage |
| respx | ~1 MB | Dev only, httpx mocking |

**Total Production Size:** ~35 MB (very reasonable)
**Total Dev Size:** ~61 MB (acceptable)

---

## Future Dependency Considerations

### Potential Additions (Post v1.0)

**If we add caching (Phase 8):**
- Redis client (redis-py) - Optional, for distributed caching
- OR python-lru-cache - Built-in, simpler

**If we add observability (Phase 8):**
- structlog - Structured logging
- prometheus-client - Metrics collection

**If we add data visualization (Phase 8):**
- matplotlib - Charting (but probably external to MCP server)

### Version Migration Plan

When major versions are released:
1. Test in separate branch
2. Review breaking changes
3. Update code as needed
4. Full test suite pass
5. Document migration in CHANGELOG.md

---

## Dependency Graph

```
mcp-fred
├── FastAPI (web framework)
│   └── pydantic (validation)
│   └── starlette (ASGI)
├── MCP SDK (protocol)
├── httpx (HTTP client)
│   └── httpcore
│   └── certifi (SSL)
├── pydantic (validation)
├── python-dotenv (env vars)
├── tiktoken (token counting)
│   └── regex (pattern matching)
│   └── requests (downloading models)
├── ruff (linting) [dev]
├── pytest (testing) [dev]
│   └── pluggy (plugin system)
├── pytest-asyncio (async tests) [dev]
│   └── pytest
└── pytest-cov (coverage) [dev]
    └── pytest
    └── coverage
```

---

## Quick Reference

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Update all dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Check for security issues:**
```bash
pip install pip-audit
pip-audit
```

**Generate dependency tree:**
```bash
pip install pipdeptree
pipdeptree
```

---

**Last Updated:** 2025-10-08
**Document Version:** 1.0
