# MCP-FRED Architecture

## Overview

This document outlines the architecture and design decisions for the FRED MCP (Model Context Protocol) Server.

---

## Technology Stack

### Core Framework
- **Language:** Python 3.11+
- **Web Framework:** FastAPI
- **MCP Protocol:** Python MCP SDK

### Development Tools
- **Linter/Formatter:** Ruff
- **Testing Framework:** pytest
- **Dependency Management:** pip + requirements.txt (or Poetry TBD)

### Transport Protocols
- **STDIO:** For local communication (MCP client runs server as subprocess)
- **Streamable HTTP:** For remote communication (modern MCP standard)

---

## Project Structure

```
mcp-fred/
├── src/
│   ├── mcp_fred/
│   │   ├── __init__.py
│   │   ├── server.py           # Main MCP server entry point
│   │   ├── config.py           # Configuration management
│   │   ├── transports/
│   │   │   ├── __init__.py
│   │   │   ├── stdio.py        # STDIO transport implementation
│   │   │   └── http.py         # Streamable HTTP transport implementation
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── client.py       # FRED API HTTP client
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── category.py
│   │   │   │   ├── release.py
│   │   │   │   ├── series.py
│   │   │   │   ├── source.py
│   │   │   │   ├── tag.py
│   │   │   │   └── maps.py
│   │   │   └── models/
│   │   │       ├── __init__.py
│   │   │       └── responses.py  # Pydantic models for API responses
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── output_handler.py    # Smart output handling (file vs screen)
│   │   │   ├── token_estimator.py   # Token counting with tiktoken
│   │   │   ├── file_writer.py       # CSV/JSON streaming to files
│   │   │   ├── json_to_csv.py       # JSON to CSV converter
│   │   │   ├── path_resolver.py     # Secure path resolution and validation
│   │   │   ├── job_manager.py       # Async job management and tracking
│   │   │   └── background_worker.py # Background job processing
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── category.py      # MCP tool: fred_category
│   │       ├── release.py       # MCP tool: fred_release
│   │       ├── series.py        # MCP tool: fred_series
│   │       ├── source.py        # MCP tool: fred_source
│   │       ├── tag.py           # MCP tool: fred_tag
│   │       ├── maps.py          # MCP tool: fred_maps
│   │       ├── job_status.py    # MCP tool: fred_job_status
│   │       ├── job_list.py      # MCP tool: fred_job_list (optional)
│   │       ├── job_cancel.py    # MCP tool: fred_job_cancel (optional)
│   │       ├── project_list.py  # MCP tool: fred_project_list
│   │       ├── project_create.py # MCP tool: fred_project_create
│   │       └── project_files.py # MCP tool: fred_project_files
├── tests/
│   ├── __init__.py
│   ├── test_tools/
│   ├── test_api/
│   ├── test_utils/              # Tests for output handling
│   └── test_integration/
├── docs/
│   ├── ARCHITECTURE.md          # This file
│   ├── FRED_API_REFERENCE.md    # FRED API documentation
│   ├── TODO.md                  # Development tasks
│   ├── PROGRESS.md              # Completed tasks
│   └── USER_GUIDE.md            # End-user documentation
├── .env.example                 # Example environment variables
├── pyproject.toml               # Ruff configuration
├── requirements.txt             # Python dependencies
├── pytest.ini                   # pytest configuration
├── CHANGELOG.md                 # Version history
├── README.md                    # Project README
└── LICENSE                      # License file
```

---

## Large Data Handling Strategy

### Problem Statement

FRED API can return very large datasets:
- Series observations: up to 100,000 observations per request
- Maps/GeoFRED data: geographical data with shape files
- Historical data: decades of daily/monthly observations
- Rate limits: 120 requests per minute

Large datasets can exceed AI model token limits and cause performance issues.

### Solution: Smart Output Handling

Inspired by Snowflake MCP server's approach, we implement intelligent data storage:

#### 1. **Output Modes**

- **`auto`** (default): Server automatically decides based on data size vs token limits
- **`screen`**: Force inline return to AI agent (for small results)
- **`file`**: Force file storage (for large datasets or permanent storage)

#### 2. **Project-Based Storage**

Data is organized by project in a user-configurable directory:
```
{FRED_STORAGE_DIR}/
└── {project-name}/
    ├── series/
    │   ├── GNPCA_observations_20251008_143022.csv
    │   └── GNPCA_observations_20251008_143022.json
    ├── maps/
    │   ├── regional_data_20251008_150030.csv
    │   └── shapes_california_20251008_150045.json
    └── releases/
        └── release_53_series_20251008_151500.csv
```

**Key Environment Variables:**
- `FRED_STORAGE_DIR`: **User-configurable root directory** for all FRED data storage
  - Required for file output operations
  - Can be any directory on user's local filesystem
  - Example: `/Users/username/Documents/fred-data` or `C:\Users\username\fred-data`
  - **Default**: `./fred-data` (relative to current working directory)
- `FRED_PROJECT_NAME`: Current project name for organizing data (default: `default`)

**Security Notes:**
- Storage directory is completely user-controlled
- No writes to MCP server installation directory
- Path validation prevents directory traversal
- Write permissions validated before operations

