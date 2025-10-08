# TODO - MCP-FRED Development Tasks

**Last Updated:** 2025-10-08

---

## Phase 1: Project Setup & Infrastructure

### Project Initialization
- [ ] Create project directory structure
- [ ] Initialize Python package structure (`src/mcp_fred/`)
- [ ] Create `pyproject.toml` for Ruff configuration
- [ ] Create `requirements.txt` with dependencies
- [ ] Create `.env.example` file
- [ ] Update `.gitignore` for Python projects
- [ ] Create `pytest.ini` configuration
- [ ] Set up basic README.md

### Dependencies to Install
- [ ] FastAPI
- [ ] Python MCP SDK
- [ ] httpx (async HTTP client)
- [ ] pydantic (data validation)
- [ ] python-dotenv (environment variables)
- [ ] tiktoken (token counting for OpenAI models)
- [ ] anthropic (for Claude token counting - optional)
- [ ] ruff (linting/formatting)
- [ ] pytest (testing)
- [ ] pytest-asyncio (async testing)
- [ ] pytest-cov (test coverage)
- [ ] pandas (optional: for CSV operations)

---

## Phase 2: Core API Client Implementation

### Base HTTP Client
- [ ] Create `src/mcp_fred/api/client.py` - Base FRED API client
- [ ] Implement authentication with API key
- [ ] Implement error handling and HTTP status code handling
- [ ] Add request/response logging
- [ ] Implement rate limiting (if needed)
- [ ] Add retry logic with exponential backoff

### API Response Models
- [ ] Create `src/mcp_fred/api/models/responses.py`
- [ ] Define Pydantic models for category responses
- [ ] Define Pydantic models for release responses
- [ ] Define Pydantic models for series responses
- [ ] Define Pydantic models for source responses
- [ ] Define Pydantic models for tag responses
- [ ] Define Pydantic models for maps responses

### Endpoint Implementations

#### Category Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/category.py`
- [ ] Implement `get_category(category_id)`
- [ ] Implement `get_category_children(category_id)`
- [ ] Implement `get_category_related(category_id)`
- [ ] Implement `get_category_series(category_id)`
- [ ] Implement `get_category_tags(category_id)`
- [ ] Implement `get_category_related_tags(category_id)`

#### Release Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/release.py`
- [ ] Implement `get_releases()` (plural)
- [ ] Implement `get_releases_dates()`
- [ ] Implement `get_release(release_id)` (singular)
- [ ] Implement `get_release_dates(release_id)`
- [ ] Implement `get_release_series(release_id)`
- [ ] Implement `get_release_sources(release_id)`
- [ ] Implement `get_release_tags(release_id)`
- [ ] Implement `get_release_related_tags(release_id)`
- [ ] Implement `get_release_tables(release_id)`

#### Series Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/series.py`
- [ ] Implement `get_series(series_id)`
- [ ] Implement `search_series(search_text)`
- [ ] Implement `get_series_categories(series_id)`
- [ ] Implement `get_series_observations(series_id)`
- [ ] Implement `get_series_release(series_id)`
- [ ] Implement `get_series_tags(series_id)`
- [ ] Implement `search_series_tags(series_search_text)`
- [ ] Implement `search_series_related_tags(series_search_text)`
- [ ] Implement `get_series_updates()`
- [ ] Implement `get_series_vintage_dates(series_id)`

#### Source Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/source.py`
- [ ] Implement `get_sources()` (plural)
- [ ] Implement `get_source(source_id)` (singular)
- [ ] Implement `get_source_releases(source_id)`

#### Tag Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/tag.py`
- [ ] Implement `get_tags()`
- [ ] Implement `get_tags_series(tag_names)`
- [ ] Implement `get_related_tags(tag_names)`

#### Maps Endpoints
- [ ] Create `src/mcp_fred/api/endpoints/maps.py`
- [ ] Implement `get_shapes(shape)`
- [ ] Implement `get_series_group(series_id)`
- [ ] Implement `get_regional_data()`
- [ ] Implement `get_series_data(series_id)`

---

## Phase 3: Large Data Handling Utilities

