# TODO - MCP-FRED Development Tasks

**Last Updated:** 2025-10-08

**Quick Links:**
- [CONTEXT.md](CONTEXT.md) - Start here for new contexts
- [API_MAPPING.md](API_MAPPING.md) - FRED API → Tools → Files mapping
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete system design
- [PROGRESS.md](PROGRESS.md) - Completed work

---

## Phase 1: Project Setup & Infrastructure

**[See: ARCHITECTURE.md → Project Structure](ARCHITECTURE.md#project-structure)**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md sections relevant to this phase
- [ ] **Identify Documentation Gaps**: Are there missing diagrams, examples, or clarifications needed?
- [ ] **Analyze Documentation Needs**: Based on this phase's tasks, what new documentation would help?
- [ ] **Recommend Updates**: Propose new documentation files or enhancements to existing docs
- [ ] **Get User Approval**: Present recommendations and wait for user approval before proceeding
- [ ] **Create/Update Documentation**: Implement approved documentation changes
- [ ] **Verify Cross-References**: Ensure all TODO items link to relevant architecture sections

**Questions to Answer:**
1. Do we need a DEVELOPMENT_GUIDE.md with project setup walkthrough?
2. Should we create Python package structure diagrams?
3. Do we need a DEPENDENCIES.md explaining why each dependency is needed?
4. Should we document common development environment issues and solutions?
5. Any other documentation that would help with this phase or future phases?

**Priority 2 Documentation (From Phase 0.4):**
- DEVELOPMENT_GUIDE.md - Implementation roadmap
- Enhanced ARCHITECTURE.md - More code examples
- TESTING_STRATEGY.md - Testing philosophy and patterns

---

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

**[See: ARCHITECTURE.md → API Client Architecture](ARCHITECTURE.md#api-client-architecture)**
**[See: FRED_API_REFERENCE.md](FRED_API_REFERENCE.md) - Complete FRED API documentation**
**[See: API_MAPPING.md](API_MAPPING.md) - All endpoint mappings**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md → API Client Architecture
- [ ] **Review API Documentation**: Study FRED_API_REFERENCE.md and API_MAPPING.md thoroughly
- [ ] **Identify Documentation Gaps**: Are HTTP client patterns clearly documented?
- [ ] **Analyze Documentation Needs**: What would help with API client implementation?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Cross-References**: Ensure API_MAPPING.md accurately reflects all endpoints

**Questions to Answer:**
1. Do we need detailed code examples for each endpoint implementation?
2. Should we create HTTP request/response examples for each FRED API operation?
3. Do we need error handling patterns documented with code examples?
4. Should we document retry logic and rate limiting strategies in detail?
5. Do we need a separate API_CLIENT_GUIDE.md for implementation patterns?
6. Should we add sequence diagrams showing API request flow?
7. Any documentation about testing API client with mocked responses?

---

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

**[See: API_MAPPING.md](API_MAPPING.md) for complete endpoint → method mapping**

#### Category Endpoints

**[See: API_MAPPING.md → Category Endpoints](API_MAPPING.md#category-endpoints)**
- [ ] Create `src/mcp_fred/api/endpoints/category.py`
- [ ] Implement `get_category(category_id)`
- [ ] Implement `get_category_children(category_id)`
- [ ] Implement `get_category_related(category_id)`
- [ ] Implement `get_category_series(category_id)`
- [ ] Implement `get_category_tags(category_id)`
- [ ] Implement `get_category_related_tags(category_id)`

#### Release Endpoints

**[See: API_MAPPING.md → Release Endpoints](API_MAPPING.md#release-endpoints)**
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

**[See: API_MAPPING.md → Series Endpoints](API_MAPPING.md#series-endpoints)** ⚠️ CRITICAL: Large data handling
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

**[See: API_MAPPING.md → Source Endpoints](API_MAPPING.md#source-endpoints)**
- [ ] Create `src/mcp_fred/api/endpoints/source.py`
- [ ] Implement `get_sources()` (plural)
- [ ] Implement `get_source(source_id)` (singular)
- [ ] Implement `get_source_releases(source_id)`

#### Tag Endpoints

**[See: API_MAPPING.md → Tag Endpoints](API_MAPPING.md#tag-endpoints)**
- [ ] Create `src/mcp_fred/api/endpoints/tag.py`
- [ ] Implement `get_tags()`
- [ ] Implement `get_tags_series(tag_names)`
- [ ] Implement `get_related_tags(tag_names)`

#### Maps Endpoints

**[See: API_MAPPING.md → Maps Endpoints](API_MAPPING.md#maps-endpoints)** ⚠️ CRITICAL: Large data handling
- [ ] Create `src/mcp_fred/api/endpoints/maps.py`
- [ ] Implement `get_shapes(shape)`
- [ ] Implement `get_series_group(series_id)`
- [ ] Implement `get_regional_data()`
- [ ] Implement `get_series_data(series_id)`

---

## Phase 3: Large Data Handling Utilities

**[See: ARCHITECTURE.md → Large Data Handling Strategy](ARCHITECTURE.md#large-data-handling-strategy)**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md → Large Data Handling Strategy (entire section)
- [ ] **Review Conservative Token Limits**: Understand Phase 0.4 decisions about 25% context usage
- [ ] **Identify Documentation Gaps**: Are utility patterns clearly documented?
- [ ] **Analyze Documentation Needs**: What would help with utility implementation?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Cross-References**: Ensure utility component documentation is complete

**Questions to Answer:**
1. Do we need UTILITY_PATTERNS.md with reusable code examples?
2. Should we create detailed token estimation algorithm documentation?
3. Do we need flow diagrams for async job lifecycle?
4. Should we document JSON to CSV conversion edge cases with examples?
5. Do we need SECURITY_GUIDE.md for path resolution and validation?
6. Should we add performance benchmarks for large dataset handling?
7. Any documentation about background worker architecture and concurrency?
8. Should we create PROJECT_STORAGE.md explaining directory organization?

---

### Token Estimation (using tiktoken)

**[See: ARCHITECTURE.md → Token Estimation](ARCHITECTURE.md#token-estimation)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
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

**[See: ARCHITECTURE.md → JSON to CSV Conversion](ARCHITECTURE.md#file-formats--json-to-csv-conversion)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
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

**[See: ARCHITECTURE.md → Streaming to Files](ARCHITECTURE.md#streaming-to-files)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
- [ ] Create `src/mcp_fred/utils/file_writer.py`
- [ ] Implement CSV writer with streaming support
- [ ] Implement JSON writer with streaming support
- [ ] Add chunked writing for large datasets
- [ ] Implement progress tracking during writes
- [ ] Add file size calculation and reporting
- [ ] Handle data type conversions for file formats
- [ ] Write unit tests for file writers

### Path Resolution & Security

**[See: ARCHITECTURE.md → Security & Validation](ARCHITECTURE.md#security--validation)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
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

**[See: ARCHITECTURE.md → Tool Parameter Design](ARCHITECTURE.md#tool-parameter-design)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
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

**[See: ARCHITECTURE.md → Configuration Management](ARCHITECTURE.md#configuration-management)**
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

**[See: ARCHITECTURE.md → Async Job Architecture](ARCHITECTURE.md#async-job-architecture)**
**[See: API_MAPPING.md → Utility Components](API_MAPPING.md#utility-components)**
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

**[See: ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)**
**[See: API_MAPPING.md](API_MAPPING.md) - Complete tool → endpoint → file mapping**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md → MCP Tool Design section
- [ ] **Review API Mappings**: Study complete API_MAPPING.md for all 12 tools
- [ ] **Review Tool Response Patterns**: Understand inline, file, and async job responses
- [ ] **Identify Documentation Gaps**: Are all tool patterns clearly documented?
- [ ] **Analyze Documentation Needs**: What would help with tool implementation?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Cross-References**: Ensure all tools link to architecture and API mapping

**Questions to Answer:**
1. Do we need TOOL_IMPLEMENTATION_GUIDE.md with step-by-step examples?
2. Should we create detailed operation routing pattern documentation?
3. Do we need comprehensive Pydantic schema examples for each tool?
4. Should we document the complete MCP protocol integration?
5. Do we need MCP_PROTOCOL.md explaining JSON-RPC communication?
6. Should we add tool testing examples with mock data?
7. Do we need USER_GUIDE.md showing how to use each tool from AI perspective?
8. Should we document tool discovery and registration process?
9. Any documentation about tool parameter validation patterns?
10. Should we create CONFIGURATION_GUIDE.md for all environment variables?

**Critical for This Phase:**
- Series tool handles 100K+ observations (async jobs required)
- Maps tool handles large shape files (file output preferred)
- Project management tools need directory scanning logic
- Job management tools need status tracking integration

---

### Configuration Management

**[See: ARCHITECTURE.md → Configuration Management](ARCHITECTURE.md#configuration-management)**
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

**[See: API_MAPPING.md → Category Endpoints](API_MAPPING.md#category-endpoints)**
- [ ] Create `src/mcp_fred/tools/category.py`
- [ ] Implement `fred_category` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Release Tool

**[See: API_MAPPING.md → Release Endpoints](API_MAPPING.md#release-endpoints)**
- [ ] Create `src/mcp_fred/tools/release.py`
- [ ] Implement `fred_release` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Series Tool

**[See: API_MAPPING.md → Series Endpoints](API_MAPPING.md#series-endpoints)** ⚠️ CRITICAL: Large data
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

**[See: API_MAPPING.md → Source Endpoints](API_MAPPING.md#source-endpoints)**
- [ ] Create `src/mcp_fred/tools/source.py`
- [ ] Implement `fred_source` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Tag Tool

**[See: API_MAPPING.md → Tag Endpoints](API_MAPPING.md#tag-endpoints)**
- [ ] Create `src/mcp_fred/tools/tag.py`
- [ ] Implement `fred_tag` tool
- [ ] Add operation routing logic
- [ ] Add parameter validation
- [ ] Add output handling (output, format, project, filename params)
- [ ] Integrate with `ResultOutputHandler` for large results
- [ ] Add error handling
- [ ] Write tool documentation

#### Maps Tool

**[See: API_MAPPING.md → Maps Endpoints](API_MAPPING.md#maps-endpoints)** ⚠️ CRITICAL: Large data
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

**[See: ARCHITECTURE.md → Async Job Management Tool](ARCHITECTURE.md#async-job-management-tool)**
**[See: API_MAPPING.md → Job Management Tools](API_MAPPING.md#job-management-tools)**
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

**[See: ARCHITECTURE.md → Project Management Tools](ARCHITECTURE.md#project-management-tools)**
**[See: API_MAPPING.md → Project Management Tools](API_MAPPING.md#project-management-tools)**
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

**[See: ARCHITECTURE.md → Transport Layer](ARCHITECTURE.md#transport-layer)**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md → Transport Layer section
- [ ] **Review MCP Protocol Specs**: Understand STDIO and Streamable HTTP protocols
- [ ] **Identify Documentation Gaps**: Are transport patterns clearly documented?
- [ ] **Analyze Documentation Needs**: What would help with transport implementation?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Cross-References**: Ensure transport documentation is complete

**Questions to Answer:**
1. Do we need TRANSPORT_GUIDE.md explaining both protocols in detail?
2. Should we create JSON-RPC message format examples?
3. Do we need DEPLOYMENT.md for different deployment scenarios?
4. Should we document how to test each transport protocol?
5. Do we need Claude Desktop integration examples?
6. Should we document HTTP transport authentication patterns?
7. Any documentation about transport error handling and recovery?
8. Should we create TROUBLESHOOTING.md for common transport issues?

---

### STDIO Transport

**[See: ARCHITECTURE.md → STDIO Transport](ARCHITECTURE.md#stdio-transport)**
- [ ] Create `src/mcp_fred/transports/stdio.py`
- [ ] Implement STDIO transport handler
- [ ] Add JSON-RPC message parsing
- [ ] Add stdin/stdout communication
- [ ] Add graceful shutdown handling
- [ ] Test with MCP client (Claude Desktop)

### Streamable HTTP Transport

**[See: ARCHITECTURE.md → Streamable HTTP Transport](ARCHITECTURE.md#streamable-http-transport)**
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

**[See: ARCHITECTURE.md → Testing Strategy](ARCHITECTURE.md#testing-strategy)**
**[See: API_MAPPING.md → Implementation Checklist](API_MAPPING.md#implementation-checklist)**

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Read ARCHITECTURE.md → Testing Strategy section
- [ ] **Review Implementation Checklist**: Study API_MAPPING.md implementation requirements
- [ ] **Identify Documentation Gaps**: Are testing patterns and strategies clearly documented?
- [ ] **Analyze Documentation Needs**: What would help with comprehensive testing?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Cross-References**: Ensure testing documentation covers all components

**Questions to Answer:**
1. Do we need TESTING_STRATEGY.md (Priority 2 doc) with detailed patterns?
2. Should we create TESTING_GUIDE.md with step-by-step testing procedures?
3. Do we need mock data examples for each FRED API endpoint?
4. Should we document test fixture organization and reuse?
5. Do we need COVERAGE_REQUIREMENTS.md by component type?
6. Should we create INTEGRATION_TESTING.md for end-to-end scenarios?
7. Any documentation about testing async job processing?
8. Should we document how to test with real FRED API (API key required)?
9. Do we need CI/CD pipeline documentation for automated testing?
10. Should we create TEST_DATA.md explaining mock data generation?

**Critical Testing Areas:**
- Token estimation accuracy (conservative limits)
- Async job lifecycle (accepted → processing → completed/failed)
- Large dataset handling (100K+ observations)
- File output and path security
- Project management directory operations
- Rate limit handling and retry logic

---

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

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review ALL Existing Documentation**: Complete audit of all docs created so far
- [ ] **Review User Perspective**: What does end user need to know?
- [ ] **Identify Documentation Gaps**: What's missing for user-facing documentation?
- [ ] **Analyze Documentation Needs**: What polishing and enhancement is needed?
- [ ] **Recommend Updates**: Propose comprehensive documentation improvements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Documentation Quality**: Ensure all docs are clear, accurate, complete

**Questions to Answer:**
1. Is README.md comprehensive enough for new users?
2. Do we need QUICK_START.md for getting started in 5 minutes?
3. Should we create EXAMPLES.md with real-world use cases?
4. Do we need TROUBLESHOOTING.md for common issues?
5. Should we document all error codes and messages?
6. Do we need API_REFERENCE.md for all 12 tools?
7. Should we create CONFIGURATION_REFERENCE.md for all env vars?
8. Do we need CONTRIBUTING.md for open source contributions?
9. Should we add diagrams and visualizations to documentation?
10. Do we need VIDEO_TUTORIALS.md links or creation plan?
11. Should we create FAQ.md addressing common questions?
12. Do we need PERFORMANCE.md documenting benchmarks?

**Documentation Audit Checklist:**
- [ ] All code has comprehensive docstrings
- [ ] All functions have type hints
- [ ] All tools documented with examples
- [ ] All configuration options documented
- [ ] All error messages documented
- [ ] Architecture diagrams current and accurate
- [ ] Cross-references all working correctly
- [ ] No broken links in documentation

---

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

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review Existing Documentation**: Ensure all user-facing docs are complete
- [ ] **Review Release Requirements**: Understand packaging and distribution needs
- [ ] **Identify Documentation Gaps**: What's needed for deployment and distribution?
- [ ] **Analyze Documentation Needs**: What would help with packaging and release?
- [ ] **Recommend Updates**: Propose new documentation or enhancements
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Verify Release Readiness**: Ensure all documentation is release-ready

**Questions to Answer:**
1. Do we need PACKAGING_GUIDE.md for creating distributions?
2. Should we create RELEASE_PROCESS.md documenting release workflow?
3. Do we need PYPI_PUBLISHING.md for PyPI publication?
4. Should we document Docker deployment?
5. Do we need INSTALLATION_VERIFICATION.md for testing installs?
6. Should we create UPGRADE_GUIDE.md for version migrations?
7. Do we need VERSIONING_POLICY.md explaining semantic versioning?
8. Should we document release checklist and verification steps?
9. Do we need SECURITY_DISCLOSURE.md for security issues?
10. Should we create SUPPORT.md explaining support channels?

**Release Documentation Checklist:**
- [ ] CHANGELOG.md complete with all changes
- [ ] README.md ready for PyPI display
- [ ] LICENSE file present and correct
- [ ] All version numbers consistent
- [ ] Installation instructions verified
- [ ] Configuration examples tested
- [ ] All links in documentation working
- [ ] Release notes drafted

---

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

### 📋 Pre-Phase Documentation Review (REQUIRED BEFORE STARTING)

**Before implementing any tasks in this phase:**
- [ ] **Review User Feedback**: Analyze actual usage patterns and feature requests
- [ ] **Review Performance Metrics**: Understand bottlenecks and optimization opportunities
- [ ] **Identify Documentation Gaps**: What new features need documentation?
- [ ] **Analyze Documentation Needs**: How to document enhancements and new features?
- [ ] **Recommend Updates**: Propose documentation for future features
- [ ] **Get User Approval**: Present recommendations and wait for approval
- [ ] **Create/Update Documentation**: Implement approved changes
- [ ] **Plan Documentation Strategy**: Ensure enhancement docs integrate with existing docs

**Questions to Answer:**
1. Do we need ROADMAP.md for future features and timeline?
2. Should we create ENHANCEMENT_PROPOSALS.md for tracking ideas?
3. Do we need PERFORMANCE_OPTIMIZATION.md documenting tuning?
4. Should we document caching strategies and implementation?
5. Do we need MONITORING_GUIDE.md for observability?
6. Should we create ANALYTICS.md for usage tracking?
7. Do we need FEEDBACK_PROCESS.md for collecting user input?
8. Should we document experimental features separately?
9. Do we need DEPRECATION_POLICY.md for removing features?
10. Should we create COMMUNITY.md for user community building?

**Enhancement Documentation Strategy:**
- Document experimental features clearly
- Mark deprecated features with timeline
- Provide migration guides for breaking changes
- Document performance improvements with benchmarks
- Create upgrade guides for each enhancement
- Maintain backward compatibility documentation

---

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

### Development Workflow

- **Documentation First**: Complete "Pre-Phase Documentation Review" section before any implementation
- **User Approval Required**: Get user approval for documentation recommendations before proceeding
- **Implementation Order**: Complete tasks in order by phase
- **Progress Tracking**: Move completed tasks to PROGRESS.md
- **Changelog Updates**: Update CHANGELOG.md after completing each phase
- **Testing Required**: Run tests before marking a phase as complete
- **Commit Conventions**: Use conventional commits for all git commits

### Documentation Review Process

Each phase includes a **📋 Pre-Phase Documentation Review** section that MUST be completed before implementation:

1. **Review**: Read all relevant existing documentation
2. **Analyze**: Identify gaps, needed updates, and new documentation
3. **Recommend**: Present specific documentation proposals to user
4. **Approve**: Wait for user approval of recommendations
5. **Create**: Implement approved documentation changes
6. **Verify**: Ensure all cross-references and links work correctly
7. **Proceed**: Only then begin phase implementation

### Why Documentation Reviews Matter

- **Context Continuity**: Ensures new AI contexts have complete information
- **Architecture Clarity**: Keeps design decisions documented as project evolves
- **User Experience**: Provides comprehensive guides for end users
- **Team Collaboration**: Enables future contributors to understand the project
- **Quality Assurance**: Documents patterns, standards, and best practices
- **Problem Prevention**: Identifies potential issues before implementation

### Documentation Quality Standards

All documentation should be:
- **Accurate**: Reflects actual implementation and decisions
- **Complete**: Covers all necessary information
- **Clear**: Easy to understand for target audience
- **Consistent**: Uses same terminology and format throughout
- **Current**: Updated with each change
- **Cross-Referenced**: Properly linked to related documentation
- **Navigable**: Easy to find information quickly
- **Self-Contained**: No dependency on external tools (Jira, Confluence, etc.)