#### 3. **Token Estimation**

Using **tiktoken** library for accurate token counting:

```python
import tiktoken

class TokenEstimator:
    def __init__(self):
        # tiktoken is lightweight (~2.7 MB installed)
        # Supports multiple model encodings
        self.encodings = {
            'claude': tiktoken.get_encoding('cl100k_base'),  # Claude approximation
            'gpt-4': tiktoken.get_encoding('cl100k_base'),
            'gpt-3.5': tiktoken.get_encoding('cl100k_base'),
        }

    def estimate_tokens(self, data: List[Dict], model: str = 'gpt-4') -> int:
        """Estimate token count using tiktoken"""
        # Sample first N rows
        # Use tiktoken to count tokens accurately
        # Extrapolate for full dataset
        pass

    def should_use_file(self, estimated_tokens: int, model_limit: int) -> bool:
        """Decide if data should go to file"""
        safety_margin = 0.7  # 70% of limit
        return estimated_tokens > (model_limit * safety_margin)
```

**Why tiktoken?**
- Accurate token counting (OpenAI's official library)
- Lightweight: ~2.7 MB installed size
- Supports multiple model encodings
- Widely used and well-maintained

**Model Token Limits (Conservative Approach):**

The token limits assume that the AI agent's context window is already partially consumed by:
- Chat history with the user
- Other MCP server responses
- System prompts and tool definitions
- Ongoing conversation context

**Conservative Safe Thresholds (25% of total capacity):**
- Claude Sonnet: ~200K total context (safe threshold: **50K**)
- GPT-4: ~100K total context (safe threshold: **25K**)
- Gemini Pro: ~1M total context (safe threshold: **250K**)

**Rationale:**
We err on the side of saving to file more often to:
1. Prevent context overflow from competing MCP servers
2. Account for existing chat history
3. Leave room for agent reasoning and response generation
4. Provide stable, predictable behavior

**Configuration:**
```bash
FRED_SAFE_TOKEN_LIMIT=50000          # Override safe threshold for auto mode
FRED_ASSUME_CONTEXT_USED=0.75        # Assume 75% of context already used
```

#### 4. **Streaming to Files**

For large datasets, stream results directly to files in chunks:

```python
async def stream_to_file(
    series_id: str,
    observations: AsyncIterator,
    format: str = "csv",
    project: str = "default"
) -> Dict[str, Any]:
    """
    Stream FRED data to file in chunks

    Returns:
        {
            "status": "success",
            "file_path": "/path/to/file.csv",
            "rows_written": 45000,
            "file_size_mb": 2.3,
            "message": "Data saved. Processing complete."
        }
    """
```

#### 5. **Async Job Management for Large Requests**

For large datasets, use background job processing with status tracking:

**Job Creation (Immediate Response):**

```json
{
  "status": "accepted",
  "job_id": "fred-job-a3f2b8c4-20251008-143022",
  "message": "Large dataset detected. Processing in background...",
  "estimated_rows": 75000,
  "estimated_time_seconds": 45,
  "output_mode": "file",
  "project": "economic-analysis",
  "check_status": "Use fred_job_status tool with this job_id"
}
```

**Job Status Checking:**

AI agent can check status anytime using `fred_job_status` tool:

```python
# Tool call
{
  "tool": "fred_job_status",
  "job_id": "fred-job-a3f2b8c4-20251008-143022"
}
```

**Status Responses:**

**In Progress:**
```json
{
  "job_id": "fred-job-a3f2b8c4-20251008-143022",
  "status": "processing",
  "progress": {
    "rows_fetched": 35000,
    "estimated_total": 75000,
    "percent_complete": 47,
    "elapsed_seconds": 18
  },
  "message": "Fetching observations from FRED API..."
}
```

**Completed:**
```json
{
  "job_id": "fred-job-a3f2b8c4-20251008-143022",
  "status": "completed",
  "duration_seconds": 42,
  "result": {
    "file_path": "/Users/username/Documents/fred-data/economic-analysis/series/GNPCA_observations_20251008_143022.csv",
    "rows_written": 75234,
    "file_size_mb": 3.2,
    "format": "csv"
  },
  "message": "Data successfully saved to file. Ready for analysis."
}
```

**Failed:**
```json
{
  "job_id": "fred-job-a3f2b8c4-20251008-143022",
  "status": "failed",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "FRED API rate limit exceeded (120 req/min). Job will retry automatically."
  },
  "retry_count": 1,
  "next_retry_in_seconds": 30
}
```

### Async Job Architecture

**Job Storage:**
```python
# In-memory job tracking (or Redis for production)
jobs = {
    "job_id": {
        "status": "processing",  # accepted, processing, completed, failed
        "created_at": datetime,
        "updated_at": datetime,
        "request": {...},  # Original request params
        "progress": {...},
        "result": {...},
        "error": {...}
    }
}
```

**Job Lifecycle:**
1. **Request received** → Estimate size
2. **If large** → Create job, return job_id immediately
3. **Background processing** → Fetch from FRED API, write to file
4. **Update status** → Progress tracking
5. **Complete** → File saved, status = completed
6. **AI checks status** → Returns result when ready

**Job Cleanup:**
- Jobs retained for 24 hours after completion
- Auto-cleanup of old jobs
- Configurable retention via `FRED_JOB_RETENTION_HOURS`

**When to Use Async Jobs:**
- Series observations > 10,000 rows
- Maps data with shape files
- Multiple paginated requests required
- Estimated processing time > 10 seconds

#### 6. **File Formats & JSON to CSV Conversion**

**FRED API Response Formats:**
- FRED API returns: **JSON** or **XML**
- MCP Server default: **JSON** (XML only if explicitly requested)

**MCP Server Output Formats:**
- **CSV**: Human-readable, Excel-compatible, good for time series
- **JSON**: Structured data, programmatic access, preserves data types
- **Parquet** (future): Columnar format for analytics

**JSON to CSV Conversion Strategy:**

Since FRED API doesn't natively return CSV, we provide a convenience conversion:

```python
class JSONToCSVConverter:
    def convert(self, json_data: dict, format_type: str = 'csv') -> Union[str, dict]:
        """
        Convert FRED JSON response to CSV format

        Handles:
        - Series observations (time series data)
        - Multiple data structures (observations, categories, releases)
        - Nested JSON structures flattened to CSV rows
        """
        if format_type == 'csv':
            # Extract observations/data array from JSON
            # Flatten nested structures
            # Convert to CSV with proper headers
            return csv_string
        else:
            # Return original JSON
            return json_data
```

**Why JSON to CSV Conversion?**
- Standardized output across different MCP servers (Snowflake returns CSV, we should too)
- Common format for data analysis workflows
- Excel compatibility for business users
- No need for AI agents to handle format conversions

**Conversion Examples:**

Series observations JSON:
```json
{
  "observations": [
    {"date": "2023-01-01", "value": "25683.8"},
    {"date": "2023-02-01", "value": "25820.4"}
  ]
}
```

Converts to CSV:
```csv
date,value
2023-01-01,25683.8
2023-02-01,25820.4
```

#### 7. **Filename Generation**

Auto-generate descriptive filenames:

**Pattern Variables:**
- `{series_id}`: FRED series ID (e.g., GNPCA)
- `{operation}`: Operation type (observations, search, etc.)
- `{date}`: Current date (YYYYMMDD)
- `{time}`: Current time (HHMMSS)
- `{project}`: Project name
- `{query_hash}`: Short hash of query parameters

**Example Patterns:**
- `{series_id}_{operation}_{date}_{time}` → `GNPCA_observations_20251008_143022.csv`
- `{operation}_{query_hash}_{timestamp}` → `search_a3f2b8_20251008143022.json`
- Custom: User can specify exact filename

#### 8. **Security & Validation**

**Directory Security:**
- NEVER write to MCP server installation directory
- Require `MCP_CLIENT_ROOT` to be set
- Validate all paths to prevent directory traversal
- Check write permissions before starting large downloads

**Filename Validation:**
- Block invalid characters: `<>:"|?*`
- Block reserved names (Windows): `CON`, `PRN`, `AUX`, etc.
- Sanitize user-provided filenames

#### 9. **Tool Parameter Design**

Each tool accepts optional output parameters:

```python
@mcp.tool()
async def fred_series(
    operation: str,
    series_id: Optional[str] = None,
    # ... other operation-specific params ...
    output: str = "auto",          # auto, screen, file
    format: str = "csv",            # csv, json, parquet
    project: Optional[str] = None,  # project name for organization
    filename: Optional[str] = None, # custom filename
    **kwargs
) -> dict:
    """FRED Series operations with smart output handling"""
```

**Parameter Precedence:**
1. User-specified parameters (highest priority)
2. Project-level configuration
3. Environment variable defaults
4. Hard-coded defaults (lowest priority)

#### 10. **Progress Feedback**

For large operations, provide progress updates:

```python
{
    "status": "in_progress",
    "progress": {
        "rows_fetched": 25000,
        "estimated_total": 50000,
        "percent_complete": 50,
        "elapsed_seconds": 15
    }
}
```

---

## Configuration Management

### Environment Variables

The server supports configuration via environment variables:

```bash
# FRED API Configuration
FRED_API_KEY=your_api_key_here          # Required: FRED API key
FRED_BASE_URL=https://api.stlouisfed.org # Optional: Override base URL

# MCP Transport Configuration
MCP_TRANSPORT=stdio                      # Optional: stdio or http
MCP_HTTP_HOST=0.0.0.0                   # Optional: HTTP server host
MCP_HTTP_PORT=8000                       # Optional: HTTP server port

# Large Data Handling Configuration
FRED_STORAGE_DIR=/path/to/fred-data    # User-configurable storage directory (default: ./fred-data)
FRED_PROJECT_NAME=default               # Optional: Project name for organization
FRED_OUTPUT_MODE=auto                   # Optional: auto, screen, or file
FRED_OUTPUT_FORMAT=csv                  # Optional: csv or json (CSV via JSON conversion)
FRED_FILENAME_PATTERN={series_id}_{operation}_{date}_{time}  # Optional

# Token Management (for auto mode)
FRED_MODEL_NAME=claude-sonnet-4         # Optional: AI model name for token limits
FRED_MODEL_TOKEN_LIMIT=200000           # Optional: Model's token context limit
FRED_SAFETY_MARGIN=0.7                  # Optional: Safety margin (0.0-1.0)
FRED_SCREEN_ROW_THRESHOLD=1000          # Optional: Max rows for screen output
```

### Configuration Sources (Priority Order)

1. **MCP Client Configuration** - When using STDIO transport, the MCP client config can pass environment variables
2. **Environment Variables** - From `.env` file or system environment
3. **Default Values** - Fallback to sensible defaults

### Example MCP Client Configuration (STDIO)

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "mcp_fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here",
        "FRED_STORAGE_DIR": "/Users/username/Documents/fred-data"
      }
    }
  }
}
```

**Minimal Configuration (uses defaults):**
```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "mcp_fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```
*Note: Without `FRED_STORAGE_DIR`, defaults to `./fred-data` in current working directory*

