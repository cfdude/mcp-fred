# MCP-FRED

Model Context Protocol server for Federal Reserve Economic Data (FRED) API

A comprehensive MCP server providing access to all FRED API endpoints with intelligent large data handling, project-based storage, and async job processing for AI assistants like Claude.

[![PyPI version](https://img.shields.io/pypi/v/mcp-fred.svg)](https://pypi.org/project/mcp-fred/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP 3.0.0b1](https://img.shields.io/badge/FastMCP-3.0.0b1-purple.svg)](https://gofastmcp.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Features

- **Built on FastMCP 3.0.0b1** - Modern decorator-based MCP framework with context injection
- **39 MCP Tools** covering 50+ FRED API endpoints (categories, releases, series, sources, tags, maps)
- **Progressive Disclosure** - 29 core tools visible by default, 16 additional tools activated on-demand
- **Per-Session Activation** - Enable data, advanced, or admin tool tiers as needed
- **Conservative Token Estimation** - Automatically saves large datasets to files to prevent context overflow
- **Project-Based Storage** - Organized file management for economic data
- **Async Job Processing** - Background processing for large datasets (>10K observations)
- **Smart Output Handling** - Auto-detect when to return data vs. save to file
- **Type Safety** - Full Pydantic validation for all inputs and outputs

---

## Quick Start

### Three Installation Options

#### Option 1: PyPI Installation (Easiest)

Install directly from PyPI using pip or uv:

```bash
# Using pip
pip install mcp-fred

# Or using uv (faster)
uv pip install mcp-fred
```

Usage with Claude Desktop:

Add to your Claude Desktop configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fred": {
      "command": "uv",
      "args": ["--directory", "/path/to/your/virtualenv", "run", "mcp-fred"],
      "env": {
        "FRED_API_KEY": "your_api_key_here",
        "FRED_STORAGE_DIR": "/Users/username/Documents/fred-data"
      }
    }
  }
}
```

Restart Claude Desktop, and the FRED tools will be available!

---

#### Option 2: Claude Desktop Extension

The no-setup option - includes bundled Python environment!

Requirements:
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager (`brew install uv`)

Installation:
1. Download `mcp-fred.mcpb` from [GitHub Releases](https://github.com/cfdude/mcp-fred/releases)
2. Double-click the file (or run `open mcp-fred.mcpb`)
3. Enter your FRED API key when prompted
4. Done! The extension is now available in Claude Desktop

See [EXTENSION.md](EXTENSION.md) for detailed instructions and troubleshooting.

---

#### Option 3: Manual Installation from Source

Prerequisites:
- Python 3.11 or higher
- FRED API key (free from [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html))

Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/cfdude/mcp-fred.git
   cd mcp-fred
   ```

2. Create virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your FRED_API_KEY
   ```

Usage with Claude Desktop:

Add to your Claude Desktop configuration file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

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

Restart Claude Desktop, and the FRED tools will be available!

CLI Usage Example:

Use the MCP CLI (or compatible host) to manage FRED data projects and background jobs:

```bash
# Create a new project workspace with canonical subdirectories
mcp-cli call fred_project_create --operation create --project macro-demo

# List known projects with file counts and storage metadata
mcp-cli call fred_project_list --operation list --output screen

# Review background job progress or filter for completed runs
mcp-cli call fred_job_list --operation list --status completed --output screen

# Cancel a long-running job when you no longer need the export
mcp-cli call fred_job_cancel --operation cancel --job_id fred-job-123

