# MCP-FRED Context Guide

**Quick Start for New AI Contexts**

This document provides essential context for AI agents starting fresh on this project. Read this first before diving into other documentation.

---

## Project Overview

**MCP-FRED** is a Model Context Protocol (MCP) server that provides AI agents with access to the Federal Reserve Economic Data (FRED) API. It handles large economic datasets intelligently by managing token limits, async job processing, and organized file storage.

**Key Challenge:** FRED API can return datasets with 100,000+ observations that exceed AI model token limits. We solve this with smart output handling, background processing, and user-organized project storage.

**Technology Stack:** Python 3.11+, FastAPI, MCP SDK, tiktoken, pytest, Ruff

---

## Current Status

**Phase:** 0.4 Complete (Planning & Architecture)
**Branch:** `dev`
**Next Phase:** Phase 1 - Project Setup & Infrastructure

**Completion Status:**
- ✅ Phase 0.0: Git setup, initial planning
- ✅ Phase 0.1: Large data handling strategy
- ✅ Phase 0.2: User-configurable storage + JSON to CSV conversion
- ✅ Phase 0.3: Async job management system
- ✅ Phase 0.4: Conservative token limits + project management tools
- ⏳ Phase 1: Project setup (NEXT)

**Total Tools Designed:** 12 tools
- 6 FRED data tools (category, release, series, source, tag, maps)
- 3 Job management tools (status, list, cancel)
- 3 Project management tools (list, create, files)

---

## Key Architectural Decisions

### 1. **Conservative Token Estimation (Phase 0.4)**
- Assume 75% of AI context already consumed by chat history and other MCP servers
- Safe limits: Claude Sonnet (50K), GPT-4 (25K), Gemini Pro (250K)
- Philosophy: "Err on the side of saving to file more often"

### 2. **User-Configurable Storage (Phase 0.2)**
- `FRED_STORAGE_DIR` - User specifies storage location (default: `./fred-data`)
- NOT the MCP server directory (security concern)
- Project-based organization: `{FRED_STORAGE_DIR}/{project-name}/{type}/`

### 3. **Async Job Processing (Phase 0.3)**
- Datasets >10K rows or >10 seconds processing time → background job
- Return job_id immediately, AI checks status with `fred_job_status`
- Job lifecycle: accepted → processing → completed/failed

### 4. **JSON to CSV Conversion (Phase 0.2)**
- FRED API returns JSON/XML, we convert to CSV for standardization
- Matches Snowflake MCP server output format
- Excel-compatible, no AI-side conversion needed

### 5. **Project Management (Phase 0.4)**
- Users organize data by analysis project
- Tools to list, create, and browse projects
- AI proactively asks users about project selection

### 6. **Transport Protocols**
- STDIO (local): For Claude Desktop and local MCP clients
- Streamable HTTP (remote): Modern MCP standard (not SSE legacy)

---

## Documentation Map

**Start Here:**
- `CONTEXT.md` (this file) - Quick overview
- `API_MAPPING.md` - FRED API endpoints → Tools → Files mapping

**Architecture & Planning:**
- `ARCHITECTURE.md` - Complete system design (read sections as needed)
- `TODO.md` - Development tasks with architecture references
- `PROGRESS.md` - Completed work and decisions
- `FRED_API_REFERENCE.md` - FRED API documentation

**Development:**
- `DEVELOPMENT_GUIDE.md` - Implementation roadmap (coming soon)
- `TESTING_STRATEGY.md` - Testing philosophy and patterns (coming soon)

**Project Management:**
- `CHANGELOG.md` - Version history with semantic versioning
- `README.md` - User-facing documentation (placeholder)

---

## What to Read Based on Your Task

### If implementing a **FRED data tool** (category, release, series, etc.):
1. Read `API_MAPPING.md` - Find your endpoint mappings
2. Read `ARCHITECTURE.md` → "MCP Tool Design" section
3. Read `ARCHITECTURE.md` → "Large Data Handling Strategy" section
4. Read `FRED_API_REFERENCE.md` - Understand FRED API parameters
5. Read `TODO.md` → Phase 4 → Your specific tool tasks