**Advanced Configuration:**
```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "mcp_fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here",
        "FRED_STORAGE_DIR": "/Users/username/Documents/fred-data",
        "FRED_PROJECT_NAME": "economic-analysis",
        "FRED_OUTPUT_MODE": "auto",
        "FRED_OUTPUT_FORMAT": "csv"
      }
    }
  }
}
```

### Example .env File (Local Server)

```bash
# Required
FRED_API_KEY=your_api_key_here

# Storage Configuration
FRED_STORAGE_DIR=/Users/username/Documents/fred-data
FRED_PROJECT_NAME=my-project
FRED_OUTPUT_FORMAT=csv

# MCP Transport
MCP_TRANSPORT=http
MCP_HTTP_HOST=127.0.0.1
MCP_HTTP_PORT=8000
```

---

## Async Job Management Tool

### fred_job_status Tool

Dedicated tool for checking async job status:

```python
@mcp.tool()
async def fred_job_status(
    job_id: str
) -> dict:
    """
    Check the status of a background FRED data job

    Args:
        job_id: The job ID returned when the request was initiated

    Returns:
        Job status with progress, result, or error information
    """
    pass
```

### fred_job_list Tool (Optional)

List recent jobs for the current session:

```python
@mcp.tool()
async def fred_job_list(
    status_filter: Optional[str] = None,  # completed, processing, failed
    limit: int = 10
) -> dict:
    """List recent FRED data jobs"""
    pass
```