# Check the final status for a specific job (useful after cancellations)
mcp-cli call fred_job_status --operation get --job_id fred-job-123
```

> Note: The CLI examples assume `mcp-cli` is configured with your `FRED_API_KEY` and optional `FRED_STORAGE_DIR`. Substitute actual job identifiers when invoking job status tools.

---

## Available Tools

MCP-FRED uses **progressive disclosure** to reduce context overhead. Core and discovery tools are always visible; additional tiers can be activated per-session.

### Tool Tiers

| Tier | Tools | Status | Activation |
|------|-------|--------|------------|
| **Core** | 8 tools | Always visible | - |
| **Discovery** | 15 tools | Always visible | - |
| **Data** | 7 tools | Hidden by default | `activate_data_tools()` |
| **Advanced** | 6 tools | Hidden by default | `activate_advanced_tools()` |
| **Admin** | 4 tools | Hidden by default | `activate_admin_tools()` |

Use `activate_all_tools()` to enable all tiers at once, or `list_tool_tiers()` to see available tools.

### Core Tools (Always Available)

| Tool | Description |
|------|-------------|
| `fred_category_get` | Get category details |
| `fred_category_children` | List child categories |
| `fred_series_get` | Get series metadata |
| `fred_release_get` | Get release details |
| `fred_source_get` | Get source details |

### Discovery Tools (Always Available)

| Tool | Description |
|------|-------------|
| `fred_series_search` | Search for series by keywords |
| `fred_tag_list` | List FRED tags |
| `fred_tag_series` | Get series by tags |
| `fred_release_list` | List all releases |
| `fred_source_list` | List all sources |
| `fred_category_series` | List series in category |

### Data Tools (Activate with `activate_data_tools()`)

| Tool | Description |
|------|-------------|
| `fred_series_observations` | Get time series data points |
| `fred_release_dates` | Get release date schedules |
| `fred_maps_shapes` | Get geographic shape data |
| `fred_maps_regional_data` | Get regional economic data |

### Admin Tools (Activate with `activate_admin_tools()`)

| Tool | Description |
|------|-------------|
| `fred_job_status` | Check status of background jobs |
| `fred_job_list` | List recent/active jobs |
| `fred_job_cancel` | Cancel running job |
| `fred_project_list` | List all projects in storage |
| `fred_project_create` | Create new project directory |

---

## How It Works

### Smart Output Handling

MCP-FRED intelligently decides whether to return data directly or save to a file:

1. Small datasets (<50K tokens): Returned directly to Claude
2. Large datasets (>50K tokens): Saved to file automatically
3. Very large datasets (>10K observations): Processed in background job

### Token Estimation

Conservative approach assuming 75% of context already used:

- Claude Sonnet: 50K safe limit (out of 200K total)
- GPT-4: 25K safe limit (out of 100K total)
- Gemini Pro: 250K safe limit (out of 1M total)

### Project-Based Storage

Files are organized by project:

```
fred-data/
  my-project/
    series/          # Series observation data
    maps/            # GeoFRED shape files
    releases/        # Release data
    categories/      # Category data
    sources/         # Source data
    tags/            # Tag data
    .project.json    # Project metadata
```

---

## Example Usage

In Claude Desktop, ask:

> "Using FRED data, get GDP observations for the last 10 years and save it to the 'economy-2024' project"

Claude will:
1. Call `fred_series` with operation="get_observations"
2. Estimate dataset size (~40 observations)
3. Save to `fred-data/economy-2024/series/GNPCA_observations.csv`
4. Return file path for further analysis

For large datasets:

> "Get all unemployment observations since 1948"

Claude will:
1. Estimate size (>10K observations)
2. Create background job
3. Return job ID immediately
4. Check status with `fred_job_status`
5. Get file path when complete

---

## Configuration

All configuration via environment variables (`.env` file or MCP client config):

### Required

- `FRED_API_KEY` - Your FRED API key

### Optional

- `FRED_STORAGE_DIR` - Storage location (default: `./fred-data`)
- `FRED_PROJECT_NAME` - Default project name (default: `default`)
- `FRED_OUTPUT_FORMAT` - Default format: `csv` or `json` (default: `csv`)
- `FRED_OUTPUT_MODE` - Output mode: `auto`, `screen`, or `file` (default: `auto`)
- `FRED_OUTPUT_FILE_CHUNK_SIZE` - Rows per CSV flush (default: `1000`)
- `FRED_JOB_RETENTION_HOURS` - Job retention period (default: `24`)

See `.env.example` for complete list.

---

## Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/cfdude/mcp-fred.git
cd mcp-fred
git checkout dev

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your FRED_API_KEY
```

### Run Tests

```bash
# Run all tests with coverage
pytest --cov=mcp_fred --cov-report=html

# Run specific tests
pytest tests/test_tools/test_series.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint and format
ruff check .
ruff format .

# Fix auto-fixable issues
ruff check --fix .
```

### Documentation

- [CONTEXT.md](docs/CONTEXT.md) - Quick start for new AI contexts
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design
- [API_MAPPING.md](docs/API_MAPPING.md) - Complete FRED API to Tool mapping
- [SERIES_MAPS_GUIDE.md](docs/SERIES_MAPS_GUIDE.md) - Series & maps tool usage
- [DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md) - Developer setup guide
- [DEPENDENCIES.md](docs/DEPENDENCIES.md) - Why each dependency was chosen
- [TODO.md](docs/TODO.md) - Development task list (8 phases)
- [CI_CD.md](docs/CI_CD.md) - CI/CD workflows and pre-commit hooks

