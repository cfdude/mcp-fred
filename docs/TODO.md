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
- [ ] **tiktoken** (token counting - lightweight ~2.7 MB installed)
- [ ] ruff (linting/formatting)
- [ ] pytest (testing)
- [ ] pytest-asyncio (async testing)
- [ ] pytest-cov (test coverage)

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

### Token Estimation (using tiktoken)
- [ ] Create `src/mcp_fred/utils/token_estimator.py`
- [ ] Install and integrate tiktoken library (~2.7 MB)
- [ ] Implement token counting using tiktoken encodings
- [ ] Implement sampling strategy for large datasets
- [ ] Add model-specific token limit configuration
- [ ] **Implement conservative token limits (25% of context capacity)**
- [ ] **Add Claude Sonnet safe limit: 50K tokens (was 140K)**
- [ ] **Add GPT-4 safe limit: 25K tokens (was 70K)**
- [ ] **Add Gemini Pro safe limit: 250K tokens (was 700K)**
- [ ] **Add `FRED_SAFE_TOKEN_LIMIT` configuration option**
- [ ] **Add `FRED_ASSUME_CONTEXT_USED` configuration (default: 0.75)**
- [ ] Add encoding support for Claude (cl100k_base approximation)
- [ ] Add encoding support for GPT-4 (cl100k_base)
- [ ] Implement `should_use_file()` decision logic with conservative thresholds
- [ ] Write unit tests for token estimation with conservative limits

### JSON to CSV Conversion
- [ ] Create `src/mcp_fred/utils/json_to_csv.py`
- [ ] Implement JSON to CSV converter for series observations
- [ ] Handle nested JSON structures (flatten for CSV)
- [ ] Implement converter for category data
- [ ] Implement converter for release data
- [ ] Implement converter for maps/GeoFRED data
- [ ] Add proper CSV headers based on JSON structure
- [ ] Handle edge cases (null values, nested arrays, special characters)
- [ ] Write unit tests for JSON to CSV conversion

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
- [ ] Implement secure path resolution with `FRED_STORAGE_DIR`
- [ ] Add validation to prevent directory traversal attacks
- [ ] Add check to prevent writing to MCP server directory
- [ ] Support user-configurable storage directory (any local path)
- [ ] Create project subdirectories automatically
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
- [ ] Integrate token estimator for auto mode (tiktoken)
- [ ] Integrate JSON to CSV converter for CSV output
- [ ] Integrate file writers for file output
- [ ] Add validation for output parameters
- [ ] Write integration tests

### Configuration for Large Data
- [ ] Add `OutputConfig` class to `config.py`
- [ ] Add environment variable loading for output settings
- [ ] Add `FRED_STORAGE_DIR` configuration and validation
- [ ] Support user-configurable storage directory path
- [ ] Add default value: `./fred-data` if not specified
- [ ] Add default values for all output parameters
- [ ] Add Pydantic validation for output config
- [ ] Add `FRED_JOB_RETENTION_HOURS` configuration
- [ ] Document all configuration options in config.py

### Async Job Management
- [ ] Create `src/mcp_fred/utils/job_manager.py`
- [ ] Implement `JobManager` class with in-memory job storage
- [ ] Implement job ID generation (UUID-based)
- [ ] Implement job lifecycle management (create, update, complete, fail)
- [ ] Add job status tracking (accepted, processing, completed, failed)
- [ ] Add progress tracking (rows fetched, percent complete, elapsed time)
- [ ] Implement job cleanup (auto-delete after 24 hours)
- [ ] Add job retention configuration
- [ ] Write unit tests for job manager

### Background Job Processing
- [ ] Create `src/mcp_fred/utils/background_worker.py`
- [ ] Implement background task queue using asyncio
- [ ] Add worker pool for concurrent job processing
- [ ] Implement job retry logic for failed requests
- [ ] Add exponential backoff for rate limit errors
- [ ] Implement progress callbacks for job updates
- [ ] Add graceful shutdown for background workers
- [ ] Write integration tests for background processing

