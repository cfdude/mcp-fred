# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CI/CD infrastructure with comprehensive testing and security scanning
- Pre-commit hooks for local development
- Documentation updates for clean Markdown rendering

---

## [0.1.0] - 2025-11-13

### Added
- **MCPB Extension Support** - Claude Desktop Extension packaging
  - Cross-platform Node.js launcher for bundled uv binaries
  - Support for macOS (ARM64/x64), Linux (x64), Windows (x64)
  - Automated build script with binary download
  - Single `.mcpb` file works across all platforms
  - Extension documentation (EXTENSION.md, BUNDLED_UV.md)
- **CI/CD Infrastructure** - Comprehensive automated testing and security
  - GitHub Actions workflows (ci.yml, security.yml)
  - Tests run on Python 3.11 and 3.12
  - Code formatting validation (ruff format)
  - Linting checks (ruff check)
  - 80% code coverage enforcement
  - Codecov integration
  - Secret scanning with Gitleaks
  - Dependency vulnerability scanning (pip-audit)
  - Hardcoded secret pattern detection
  - Weekly security scans
- **Pre-commit Hooks** - Local validation before commits
  - Automated formatting, linting, and test checks
  - Coverage validation
  - Easy installation script
  - Clear error messages and fix suggestions
- **Documentation**
  - CI_CD.md - Complete CI/CD workflow documentation
  - .gitleaks.toml - Secret scanning configuration
  - Updated README with extension and CI/CD information

### Changed
- README.md completely rewritten with clean Markdown formatting
  - Removed HTML tags and excessive formatting
  - Improved section structure and flow
  - Added CI/CD section
  - Removed internal project tracking information
- requirements.txt simplified (removed comments, kept dependencies only)

### Fixed
- README.md formatting issues on GitHub
- Typo in API_MAPPING.md reference
- Unsigned commits in CI/CD PR (rebased with signed commits)

### Security
- Gitleaks integration for secret detection
- Dependency vulnerability scanning
- Pattern detection for hardcoded secrets

### Added (Phase 2 Documentation - 2025-10-08)
- **Rate Limiting & Retry Logic section in ARCHITECTURE.md**
  - FRED API limits: 120 req/min, HTTP 429 response handling
  - Exponential backoff formula with jitter (±25% variance)
  - Max retries: 3 for 429 rate limits, 2 for 5xx server errors
  - Retry conditions: 429 and 5xx retry with backoff, 4xx fail immediately
  - Circuit breaker pattern: 5 failures threshold, 60s cooldown, state transitions
  - Configuration options and testing requirements
- **Testing Patterns section in DEVELOPMENT_GUIDE.md**
  - Mocking guidelines using respx for httpx requests
  - What to test: API client, error handling, retry logic, circuit breaker, rate limiting
  - Testing style: descriptive names, parametrize, one assertion per test
  - Quality standards: tests before merge, 80% coverage, no flaky tests
- **respx dependency** (12th dependency, 5th dev dependency)
  - requirements.txt: respx>=0.20.0 for httpx mocking
  - pyproject.toml: Added to dev dependencies
  - DEPENDENCIES.md: Full rationale with alternatives considered
  - Size analysis updated: ~61 MB total dev size (was ~60 MB)

### Changed (Phase 2 Documentation - 2025-10-08)
- **Total Dependencies**: Increased from 10 to 12 (7 core + 5 dev)
- **Documentation Philosophy**: Established principle-based approach (state expectations, not scaffolding)

### Decided (Phase 2 Documentation - 2025-10-08)
- **Concise Documentation**: ~70 lines added (down from 250-line proposal)
- **No Code Scaffolding**: Let AI figure out implementation from principles
- **respx for Mocking**: Official httpx mocking library with async support
- **Reject Code Examples**: Too much maintenance, AI can implement from guidelines

### Added (Phase 1 Implementation - 2025-10-08)
- **Project Directory Structure**
  - `src/mcp_fred/` package with subdirectories: api, tools, utils, transports
  - `tests/` with mirrored structure: test_api, test_tools, test_utils, test_transports, fixtures
  - All packages initialized with `__init__.py` files