### CI/CD

Automated testing and security checks run on every commit and pull request.

**Install pre-commit hook** (recommended for development):
```bash
./scripts/install-pre-commit-hook.sh
```

The hook runs before each commit:
- Code formatting check (ruff)
- Linting (ruff)
- Full test suite (pytest)
- Coverage validation (80% minimum)

**GitHub Actions workflows:**
- CI: Tests, formatting, linting on Python 3.11 & 3.12
- Security: Secret scanning, dependency vulnerabilities

See [CI_CD.md](docs/CI_CD.md) for complete details.

---

## Architecture

### Built on FastMCP 3.0.0b1

MCP-FRED is built on [FastMCP 3.0.0b1](https://gofastmcp.com), the modern Python framework for building MCP servers. Key framework features used:

- **Decorator-based tool registration** - `@mcp.tool()` decorators for clean tool definitions
- **Context injection** - `CurrentContext()` dependency provides access to shared resources
- **Lifespan management** - `@lifespan` decorator handles initialization and cleanup
- **Tag-based visibility** - `mcp.disable(tags={...})` and `ctx.enable_components()` for progressive disclosure
- **Tool annotations** - `readOnlyHint`, `idempotentHint` for LLM optimization

### Core Components

```
mcp-fred/
  src/mcp_fred/
    fastmcp_server.py   # FastMCP entry point with progressive disclosure
    config.py           # Configuration management
    servers/            # FastMCP tool modules (39 tools)
      base.py           # Server instance and lifespan context
      admin.py          # Job/project management + activation tools
      categories.py     # Category tools
      releases.py       # Release tools
      series.py         # Series tools (largest module)
      sources.py        # Source tools
      tags.py           # Tag tools
      maps.py           # GeoFRED tools
      common.py         # Shared utilities (smart_output, error formatting)
    api/                # FRED API client
      client.py         # Async HTTP client with retry/backoff
      endpoints/        # API endpoint implementations
      models/           # Pydantic response models
    utils/              # Utilities
      token_estimator.py    # Token counting (tiktoken)
      output_handler.py     # Smart output routing
      json_to_csv.py        # JSON to CSV conversion
      job_manager.py        # Async job tracking
      background_worker.py  # Background task processing
    tools/              # Legacy tool implementations (for MCPFRED_LEGACY=1)
    transports/         # Legacy STDIO transport
  tests/                # Test suite (80% coverage target)
```

### Key Design Decisions

1. **FastMCP 3.0.0b1** - Modern framework with decorator-based tools and context injection
2. **Progressive Disclosure** - 29 tools visible by default, 16 activated on-demand to reduce LLM context overhead
3. **Conservative Token Limits** - Assume 75% context used, safe limits at 25% of total
4. **Project-Based Storage** - User-configurable directory, organized subdirectories
5. **Async Job Processing** - Background jobs for datasets >10K rows or >10 seconds
6. **Type Safety** - Pydantic for all validation, runtime error catching
7. **Legacy Support** - Set `MCPFRED_LEGACY=1` to use old STDIO transport

---

## FRED API Coverage

50+ FRED API endpoints mapped to 12 MCP tools

### Critical Operations (Large Data)

- Series Observations: Up to 100K observations per series
- GeoFRED Maps: Shape files can be 1MB+ per region

### Rate Limits

- 120 requests per minute (FRED API limit)
- Automatic retry with exponential backoff

---

## Testing Philosophy

- Target: 80% code coverage minimum
- Focus: Unit tests (primary), integration tests (as needed)
- Mocking: Mock FRED API responses, no real API calls in tests
- No E2E: MCP product doesn't require end-to-end testing
- Reference: See [docs/TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md) for scenarios, fixtures, and tooling details.

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow conventional commit format (`feat:`, `fix:`, `docs:`, etc.)
4. Run tests and linting (`pytest && ruff check .`)
5. Submit a pull request to `dev` branch

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- FRED API: Federal Reserve Bank of St. Louis for providing free economic data API
- Model Context Protocol: Anthropic for the MCP specification
- Snowflake MCP: Inspiration for smart output handling approach

---

## Support

- Issues: [GitHub Issues](https://github.com/cfdude/mcp-fred/issues)
- FRED API Docs: [fred.stlouisfed.org/docs/api](https://fred.stlouisfed.org/docs/api/fred/)
- MCP Specification: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