### If implementing **utilities** (token estimation, file writer, job manager):
1. Read `ARCHITECTURE.md` → "Large Data Handling Strategy" section
2. Read `ARCHITECTURE.md` → "Async Job Management" section (for job utilities)
3. Read `TODO.md` → Phase 3 → Your specific utility tasks

### If implementing **project management tools**:
1. Read `ARCHITECTURE.md` → "Project Management Tools" section
2. Read `TODO.md` → Phase 4 → Project Management Tools

### If implementing **API client**:
1. Read `FRED_API_REFERENCE.md` - Complete API documentation
2. Read `API_MAPPING.md` - All endpoints mapped
3. Read `ARCHITECTURE.md` → "API Client Architecture" section
4. Read `TODO.md` → Phase 2 → Endpoint implementations

### If writing **tests**:
1. Read `ARCHITECTURE.md` → "Testing Strategy" section
2. Read `TESTING_STRATEGY.md` (when created)
3. Read `TODO.md` → Phase 5 → Testing tasks

### If setting up **transport layer**:
1. Read `ARCHITECTURE.md` → "Transport Layer" section
2. Read `TODO.md` → Phase 4 → Transport Layer Implementation

---

## Quick Reference: File Locations

**When Phase 1+ is implemented, code will be located at:**

```
src/mcp_fred/
├── server.py              # Main MCP server entry point
├── config.py              # Configuration management
├── api/
│   ├── client.py          # FRED API HTTP client
│   ├── endpoints/         # FRED API endpoint implementations
│   │   ├── category.py    # Category endpoints
│   │   ├── release.py     # Release endpoints
│   │   ├── series.py      # Series endpoints (CRITICAL: large data)
│   │   ├── source.py      # Source endpoints
│   │   ├── tag.py         # Tag endpoints
│   │   └── maps.py        # Maps/GeoFRED endpoints (CRITICAL: large data)
│   └── models/
│       └── responses.py   # Pydantic response models
├── utils/
│   ├── output_handler.py  # Smart output handling (file vs screen)
│   ├── token_estimator.py # Token counting with tiktoken
│   ├── file_writer.py     # CSV/JSON streaming
│   ├── json_to_csv.py     # JSON to CSV converter
│   ├── path_resolver.py   # Secure path resolution
│   ├── job_manager.py     # Async job management
│   └── background_worker.py # Background job processing
├── tools/
│   ├── category.py        # MCP tool: fred_category
│   ├── release.py         # MCP tool: fred_release
│   ├── series.py          # MCP tool: fred_series
│   ├── source.py          # MCP tool: fred_source
│   ├── tag.py             # MCP tool: fred_tag
│   ├── maps.py            # MCP tool: fred_maps
│   ├── job_status.py      # MCP tool: fred_job_status
│   ├── job_list.py        # MCP tool: fred_job_list (optional)
│   ├── job_cancel.py      # MCP tool: fred_job_cancel (optional)
│   ├── project_list.py    # MCP tool: fred_project_list
│   ├── project_create.py  # MCP tool: fred_project_create
│   └── project_files.py   # MCP tool: fred_project_files
└── transports/
    ├── stdio.py           # STDIO transport
    └── http.py            # Streamable HTTP transport
```

---

## Critical Context for Development

### FRED API Constraints
- **Rate limit:** 120 requests per minute
- **Max observations:** 100,000 per request
- **Pagination:** Use `offset` parameter for larger datasets
- **Authentication:** API key required for all requests

### Token Limits (Conservative)
- **Claude Sonnet:** 50K safe threshold (200K total, assume 75% used)
- **GPT-4:** 25K safe threshold (100K total, assume 75% used)
- **Gemini Pro:** 250K safe threshold (1M total, assume 75% used)