### Token Estimation
- [ ] Create `src/mcp_fred/utils/token_estimator.py`
- [ ] Implement token counting for text data
- [ ] Implement sampling strategy for large datasets
- [ ] Add model-specific token limit configuration
- [ ] Implement `should_use_file()` decision logic
- [ ] Add support for multiple AI models (Claude, GPT-4, Gemini)
- [ ] Write unit tests for token estimation

### File Writing Utilities
- [ ] Create `src/mcp_fred/utils/file_writer.py`
- [ ] Implement CSV writer with streaming support
- [ ] Implement JSON writer with streaming support
- [ ] Add chunked writing for large datasets
- [ ] Implement progress tracking during writes
- [ ] Add file size calculation and reporting
- [ ] Handle data type conversions for file formats
- [ ] Write unit tests for file writers

### Path Resolution & Security
- [ ] Create `src/mcp_fred/utils/path_resolver.py`
- [ ] Implement secure path resolution with `MCP_CLIENT_ROOT`
- [ ] Add validation to prevent directory traversal attacks
- [ ] Add check to prevent writing to MCP server directory
- [ ] Implement filename sanitization
- [ ] Add reserved name checking (Windows compatibility)
- [ ] Implement write permission validation
- [ ] Write unit tests for path security

### Output Handler Integration
- [ ] Create `src/mcp_fred/utils/output_handler.py`
- [ ] Implement `ResultOutputHandler` class
- [ ] Add filename pattern generation with variables
- [ ] Implement auto vs manual mode decision logic
- [ ] Add project-based directory organization
- [ ] Integrate token estimator for auto mode
- [ ] Integrate file writers for file output
- [ ] Add validation for output parameters
- [ ] Write integration tests

### Configuration for Large Data
- [ ] Add `OutputConfig` class to `config.py`
- [ ] Add environment variable loading for output settings
- [ ] Add `MCP_CLIENT_ROOT` validation
- [ ] Add default values for all output parameters
- [ ] Add Pydantic validation for output config
- [ ] Document all configuration options

---

## Phase 4: MCP Tool Layer Implementation

### Configuration Management
- [ ] Create `src/mcp_fred/config.py`
- [ ] Implement environment variable loading
- [ ] Implement configuration validation
- [ ] Add default value handling

### MCP Server Setup
- [ ] Create `src/mcp_fred/server.py` - Main MCP server
- [ ] Initialize FastMCP server
- [ ] Register all tools
- [ ] Add server metadata (name, version, description)

### Tool Implementations

#### Category Tool
- [ ] Create `src/mcp_fred/tools/category.py`
- [ ] Implement `fred_category` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Release Tool
- [ ] Create `src/mcp_fred/tools/release.py`
- [ ] Implement `fred_release` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Series Tool
- [ ] Create `src/mcp_fred/tools/series.py`
- [ ] Implement `fred_series` tool (CRITICAL: handles large observation datasets)
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large observations
- [ ] Add streaming support for 100k+ observation requests
- [ ] Add error handling
- [ ] Write tool documentation

#### Source Tool
- [ ] Create `src/mcp_fred/tools/source.py`
- [ ] Implement `fred_source` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Tag Tool
- [ ] Create `src/mcp_fred/tools/tag.py`
- [ ] Implement `fred_tag` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Maps Tool
- [ ] Create `src/mcp_fred/tools/maps.py`
- [ ] Implement `fred_maps` tool (CRITICAL: handles large geographical datasets)
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for shape files and regional data
- [ ] Add streaming support for large map data
- [ ] Add error handling
- [ ] Write tool documentation

---

## Phase 4: Transport Layer Implementation

### STDIO Transport
- [ ] Create `src/mcp_fred/transports/stdio.py`
- [ ] Implement STDIO transport handler
- [ ] Add JSON-RPC message parsing
- [ ] Add stdin/stdout communication
- [ ] Add graceful shutdown handling
- [ ] Test with MCP client (Claude Desktop)

