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
│   │   │   └── path_resolver.py     # Secure path resolution and validation
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── category.py      # MCP tool: fred_category
│   │       ├── release.py       # MCP tool: fred_release
│   │       ├── series.py        # MCP tool: fred_series
│   │       ├── source.py        # MCP tool: fred_source
│   │       ├── tag.py           # MCP tool: fred_tag
│   │       └── maps.py          # MCP tool: fred_maps
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

**Model Token Limits:**
- Claude Sonnet: ~200K tokens (safe threshold: 140K)
- GPT-4: ~100K tokens (safe threshold: 70K)
- Gemini Pro: ~1M tokens (safe threshold: 700K)

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

#### 5. **Immediate Response to AI Agent**

For large requests, return immediate acknowledgment:

```json
{
  "status": "processing",
  "request_id": "uuid-here",
  "message": "Large dataset detected. Fetching and saving to file...",
  "estimated_rows": 50000,
  "output_mode": "file",
  "project": "economic-analysis",
  "file_path": "{MCP_CLIENT_ROOT}/fred-data/economic-analysis/series/GNPCA_observations_{timestamp}.csv"
}
```

Then process in background and update when complete.

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

| Tool Name | Operations | Endpoints Covered |
|-----------|-----------|-------------------|
| `fred_category` | `get`, `list_children`, `get_related`, `get_series`, `get_tags`, `get_related_tags` | `/category/*` |
| `fred_release` | `list`, `get`, `get_dates`, `get_series`, `get_sources`, `get_tags`, `get_related_tags`, `get_tables` | `/releases/*`, `/release/*` |
| `fred_series` | `get`, `search`, `get_categories`, `get_observations`, `get_release`, `get_tags`, `search_tags`, `search_related_tags`, `get_updates`, `get_vintage_dates` | `/series/*` |
| `fred_source` | `list`, `get`, `get_releases` | `/sources/*`, `/source/*` |
| `fred_tag` | `list`, `get_related_tags`, `get_series` | `/tags/*`, `/related_tags` |
| `fred_maps` | `get_shapes`, `get_series_group`, `get_regional_data`, `get_series_data` | `/geofred/*` |

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

### Error Response Format

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