### When to Use Async Jobs
- Series observations > 10,000 rows
- Maps data with shape files
- Estimated processing time > 10 seconds
- Multiple paginated requests required

### Security Requirements
- NEVER write to MCP server installation directory
- Require `FRED_STORAGE_DIR` to be configured
- Validate all paths to prevent directory traversal
- Sanitize filenames and project names

### Configuration (Claude Desktop Example)
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

---

## Common Patterns to Follow

### Tool Implementation Pattern
All MCP tools follow this pattern:
1. Accept `operation` parameter for routing
2. Accept optional output parameters: `output`, `format`, `project`, `filename`
3. Validate parameters with Pydantic
4. Estimate data size before fetching
5. Decide: inline return vs file output vs async job
6. Return structured response

### Error Handling Pattern
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

### File Output Response Pattern
```json
{
  "status": "success",
  "output_mode": "file",
  "file_path": "/path/to/file.csv",
  "rows_written": 45000,
  "file_size_mb": 2.3,
  "message": "Data saved. Processing complete."
}
```

### Async Job Response Pattern
```json
{
  "status": "accepted",
  "job_id": "fred-job-uuid-timestamp",
  "message": "Processing in background...",
  "estimated_rows": 75000,
  "check_status": "Use fred_job_status tool with this job_id"
}
```

---

## Development Workflow

1. **Always work on `dev` branch**
2. **Use conventional commits:** `feat(scope): description`, `fix(scope): description`, etc.
3. **Run tests before committing:** `pytest`
4. **Run Ruff before committing:** `ruff check .`
5. **Update documentation** with code changes
6. **Update CHANGELOG.md** after completing phases
7. **Update PROGRESS.md** when tasks are completed

---

## Important User Feedback Quotes

> "I think that should be a default... We should have an optional configurable directory where the user can specify a specific directory on their local file system"
— Led to `FRED_STORAGE_DIR` instead of `MCP_CLIENT_ROOT`

> "In the Snowflake MCP server, if the download is going to be large... it does automatically respond with a unique job ID, like a UUID. There's a status method..."
— Led to async job management system design

> "We may run into an instance where the user is running late, and their chat thread already has several MCP servers. A lot of that context window may actually be eaten up."
— Led to conservative token limits (25% instead of 70%)

> "I think that should probably come from Fred-Data.functions, so that we can scan that directory, know what projects exist"
— Led to project management tools design

> "Let's just focus on grabbing the data and returning it back to AI so that AI can do the analysis. We won't try and do any analysis through the MCP server."
— Simplified approach: no server-side analysis

---

## Next Steps

**Current Phase:** Phase 1 - Project Setup & Infrastructure

**First Tasks:**
1. Create project directory structure
2. Initialize Python package (`src/mcp_fred/`)
3. Create `pyproject.toml` for Ruff configuration
4. Create `requirements.txt` with dependencies
5. Create `.env.example` file
6. Update `.gitignore` for Python projects
7. Create `pytest.ini` configuration
8. Set up basic README.md

**See:** `TODO.md` → Phase 1 for complete task list

---

## Questions to Ask if Context is Unclear

1. **What phase am I implementing?** → Check `PROGRESS.md` for last completed phase
2. **What are the dependencies?** → Check `TODO.md` task notes and `API_MAPPING.md`
3. **What's the architecture pattern?** → Check `ARCHITECTURE.md` relevant section
4. **What FRED endpoints do I need?** → Check `API_MAPPING.md` and `FRED_API_REFERENCE.md`
5. **What are the test requirements?** → Check `ARCHITECTURE.md` → Testing Strategy
6. **What configuration is needed?** → Check `ARCHITECTURE.md` → Configuration Management

---

## Repository Information

- **Repository:** https://github.com/cfdude/mcp-fred
- **Branches:** `main` (production), `dev` (development)
- **Commit Signing:** SSH key-based signed commits enabled
- **License:** Not yet specified

---

**Last Updated:** 2025-10-08
**Document Version:** 1.0 (Phase 0.4 Complete)