### Streamable HTTP Transport
- [ ] Create `src/mcp_fred/transports/http.py`
- [ ] Implement FastAPI HTTP endpoint
- [ ] Add POST request handler for messages
- [ ] Add optional SSE streaming support
- [ ] Add authentication middleware (if needed)
- [ ] Add CORS configuration
- [ ] Test with HTTP MCP client

### Transport Selection
- [ ] Add transport auto-detection based on environment
- [ ] Add command-line arguments for transport selection
- [ ] Add configuration validation for transport-specific settings

---

## Phase 5: Testing

### Unit Tests

#### Output Handling Tests
- [ ] Test token estimation accuracy
- [ ] Test file vs screen decision logic
- [ ] Test path resolution and security
- [ ] Test filename generation and sanitization
- [ ] Test CSV writer with various data types
- [ ] Test JSON writer with various data types
- [ ] Test chunked writing for large datasets
- [ ] Test project directory organization
- [ ] Mock large datasets for testing

#### API Client Tests
- [ ] Test FRED API client initialization
- [ ] Test API key authentication
- [ ] Test error handling (400, 401, 404, 429, 500)
- [ ] Test request parameter building
- [ ] Mock API responses for testing

#### Endpoint Tests
- [ ] Test category endpoint functions
- [ ] Test release endpoint functions
- [ ] Test series endpoint functions
- [ ] Test source endpoint functions
- [ ] Test tag endpoint functions
- [ ] Test maps endpoint functions

#### Tool Tests
- [ ] Test `fred_category` tool operations
- [ ] Test `fred_release` tool operations
- [ ] Test `fred_series` tool operations
- [ ] Test `fred_source` tool operations
- [ ] Test `fred_tag` tool operations
- [ ] Test `fred_maps` tool operations

### Integration Tests
- [ ] Test end-to-end STDIO transport
- [ ] Test end-to-end HTTP transport
- [ ] Test with real FRED API (requires API key)
- [ ] Test error propagation through layers
- [ ] Test rate limiting behavior

### Test Coverage
- [ ] Set up pytest-cov
- [ ] Achieve 80%+ code coverage
- [ ] Generate coverage reports

---

## Phase 6: Documentation & Polish

### User Documentation
- [ ] Create comprehensive README.md
- [ ] Write installation instructions
- [ ] Write configuration guide
- [ ] Add usage examples for each tool
- [ ] Document error codes and troubleshooting
- [ ] Create `docs/USER_GUIDE.md`

### Developer Documentation
- [ ] Document code architecture
- [ ] Add inline code comments
- [ ] Create API reference documentation
- [ ] Document testing procedures
- [ ] Create contribution guidelines

### Code Quality
- [ ] Run Ruff linting on entire codebase
- [ ] Fix all Ruff warnings/errors
- [ ] Add type hints to all functions
- [ ] Run mypy for type checking (optional)

---

## Phase 7: Deployment & Release

### Package Preparation
- [ ] Create setup.py or use pyproject.toml for packaging
- [ ] Add __version__ to package
- [ ] Create distribution package
- [ ] Test package installation

### Release Checklist
- [ ] Update CHANGELOG.md with all changes
- [ ] Tag release with semantic version (v0.1.0)
- [ ] Create GitHub release
- [ ] Publish to PyPI (optional)

### Distribution
- [ ] Publish package to PyPI
- [ ] Create Docker image (optional)
- [ ] Add to MCP server registry (if exists)

---

## Phase 8: Future Enhancements (Post v1.0)

### Performance Optimization
- [ ] Implement response caching
- [ ] Add connection pooling
- [ ] Optimize batch requests
- [ ] Add request deduplication

### Advanced Features
- [ ] Add data visualization tools
- [ ] Support batch operations
- [ ] Add offline mode with cached data
- [ ] Implement streaming for large datasets

### Monitoring & Observability
- [ ] Add structured logging
- [ ] Add metrics collection
- [ ] Add health check endpoint
- [ ] Add debugging mode

---

## Notes

- All tasks should be completed in order by phase
- Each completed task should be moved to PROGRESS.md
- Update CHANGELOG.md after completing each phase
- Run tests before marking a phase as complete
- Use conventional commits for all git commits