### fred_job_cancel Tool (Optional)

Cancel a running job:

```python
@mcp.tool()
async def fred_job_cancel(
    job_id: str
) -> dict:
    """Cancel a running FRED data job"""
    pass
```

---

## Project Management Tools

To help users organize their FRED data storage, the server provides project management helper tools:

### fred_project_list Tool

List all existing projects in the FRED storage directory:

```python
@mcp.tool()
async def fred_project_list() -> dict:
    """
    List all FRED data projects in the storage directory

    Scans FRED_STORAGE_DIR to discover existing project directories

    Returns:
        {
            "status": "success",
            "storage_dir": "/Users/username/Documents/fred-data",
            "projects": [
                {
                    "name": "economic-analysis",
                    "path": "/Users/username/Documents/fred-data/economic-analysis",
                    "file_count": 45,
                    "total_size_mb": 23.4,
                    "created_date": "2025-10-01",
                    "last_modified": "2025-10-08"
                },
                {
                    "name": "gdp-research",
                    "path": "/Users/username/Documents/fred-data/gdp-research",
                    "file_count": 12,
                    "total_size_mb": 5.2,
                    "created_date": "2025-09-15",
                    "last_modified": "2025-09-20"
                }
            ],
            "total_projects": 2,
            "total_storage_mb": 28.6
        }
    """
    pass
```

### fred_project_create Tool

Create a new project directory:

```python
@mcp.tool()
async def fred_project_create(
    project_name: str,
    description: Optional[str] = None
) -> dict:
    """
    Create a new FRED data project directory

    Args:
        project_name: Name for the new project (alphanumeric, hyphens, underscores)
        description: Optional description of the project

    Returns:
        {
            "status": "success",
            "project_name": "inflation-study",
            "project_path": "/Users/username/Documents/fred-data/inflation-study",
            "subdirectories_created": ["series", "maps", "releases"],
            "message": "Project 'inflation-study' created successfully"
        }
    """
    pass
```

**Project Directory Structure:**

When a new project is created, it automatically includes:

```
{FRED_STORAGE_DIR}/{project-name}/
├── series/       # Series observations and metadata
├── maps/         # GeoFRED data and shape files
├── releases/     # Release data
├── categories/   # Category data
├── sources/      # Source data
├── tags/         # Tag data
└── .project.json # Project metadata (description, created date, etc.)
```

### fred_project_files Tool

List all files in a specific project:

