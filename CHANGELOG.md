# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/cfdude/mcp-fred/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/cfdude/mcp-fred/releases/tag/v0.0.1