- **pyproject.toml** - Comprehensive project configuration
  - Build system: setuptools
  - Project metadata: dependencies, classifiers, URLs
  - Ruff configuration: linting rules, formatting, isort
  - Pytest configuration: 80% coverage target, async mode, markers
  - Coverage reporting: HTML and terminal reports
- **requirements.txt** - All 11 dependencies with version constraints
  - Core: FastAPI, MCP SDK, httpx, pydantic, python-dotenv, tiktoken
  - Dev: ruff, pytest, pytest-asyncio, pytest-cov
  - Documented rationale for each dependency
- **.env.example** - Complete environment variable template
  - Required: FRED_API_KEY
  - Optional: Storage, output, token estimation, async job, rate limiting config
  - Development and production configuration examples
- **.gitignore** - Comprehensive Python project patterns
  - Python bytecode, distribution, testing, virtual environments
  - Ruff cache, IDE files (VS Code, PyCharm, Sublime)
  - Project-specific: fred-data/ directory
- **README.md** - Complete project documentation
  - Features overview with badges
  - Quick start guide and installation
  - Claude Desktop configuration examples
  - All 12 tools documented with examples
  - Smart output handling and token estimation
  - Development setup and testing guidelines
  - Architecture overview and contributing guidelines

### Changed (Phase 1 Implementation - 2025-10-08)
- **Package Version**: Set to 0.1.0 in `src/mcp_fred/__init__.py`

### Added (Phase 1 Documentation - 2025-10-08)
- **DEVELOPMENT_GUIDE.md** - Complete developer and AI agent setup guide
  - Prerequisites: Python 3.11+, Git, IDE setup
  - Environment setup: venv, dependencies, .env configuration
  - Development workflow: testing (80% coverage), debugging, git conventions
  - IDE configuration examples for VS Code and PyCharm
  - Claude Desktop MCP configuration examples
  - Common development tasks (adding tools, endpoints, utilities)
  - Testing philosophy: unit tests primary, mock FRED API, no E2E tests
- **DEPENDENCIES.md** - Detailed rationale for all 11 dependencies
  - Why each dependency was chosen over alternatives
  - Size analysis: ~35 MB production, ~60 MB with dev dependencies
  - Tiktoken justification: 2.7 MB acceptable for accurate token counting
  - Version pinning strategy and security update process
  - Dependency graph and quick reference
- **Error handling patterns in ARCHITECTURE.md**
  - 4 comprehensive patterns: API client, MCP tool, file system, async job
  - Error code reference table with 14 standardized codes
  - Full code examples for each pattern
  - Logging and user feedback examples

### Changed (Phase 1 Documentation - 2025-10-08)
- **Testing Strategy Defined**: 80% code coverage minimum, unit tests focus
- **Mocking Strategy**: Mock FRED API responses, no real API calls in tests

### Decided (Phase 1 Documentation - 2025-10-08)
- **No E2E Tests**: MCP product doesn't require end-to-end testing
- **Error Handling**: Document specific patterns we want to follow consistently
- **Troubleshooting**: Defer to Phase 6, keep it basic (API key, permissions, config)

### Added (Phase 0.5 - 2025-10-08)
- **Documentation review process** integrated into all 8 phases of TODO.md
- **Pre-phase documentation review sections** with 70+ specific questions
- **7-step documentation workflow** (review → analyze → recommend → approve → create → verify → proceed)
- **CONTEXT.md** - Quick start guide for new AI contexts
  - Project overview with current status
  - Key architectural decisions with user feedback quotes
  - Documentation navigation map
  - File location reference
  - Critical constraints and patterns
  - Development workflow
- **API_MAPPING.md** - Complete FRED API to MCP tool mapping
  - All 50+ FRED endpoints → 12 MCP tools
  - Tool call examples for each operation
  - Critical operations marked (Series, Maps)
  - Utility components reference
  - Response format patterns
  - Implementation checklist
- **TODO.md cross-references** - Every section links to architecture docs
- **Documentation quality standards** - 8 standards for all documentation

### Changed (Phase 0.5 - 2025-10-08)
- **TODO.md workflow** - Documentation review REQUIRED before each phase
- **Development process** - User approval required for documentation changes
- **Notes section** - Added comprehensive documentation guidelines