```python
@mcp.tool()
async def fred_project_files(
    project_name: str,
    subdirectory: Optional[str] = None,  # Filter by: series, maps, releases, etc.
    sort_by: str = "modified",            # Sort by: name, size, modified
    limit: int = 100
) -> dict:
    """
    List files in a FRED data project

    Args:
        project_name: Name of the project
        subdirectory: Optional filter (series, maps, releases, categories, sources, tags)
        sort_by: Sort order (name, size, modified, created)
        limit: Maximum files to return

    Returns:
        {
            "status": "success",
            "project_name": "economic-analysis",
            "project_path": "/Users/username/Documents/fred-data/economic-analysis",
            "files": [
                {
                    "name": "GNPCA_observations_20251008_143022.csv",
                    "path": "series/GNPCA_observations_20251008_143022.csv",
                    "full_path": "/Users/username/.../economic-analysis/series/GNPCA_observations_20251008_143022.csv",
                    "size_mb": 3.2,
                    "rows": 75234,
                    "created": "2025-10-08T14:30:22",
                    "modified": "2025-10-08T14:30:45",
                    "format": "csv"
                },
                {
                    "name": "inflation_search_20251007_091500.json",
                    "path": "series/inflation_search_20251007_091500.json",
                    "full_path": "/Users/username/.../economic-analysis/series/inflation_search_20251007_091500.json",
                    "size_mb": 0.8,
                    "created": "2025-10-07T09:15:00",
                    "modified": "2025-10-07T09:15:03",
                    "format": "json"
                }
            ],
            "total_files": 45,
            "total_size_mb": 23.4
        }
    """
    pass
```

### Project Management Workflow

**Typical User Experience:**

1. **User starts new analysis:**
   - AI: "Would you like to use an existing project or create a new one?"
   - AI calls `fred_project_list` to show available projects

2. **User chooses to create new project:**
   - User: "Create a new project called 'inflation-study'"
   - AI calls `fred_project_create` with name="inflation-study"

3. **User requests FRED data:**
   - User: "Get GDP data for the last 10 years"
   - AI calls `fred_series` with project="inflation-study"
   - Data automatically saved to `/fred-data/inflation-study/series/`

4. **User wants to review collected data:**
   - User: "What data have I collected for this project?"
   - AI calls `fred_project_files` with project_name="inflation-study"
   - Shows list of all files with metadata

**Benefits:**
- Organization: Data grouped by analysis project
- Discovery: Easy to find existing projects and data
- Reusability: Projects can be resumed across sessions
- Cleanup: Easy to identify and remove old projects

---

## MCP Tool Design

### Tool Structure

Each tool follows a consistent pattern with an `operation` parameter to handle multiple related endpoints:

```python
@mcp.tool()
async def fred_category(
    operation: str,
    category_id: Optional[int] = None,
    **kwargs
) -> dict:
    """
    FRED Category operations

    Args:
        operation: One of: get, list_children, get_related, get_series,
                   get_tags, get_related_tags
        category_id: Category ID (required for most operations)
        **kwargs: Additional operation-specific parameters
    """
    pass
```

### Implemented Tools

#### Core FRED Data Tools

| Tool Name | Operations | Endpoints Covered |
|-----------|-----------|-------------------|
| `fred_category` | `get`, `list_children`, `get_related`, `get_series`, `get_tags`, `get_related_tags` | `/category/*` |
| `fred_release` | `list`, `get`, `get_dates`, `get_series`, `get_sources`, `get_tags`, `get_related_tags`, `get_tables` | `/releases/*`, `/release/*` |
| `fred_series` | `get`, `search`, `get_categories`, `get_observations`, `get_release`, `get_tags`, `search_tags`, `search_related_tags`, `get_updates`, `get_vintage_dates` | `/series/*` |
| `fred_source` | `list`, `get`, `get_releases` | `/sources/*`, `/source/*` |
| `fred_tag` | `list`, `get_related_tags`, `get_series` | `/tags/*`, `/related_tags` |
| `fred_maps` | `get_shapes`, `get_series_group`, `get_regional_data`, `get_series_data` | `/geofred/*` |

#### Job Management Tools

| Tool Name | Purpose | Required |
|-----------|---------|----------|
| `fred_job_status` | Check status of async background jobs | **Yes** |
| `fred_job_list` | List recent jobs with filtering | Optional |
| `fred_job_cancel` | Cancel running background jobs | Optional |

#### Project Management Tools

| Tool Name | Purpose | Required |
|-----------|---------|----------|
| `fred_project_list` | List all projects in storage directory | **Yes** |
| `fred_project_create` | Create new project directory structure | **Yes** |
| `fred_project_files` | List files within a specific project | **Yes** |

### Tool Response Format

All tools return structured data matching the FRED API response format, with minimal transformation to preserve data fidelity.

---

## API Client Architecture

### HTTP Client Layer

- **Base Client:** `api/client.py` - Handles HTTP requests, authentication, error handling
- **Endpoint Modules:** `api/endpoints/*.py` - Encapsulate endpoint-specific logic
- **Response Models:** `api/models/responses.py` - Pydantic models for validation

### Design Principles

1. **Separation of Concerns:** API client logic separate from MCP tool logic
2. **Type Safety:** Use Pydantic models for request/response validation
3. **Error Handling:** Graceful handling of API errors with meaningful messages
4. **Testability:** API client can be tested independently from MCP layer