### Async Job Decision Logic
- [ ] Add size estimation before executing requests
- [ ] Implement threshold for async vs sync (>10K rows = async)
- [ ] Add time estimation for operations
- [ ] Integrate job manager with output handler
- [ ] Add async mode to all tools that fetch large data
- [ ] Document async vs sync decision criteria

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

#### Job Management Tools
- [ ] Create `src/mcp_fred/tools/job_status.py`
- [ ] Implement `fred_job_status` tool
- [ ] Add job_id parameter validation
- [ ] Return comprehensive status (progress, result, error)
- [ ] Add error handling for invalid job IDs
- [ ] Write tool documentation

- [ ] Create `src/mcp_fred/tools/job_list.py` (Optional)
- [ ] Implement `fred_job_list` tool
- [ ] Add status filtering (completed, processing, failed)
- [ ] Add pagination/limit support
- [ ] Write tool documentation

- [ ] Create `src/mcp_fred/tools/job_cancel.py` (Optional)
- [ ] Implement `fred_job_cancel` tool
- [ ] Add cancellation logic
- [ ] Clean up resources for cancelled jobs
- [ ] Write tool documentation

#### Project Management Tools
- [ ] Create `src/mcp_fred/tools/project_list.py`
- [ ] Implement `fred_project_list` tool
- [ ] Add directory scanning logic for FRED_STORAGE_DIR
- [ ] Calculate project metadata (file count, size, dates)
- [ ] Add error handling for missing storage directory
- [ ] Write tool documentation

- [ ] Create `src/mcp_fred/tools/project_create.py`
- [ ] Implement `fred_project_create` tool
- [ ] Add project name validation (alphanumeric, hyphens, underscores)
- [ ] Create subdirectories (series, maps, releases, categories, sources, tags)
- [ ] Create .project.json metadata file
- [ ] Add error handling for existing projects
- [ ] Write tool documentation

- [ ] Create `src/mcp_fred/tools/project_files.py`
- [ ] Implement `fred_project_files` tool
- [ ] Add file listing with metadata (size, rows, dates, format)
- [ ] Add subdirectory filtering (series, maps, releases, etc.)
- [ ] Add sorting options (name, size, modified, created)
- [ ] Add pagination/limit support
- [ ] Add error handling for missing projects
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
- [ ] Test token estimation accuracy with tiktoken
- [ ] Test file vs screen decision logic
- [ ] Test path resolution and security
- [ ] Test FRED_STORAGE_DIR configuration
- [ ] Test user-configurable storage directory paths
- [ ] Test filename generation and sanitization
- [ ] Test JSON to CSV conversion for series data
- [ ] Test JSON to CSV conversion for nested structures
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
- [ ] Test `fred_series` tool operations (including async mode)
- [ ] Test `fred_source` tool operations
- [ ] Test `fred_tag` tool operations
- [ ] Test `fred_maps` tool operations (including async mode)
- [ ] Test `fred_job_status` tool
- [ ] Test `fred_job_list` tool (optional)
- [ ] Test `fred_job_cancel` tool (optional)
- [ ] Test `fred_project_list` tool
- [ ] Test `fred_project_create` tool
- [ ] Test `fred_project_files` tool

#### Async Job Tests
- [ ] Test job creation and ID generation
- [ ] Test job status transitions (accepted → processing → completed)
- [ ] Test job failure handling and retry logic
- [ ] Test job progress tracking
- [ ] Test job cleanup after retention period
- [ ] Test background worker task queue
- [ ] Test concurrent job processing
- [ ] Test rate limit handling with backoff
- [ ] Mock large FRED API responses for testing

#### Project Management Tests
- [ ] Test project listing with metadata calculation
- [ ] Test project creation with directory structure
- [ ] Test project creation validation (name, duplicates)
- [ ] Test project files listing with filtering
- [ ] Test project files sorting (name, size, modified)
- [ ] Test .project.json metadata creation and reading
- [ ] Test handling of missing FRED_STORAGE_DIR
- [ ] Test handling of non-existent projects
- [ ] Mock file system operations for testing

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