### Decided (Phase 0.5 - 2025-10-08)
- **Documentation-first approach** - Analyze and recommend docs before implementation
- **Self-contained documentation** - No dependency on external tools (Jira, Confluence)
- **Context continuity strategy** - New AI sessions can start from comprehensive docs
- **User control** - Approval required for all documentation proposals

### Added (Phase 0.4 - 2025-10-08)
- **Conservative token estimation strategy**
  - Reduced safe thresholds from 70% to 25% of total context capacity
  - Claude Sonnet: 50K safe limit (was 140K)
  - GPT-4: 25K safe limit (was 70K)
  - Gemini Pro: 250K safe limit (was 700K)
  - New configuration: `FRED_SAFE_TOKEN_LIMIT` and `FRED_ASSUME_CONTEXT_USED`
- **Project management tools** (3 new tools):
  - `fred_project_list` - Discover existing projects in storage directory
  - `fred_project_create` - Create new project with organized subdirectories
  - `fred_project_files` - List files within a project with metadata
- **Project directory structure** with automatic subdirectories and .project.json metadata
- **25 new development tasks** in TODO.md (7 token estimation, 18 project management)

### Changed (Phase 0.4 - 2025-10-08)
- **Token estimation philosophy**: "Err on the side of saving to file more often"
- **Context window assumptions**: Now assume 75% already consumed (was 30%)
- **Tool count**: Increased from 9 tools to 12 tools (6 data + 3 job + 3 project)

### Decided (Phase 0.4 - 2025-10-08)
- **Conservative approach**: Account for chat history and multiple MCP servers
- **Project workflow**: AI proactively asks users about project selection
- **Simplicity**: Focus on data retrieval, no server-side analysis

### Planned
- Phase 1: Project setup and infrastructure
- Phase 2: Core API client implementation
- Phase 3: MCP tool layer implementation (includes large data utilities)
- Phase 4: Transport layer implementation (STDIO and Streamable HTTP)
- Phase 5: Testing suite
- Phase 6: Documentation and polish
- Phase 7: Initial release preparation

---

## [0.0.1] - 2025-10-08

### Added
- Initial project planning and architecture documentation
- Git repository setup with signed commits
- Documentation structure:
  - `docs/FRED_API_REFERENCE.md` - FRED API endpoint reference
  - `docs/ARCHITECTURE.md` - System architecture and design
  - `docs/TODO.md` - Development task list with 8 phases
  - `docs/PROGRESS.md` - Completed task tracking
  - `CHANGELOG.md` - This changelog
- Project README placeholder
- `.gitignore` for Python projects

### Decided
- Technology stack: Python 3.11+, FastAPI, Ruff, pytest
- MCP transport protocols: STDIO and Streamable HTTP (excluding SSE)
- Tool structure: 6 consolidated tools using operation parameters
  - `fred_category` - Category operations
  - `fred_release` - Release operations (singular + plural endpoints)
  - `fred_series` - Series operations
  - `fred_source` - Source operations (singular + plural endpoints)
  - `fred_tag` - Tag operations
  - `fred_maps` - Maps/GeoFRED operations
- Configuration strategy: Environment variables via `.env` or MCP client config
- API key handling: `FRED_API_KEY` environment variable

### Repository
- Repository: https://github.com/cfdude/mcp-fred
- Branches: `main` (production), `dev` (development)
- Commit signing: SSH key-based signed commits enabled

---

## Version History

### Semantic Versioning Guidelines

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality in a backward-compatible manner
- **PATCH** version (0.0.X): Backward-compatible bug fixes

### Pre-1.0.0 Development

During initial development (0.x.x versions):
- Breaking changes may occur between minor versions
- The API is not yet stable
- Production use is not recommended

### Release Types

- **[Unreleased]**: Changes in development, not yet released
- **[X.Y.Z]**: Released versions with date stamps

---

## Change Categories

Changes are grouped by the following categories:

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes
- **Decided**: Architectural or design decisions (planning phase)

---

[Unreleased]: https://github.com/cfdude/mcp-fred/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cfdude/mcp-fred/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/cfdude/mcp-fred/releases/tag/v0.0.1