### API Client Example

```python
class FREDClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    async def get(self, endpoint: str, params: dict) -> dict:
        """Make GET request to FRED API"""
        params['api_key'] = self.api_key
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
```

### Rate Limiting & Retry Logic

**FRED API Limits:**
- 120 requests per minute
- Exceeding limit returns HTTP 429 (Too Many Requests)

**Retry Strategy:**
- **Exponential Backoff:** Wait time = `base_delay * (2 ^ attempt)` with jitter
- **Max Retries:** 3 attempts for rate limits (429), 2 for server errors (500+)
- **Retry Conditions:**
  - 429 (Rate Limit): Always retry with backoff
  - 500, 502, 503, 504 (Server Errors): Retry with backoff
  - 401, 400, 404 (Client Errors): No retry, fail immediately
- **Jitter:** Add random variance (±25%) to prevent thundering herd

**Circuit Breaker Pattern:**
- Track consecutive failures per endpoint
- Open circuit after 5 consecutive failures (stop making requests)
- Half-open after cooldown period (60 seconds)
- Close circuit on successful request

**Implementation Expectations:**
- Use decorators or middleware for retry logic
- Track rate limit windows (60-second sliding window)
- Log retry attempts with backoff times
- Expose metrics: retry count, circuit breaker state, rate limit hits

**Configuration:**
- `FRED_RATE_LIMIT_PER_MINUTE` (default: 120)
- `FRED_RATE_LIMIT_RETRY_DELAY` (default: 60 seconds)
- `FRED_MAX_RETRIES` (default: 3 for 429, 2 for 5xx)
- `FRED_CIRCUIT_BREAKER_THRESHOLD` (default: 5 failures)

**Testing Requirements:**
- Verify exponential backoff calculation
- Test circuit breaker state transitions
- Mock 429 responses and verify retry behavior
- Test that 401/400/404 don't trigger retries

---

## Transport Layer

### STDIO Transport

- **Use Case:** Local MCP client integration (Claude Desktop, etc.)
- **Communication:** JSON-RPC over stdin/stdout
- **Process Model:** MCP server runs as subprocess of client
- **Lifecycle:** Server starts when client initializes, stops when client disconnects

### Streamable HTTP Transport

- **Use Case:** Remote MCP server deployment
- **Communication:** HTTP POST for messages, optional SSE for streaming
- **Endpoint:** Single endpoint (e.g., `/mcp`)
- **Authentication:** Supports bearer tokens, API keys, custom headers

---

## Error Handling Strategy

### Error Types

1. **Configuration Errors:** Missing API key, invalid configuration
2. **API Errors:** FRED API returns error response (400, 401, 404, 429, 500)
3. **Network Errors:** Connection failures, timeouts
4. **Validation Errors:** Invalid parameters passed to tools
5. **File System Errors:** Permission denied, disk full, path not found
6. **Job Errors:** Job not found, job failed, job timeout

### Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "endpoint": "/fred/series",
      "status_code": 404
    }
  }
}
```

### Error Handling Patterns

#### Pattern 1: API Client Error Handling

```python
# src/mcp_fred/api/client.py

import httpx
from typing import Dict, Any
from pydantic import ValidationError

class FREDAPIError(Exception):
    """Base exception for FRED API errors"""
    def __init__(self, code: str, message: str, details: Dict[str, Any] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class FREDClient:
    async def get(self, endpoint: str, params: dict) -> dict:
        """Make GET request to FRED API with comprehensive error handling"""
        params['api_key'] = self.api_key

        try:
            response = await self.client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            # Handle HTTP errors with specific messages
            status_code = e.response.status_code

            if status_code == 400:
                raise FREDAPIError(
                    code="INVALID_REQUEST",
                    message="Invalid parameters provided to FRED API",
                    details={
                        "endpoint": endpoint,
                        "params": params,
                        "status_code": 400
                    }
                )
            elif status_code == 401:
                raise FREDAPIError(
                    code="INVALID_API_KEY",
                    message="FRED API key is invalid or missing",
                    details={"status_code": 401}
                )
            elif status_code == 404:
                raise FREDAPIError(
                    code="NOT_FOUND",
                    message=f"Resource not found: {endpoint}",
                    details={"endpoint": endpoint, "status_code": 404}
                )
            elif status_code == 429:
                raise FREDAPIError(
                    code="RATE_LIMIT_EXCEEDED",
                    message="FRED API rate limit exceeded (120 req/min)",
                    details={"status_code": 429, "retry_after": 60}
                )
            elif status_code >= 500:
                raise FREDAPIError(
                    code="SERVER_ERROR",
                    message="FRED API server error",
                    details={"status_code": status_code}
                )
            else:
                raise FREDAPIError(
                    code="HTTP_ERROR",
                    message=f"HTTP error {status_code}",
                    details={"status_code": status_code}
                )

        except httpx.TimeoutException:
            raise FREDAPIError(
                code="TIMEOUT",
                message="Request to FRED API timed out",
                details={"endpoint": endpoint, "timeout_seconds": 30}
            )

        except httpx.NetworkError as e:
            raise FREDAPIError(
                code="NETWORK_ERROR",
                message="Network error connecting to FRED API",
                details={"error": str(e)}
            )

        except ValidationError as e:
            raise FREDAPIError(
                code="VALIDATION_ERROR",
                message="Response validation failed",
                details={"errors": e.errors()}
            )
```

#### Pattern 2: MCP Tool Error Handling

```python
# src/mcp_fred/tools/series.py

from typing import Dict, Any
from pydantic import BaseModel, ValidationError

class SeriesToolParams(BaseModel):
    operation: str
    series_id: str | None = None
    output: str = "auto"
    format: str = "csv"
    project: str | None = None

@mcp.tool()
async def fred_series(
    operation: str,
    series_id: str | None = None,
    **kwargs
) -> Dict[str, Any]:
    """
    FRED Series operations with comprehensive error handling

    Returns:
        Success response or error response in standard format
    """
    try:
        # Validate parameters
        params = SeriesToolParams(
            operation=operation,
            series_id=series_id,
            **kwargs
        )

        # Validate operation type
        valid_operations = [
            "get", "search", "get_categories", "get_observations",
            "get_release", "get_tags", "search_tags",
            "search_related_tags", "get_updates", "get_vintage_dates"
        ]

        if params.operation not in valid_operations:
            return {
                "error": {
                    "code": "INVALID_OPERATION",
                    "message": f"Invalid operation: {operation}",
                    "details": {
                        "valid_operations": valid_operations
                    }
                }
            }

        # Validate series_id for operations that require it
        requires_series_id = [
            "get", "get_categories", "get_observations",
            "get_release", "get_tags", "get_vintage_dates"
        ]

        if params.operation in requires_series_id and not params.series_id:
            return {
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": f"Operation '{operation}' requires series_id",
                    "details": {
                        "required_parameter": "series_id",
                        "operation": operation
                    }
                }
            }

        # Execute operation
        if params.operation == "get_observations":
            result = await get_series_observations(
                series_id=params.series_id,
                output=params.output,
                format=params.format,
                project=params.project
            )
            return result

        # ... other operations

    except ValidationError as e:
        return {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Parameter validation failed",
                "details": {"errors": e.errors()}
            }
        }

    except FREDAPIError as e:
        # Pass through API errors
        return {
            "error": {
                "code": e.code,
                "message": e.message,
                "details": e.details
            }
        }

    except Exception as e:
        # Catch-all for unexpected errors
        return {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
                "details": {
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            }
        }
```

#### Pattern 3: File System Error Handling

```python
# src/mcp_fred/utils/path_resolver.py

import os
from pathlib import Path

class PathSecurityError(Exception):
    """Raised when path validation fails for security reasons"""
    pass

class PathResolver:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir).resolve()

    def resolve_path(self, project: str, filename: str) -> Path:
        """
        Resolve and validate file path with comprehensive error handling

        Raises:
            PathSecurityError: If path validation fails
            PermissionError: If write permissions are denied
            OSError: If filesystem errors occur
        """
        try:
            # Validate storage directory exists
            if not self.storage_dir.exists():
                try:
                    self.storage_dir.mkdir(parents=True, mode=0o755)
                except PermissionError:
                    raise PathSecurityError(
                        f"No permission to create storage directory: {self.storage_dir}"
                    )
                except OSError as e:
                    raise PathSecurityError(
                        f"Cannot create storage directory: {e}"
                    )

            # Sanitize project name
            safe_project = self._sanitize_name(project)
            if not safe_project:
                raise PathSecurityError(
                    f"Invalid project name: {project}"
                )

            # Sanitize filename
            safe_filename = self._sanitize_name(filename)
            if not safe_filename:
                raise PathSecurityError(
                    f"Invalid filename: {filename}"
                )

            # Construct path
            project_dir = self.storage_dir / safe_project
            file_path = project_dir / safe_filename

            # Resolve to absolute path
            resolved_path = file_path.resolve()

            # Security check: Ensure path is within storage directory
            if not str(resolved_path).startswith(str(self.storage_dir)):
                raise PathSecurityError(
                    f"Path traversal detected: {file_path}"
                )

            # Create project directory if needed
            if not project_dir.exists():
                try:
                    project_dir.mkdir(parents=True, mode=0o755)
                except PermissionError:
                    raise PathSecurityError(
                        f"No permission to create project directory: {project_dir}"
                    )

            # Check write permissions
            if not os.access(project_dir, os.W_OK):
                raise PermissionError(
                    f"No write permission for directory: {project_dir}"
                )

            return resolved_path

        except PathSecurityError:
            raise  # Re-raise security errors
        except PermissionError:
            raise  # Re-raise permission errors
        except Exception as e:
            raise OSError(f"Path resolution failed: {e}")

    def _sanitize_name(self, name: str) -> str:
        """Sanitize filename/project name"""
        # Remove dangerous characters
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
        sanitized = ''.join(c for c in name if c in safe_chars)

        # Check for reserved names (Windows)
        reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'LPT1'}
        if sanitized.upper() in reserved:
            return ""

        return sanitized
```

#### Pattern 4: Async Job Error Handling

```python
# src/mcp_fred/utils/job_manager.py

from enum import Enum
from datetime import datetime
from typing import Dict, Any

class JobStatus(Enum):
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobManager:
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get job status with error handling

        Returns:
            Job status dict or error response
        """
        try:
            # Check if job exists
            if job_id not in self.jobs:
                return {
                    "error": {
                        "code": "JOB_NOT_FOUND",
                        "message": f"Job not found: {job_id}",
                        "details": {
                            "job_id": job_id,
                            "suggestion": "Job may have expired (24 hour retention)"
                        }
                    }
                }

            job = self.jobs[job_id]

            # Return status based on job state
            if job['status'] == JobStatus.FAILED:
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "error": {
                        "code": job['error_code'],
                        "message": job['error_message'],
                        "retry_count": job.get('retry_count', 0),
                        "next_retry_in_seconds": job.get('next_retry', None)
                    },
                    "duration_seconds": job.get('duration_seconds', 0)
                }

            elif job['status'] == JobStatus.COMPLETED:
                return {
                    "job_id": job_id,
                    "status": "completed",
                    "duration_seconds": job['duration_seconds'],
                    "result": job['result']
                }

            elif job['status'] == JobStatus.PROCESSING:
                return {
                    "job_id": job_id,
                    "status": "processing",
                    "progress": job['progress']
                }

            else:  # ACCEPTED
                return {
                    "job_id": job_id,
                    "status": "accepted",
                    "message": "Job queued for processing"
                }

        except Exception as e:
            return {
                "error": {
                    "code": "JOB_STATUS_ERROR",
                    "message": "Failed to retrieve job status",
                    "details": {"error": str(e)}
                }
            }
```

### Error Code Reference

| Code | HTTP Status | Meaning | User Action |
|------|-------------|---------|-------------|
| `INVALID_API_KEY` | 401 | FRED API key is invalid | Check FRED_API_KEY environment variable |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests (120/min) | Wait 60 seconds, or use async jobs |
| `NOT_FOUND` | 404 | Series/resource not found | Verify series ID exists in FRED |
| `INVALID_REQUEST` | 400 | Bad request parameters | Check parameter format and values |
| `SERVER_ERROR` | 500 | FRED API server error | Retry later, issue with FRED |
| `TIMEOUT` | 408 | Request timed out | Check network, retry |
| `NETWORK_ERROR` | 503 | Cannot connect to FRED | Check internet connection |
| `VALIDATION_ERROR` | 422 | Parameter validation failed | Fix parameter types/values |
| `INVALID_OPERATION` | 400 | Unknown operation | Use valid operation name |
| `MISSING_PARAMETER` | 400 | Required parameter missing | Provide required parameter |
| `PATH_SECURITY_ERROR` | 403 | Path validation failed | Check project/filename format |
| `PERMISSION_ERROR` | 403 | No write permission | Check FRED_STORAGE_DIR permissions |
| `JOB_NOT_FOUND` | 404 | Job ID not found | Job expired (24hr retention) |
| `INTERNAL_ERROR` | 500 | Unexpected server error | Report bug with details |

### Logging Error Details

All errors should be logged for debugging:

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await fred_api_call()
except FREDAPIError as e:
    logger.error(
        f"FRED API error: {e.code}",
        extra={
            "error_code": e.code,
            "error_message": e.message,
            "details": e.details
        }
    )
    raise
```

---

## Testing Strategy

### Unit Tests
- Test individual functions and methods
- Mock external API calls
- Verify parameter validation

### Integration Tests
- Test API client with real FRED API (requires API key)
- Test end-to-end tool execution
- Verify error handling

### Test Coverage Goals
- Minimum 80% code coverage
- 100% coverage for critical paths (authentication, error handling)

---

## Development Workflow

1. **Feature Development:** Work on `dev` branch
2. **Code Quality:** Run Ruff before commits
3. **Testing:** Run pytest before merging
4. **Documentation:** Update docs with code changes
5. **Changelog:** Update CHANGELOG.md with semantic versioning

---

## Security Considerations

1. **API Key Protection:**
   - Never commit API keys to version control
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Input Validation:**
   - Validate all user inputs
   - Sanitize parameters before API calls
   - Use Pydantic for type validation

3. **Rate Limiting:**
   - Implement client-side rate limiting
   - Handle 429 responses gracefully
   - Consider caching frequently accessed data

---

## Future Enhancements

### Potential Features
- **Caching Layer:** Cache API responses to reduce API calls
- **Batch Operations:** Support multiple operations in single tool call
- **Data Visualization:** Generate charts/graphs from series data
- **Offline Mode:** Cache data for offline access
- **Retry Logic:** Automatic retry with exponential backoff

### Scalability Considerations
- Connection pooling for HTTP client
- Async/await for concurrent requests
- Response streaming for large datasets

---

## References

- **MCP Specification:** https://modelcontextprotocol.io/
- **FRED API Documentation:** https://fred.stlouisfed.org/docs/api/fred/
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Ruff Documentation:** https://docs.astral.sh/ruff/
