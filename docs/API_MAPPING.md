# FRED API to MCP Tool Mapping

**Complete Reference: FRED API Endpoints → MCP Tools → Implementation Files**

This document provides a comprehensive mapping between FRED API endpoints and MCP tools built on **FastMCP 3.0.0b1**.

> **Note:** As of the FastMCP 3.0.0b1 migration, each FRED API endpoint maps to an individual MCP tool (not operation-based dispatch). Tools are organized by tier for progressive disclosure.

---

## Quick Navigation

- [Category Endpoints](#category-endpoints) → `fred_category_*` tools
- [Release Endpoints](#release-endpoints) → `fred_release_*` tools
- [Series Endpoints](#series-endpoints) → `fred_series_*` tools (CRITICAL: Large Data)
- [Source Endpoints](#source-endpoints) → `fred_source_*` tools
- [Tag Endpoints](#tag-endpoints) → `fred_tag_*` tools
- [Maps Endpoints](#maps-endpoints) → `fred_maps_*` tools (CRITICAL: Large Data)

---

## Category Endpoints

**MCP Tools:** `fred_category_*` (6 tools)
**Implementation File:** `src/mcp_fred/servers/categories.py`
**API Client File:** `src/mcp_fred/api/endpoints/category.py`

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Notes |
|-------------------|----------|------|-------------------|-------|
| `GET /fred/category` | `fred_category_get` | core | `fred_category_get(category_id=125)` | Get category metadata |
| `GET /fred/category/children` | `fred_category_children` | core | `fred_category_children(category_id=125)` | Get child categories |
| `GET /fred/category/related` | `fred_category_related` | discovery | `fred_category_related(category_id=125)` | Get related categories |
| `GET /fred/category/series` | `fred_category_series` | discovery | `fred_category_series(category_id=125, limit=100)` | List series in category |
| `GET /fred/category/tags` | `fred_category_tags` | advanced | `fred_category_tags(category_id=125)` | Get category tags |
| `GET /fred/category/related_tags` | `fred_category_related_tags` | advanced | `fred_category_related_tags(category_id=125, tag_names="gdp")` | Get related tags |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)

---

## Release Endpoints

**MCP Tools:** `fred_release_*` (9 tools)
**Implementation File:** `src/mcp_fred/servers/releases.py`
**API Client File:** `src/mcp_fred/api/endpoints/release.py`

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Notes |
|-------------------|----------|------|-------------------|-------|
| `GET /fred/releases` | `fred_release_list` | discovery | `fred_release_list(limit=100)` | Get all releases |
| `GET /fred/releases/dates` | `fred_release_dates` | data | `fred_release_dates(limit=100)` | All release dates |
| `GET /fred/release` | `fred_release_get` | core | `fred_release_get(release_id=53)` | Get release metadata |
| `GET /fred/release/dates` | `fred_release_get_dates` | data | `fred_release_get_dates(release_id=53)` | Release dates for specific release |
| `GET /fred/release/series` | `fred_release_series` | discovery | `fred_release_series(release_id=53)` | Series in release |
| `GET /fred/release/sources` | `fred_release_sources` | discovery | `fred_release_sources(release_id=53)` | Sources for release |
| `GET /fred/release/tags` | `fred_release_tags` | advanced | `fred_release_tags(release_id=53)` | Tags for release |
| `GET /fred/release/related_tags` | `fred_release_related_tags` | advanced | `fred_release_related_tags(release_id=53, tag_names="gdp")` | Related tags |
| `GET /fred/release/tables` | `fred_release_tables` | advanced | `fred_release_tables(release_id=53)` | Release tables |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)

---

## Series Endpoints

**⚠️ CRITICAL: Large Data Handling Required**

**MCP Tools:** `fred_series_*` (10 tools)
**Implementation File:** `src/mcp_fred/servers/series.py`
**API Client File:** `src/mcp_fred/api/endpoints/series.py`

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Large Data Risk | Notes |
|-------------------|----------|------|-------------------|-----------------|-------|
| `GET /fred/series` | `fred_series_get` | core | `fred_series_get(series_id="GNPCA")` | Low | Series metadata only |
| `GET /fred/series/search` | `fred_series_search` | discovery | `fred_series_search(search_text="gdp", limit=100)` | Medium | Can return many results |
| `GET /fred/series/categories` | `fred_series_categories` | discovery | `fred_series_categories(series_id="GNPCA")` | Low | Categories for series |
| `GET /fred/series/observations` | `fred_series_observations` | data | `fred_series_observations(series_id="GNPCA")` | **CRITICAL** | **Up to 100K observations** |
| `GET /fred/series/release` | `fred_series_release` | discovery | `fred_series_release(series_id="GNPCA")` | Low | Release for series |
| `GET /fred/series/tags` | `fred_series_tags` | discovery | `fred_series_tags(series_id="GNPCA")` | Low | Tags for series |
| `GET /fred/series/search/tags` | `fred_series_search_tags` | advanced | `fred_series_search_tags(series_search_text="gdp")` | Low | Search for tags |
| `GET /fred/series/search/related_tags` | `fred_series_search_related_tags` | advanced | `fred_series_search_related_tags(series_search_text="gdp")` | Low | Related tags search |
| `GET /fred/series/updates` | `fred_series_updates` | data | `fred_series_updates(limit=100)` | Medium | Recently updated series |
| `GET /fred/series/vintagedates` | `fred_series_vintage_dates` | data | `fred_series_vintage_dates(series_id="GNPCA")` | Low | Vintage dates |

### Critical Implementation Requirements

**For `get_observations` operation:**
1. **Token Estimation:** Estimate result size before fetching
2. **Async Jobs:** Use background processing if >10K rows
3. **File Output:** Auto-save to file if exceeds token limits
4. **Streaming:** Stream to CSV/JSON in chunks
5. **Progress:** Provide progress updates for large datasets

**Architecture References:**
- [ARCHITECTURE.md → Large Data Handling Strategy](ARCHITECTURE.md#large-data-handling-strategy)
- [ARCHITECTURE.md → Async Job Management](ARCHITECTURE.md#async-job-management-for-large-requests)
- [ARCHITECTURE.md → Token Estimation](ARCHITECTURE.md#token-estimation)

**TODO References:**
- [TODO.md → Phase 3 → Token Estimation](TODO.md#token-estimation-using-tiktoken)
- [TODO.md → Phase 3 → Async Job Management](TODO.md#async-job-management)
- [TODO.md → Phase 4 → Series Tool](TODO.md#series-tool)

### Usage Tips

- Use `output="auto"` for everyday lookups; large observations auto-save to project storage using chunked CSV writers.
- Provide `project` and optional `filename` to direct output (e.g., `fred_series(operation="get_observations", series_id="GDP", project="macro")`).
- Combine `search` + `search_tags` to discover candidate series before fetching heavy observations.
- `get_observations` automatically schedules a background job when row counts exceed the configured threshold; monitor `fred_job_status` for `rows_written`/`bytes_written`.
- CSV exports include flattened metadata columns so nested properties (e.g., `location_state`) appear as individual fields.
- When working with vintages, call `get_vintage_dates` first and loop through the returned dates for historical slices.

---

## Source Endpoints

**MCP Tools:** `fred_source_*` (3 tools)
**Implementation File:** `src/mcp_fred/servers/sources.py`
**API Client File:** `src/mcp_fred/api/endpoints/source.py`

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Notes |
|-------------------|----------|------|-------------------|-------|
| `GET /fred/sources` | `fred_source_list` | discovery | `fred_source_list(limit=100)` | Get all sources |
| `GET /fred/source` | `fred_source_get` | core | `fred_source_get(source_id=1)` | Get source metadata |
| `GET /fred/source/releases` | `fred_source_releases` | discovery | `fred_source_releases(source_id=1)` | Releases from source |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)

---

## Tag Endpoints

**MCP Tools:** `fred_tag_*` (3 tools)
**Implementation File:** `src/mcp_fred/servers/tags.py`
**API Client File:** `src/mcp_fred/api/endpoints/tag.py`

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Notes |
|-------------------|----------|------|-------------------|-------|
| `GET /fred/tags` | `fred_tag_list` | discovery | `fred_tag_list(limit=100)` | Get all tags |
| `GET /fred/tags/series` | `fred_tag_series` | discovery | `fred_tag_series(tag_names="gdp;quarterly")` | Series matching tags |
| `GET /fred/related_tags` | `fred_tag_related` | discovery | `fred_tag_related(tag_names="gdp")` | Related tags |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)

---

## Maps Endpoints

**⚠️ CRITICAL: Large Data Handling Required**

**MCP Tools:** `fred_maps_*` (4 tools)
**Implementation File:** `src/mcp_fred/servers/maps.py`
**API Client File:** `src/mcp_fred/api/endpoints/maps.py`

**Note:** Maps API uses different base path (`/geofred` instead of `/fred`)

| FRED API Endpoint | MCP Tool | Tier | Tool Call Example | Large Data Risk | Notes |
|-------------------|----------|------|-------------------|-----------------|-------|
| `GET /geofred/shapes/file` | `fred_maps_shapes` | data | `fred_maps_shapes(shape="state")` | **HIGH** | **Shape files with geo data** |
| `GET /geofred/series/group` | `fred_maps_series_group` | data | `fred_maps_series_group(series_id="SMU56000000500000001a")` | Medium | Series group metadata |
| `GET /geofred/regional/data` | `fred_maps_regional_data` | data | `fred_maps_regional_data(series_group="882")` | **HIGH** | **Regional economic data** |
| `GET /geofred/series/data` | `fred_maps_series_data` | data | `fred_maps_series_data(series_id="SMU56000000500000001a")` | **HIGH** | **Series data for maps** |

### Critical Implementation Requirements

**For all `fred_maps` operations:**
1. **Large Files:** Shape files can be several MB
2. **Token Estimation:** Always estimate before returning
3. **File Output Preferred:** Default to file output for shape files
4. **Async Jobs:** Use for regional data and series data
5. **Format Support:** JSON for shape files, CSV for regional data

**Architecture References:**
- [ARCHITECTURE.md → Large Data Handling Strategy](ARCHITECTURE.md#large-data-handling-strategy)
- [FRED_API_REFERENCE.md → Maps API](FRED_API_REFERENCE.md#6-maps-api)

**TODO Reference:** [TODO.md → Phase 4 → Maps Tool](TODO.md#maps-tool)

### Usage Tips

- `get_shapes` returns GeoJSON-like dictionaries; prefer `output="file"` (default) to persist shape files under `maps/`.
- Supply `series_id` to `get_series_data` for region-level statistics ready for choropleth rendering.
- Pair `get_series_group` with `fred_series(search=...)` to surface compatible map series for dashboards.
- Large map exports queue background jobs automatically; use `fred_job_status` to retrieve file paths once the worker completes.
- CSV outputs flatten nested fields such as `properties_state_abbr`, `metadata_units`, and keep geometry serialized as JSON strings. Fixtures live in `tests/fixtures/maps/` for reference.
- For quick inspection without saving, force `output="screen"`; responses remain limited by token estimator safeguards.

---

## Job Management Tools

**Not FRED API endpoints** - Internal MCP server functionality (Tier: admin)

| MCP Tool | Implementation File | Tier | Purpose |
|----------|---------------------|------|---------|
| `fred_job_status` | `src/mcp_fred/servers/admin.py` | admin | Check status of background jobs |
| `fred_job_list` | `src/mcp_fred/servers/admin.py` | admin | List recent jobs with filtering |
| `fred_job_cancel` | `src/mcp_fred/servers/admin.py` | admin | Cancel running background jobs |

- `fred_job_status` surfaces job metadata (progress, result, error, timestamps) for a single background operation.
- `fred_job_list` supports filtering by status, pagination (`limit`, `offset`), and sorts jobs by most recent update.
- `fred_job_cancel` marks a job as `cancelled` and records the optional user-supplied reason.

**Activation:** Call `activate_admin_tools()` to enable these tools.

---

## Project Management Tools

**Not FRED API endpoints** - Internal MCP server functionality (Tier: admin)

| MCP Tool | Implementation File | Tier | Purpose |
|----------|---------------------|------|---------|
| `fred_project_list` | `src/mcp_fred/servers/admin.py` | admin | List all projects in storage directory |
| `fred_project_create` | `src/mcp_fred/servers/admin.py` | admin | Create new project directory |

- `fred_project_list` returns aggregate metadata (`file_count`, `total_size_bytes`, `latest_modified`) for each project under `FRED_STORAGE_DIR`.
- `fred_project_create` scaffolds the canonical subdirectories (series, maps, releases, categories, sources, tags) and writes `.project.json` metadata.

**Activation:** Call `activate_admin_tools()` to enable these tools.

---

## Activation Tools

**Always visible** - Used to enable additional tool tiers for progressive disclosure

| MCP Tool | Implementation File | Purpose |
|----------|---------------------|---------|
| `activate_data_tools` | `src/mcp_fred/servers/admin.py` | Enable data retrieval tools (tier:data) |
| `activate_advanced_tools` | `src/mcp_fred/servers/admin.py` | Enable advanced query tools (tier:advanced) |
| `activate_admin_tools` | `src/mcp_fred/servers/admin.py` | Enable job/project management tools (tier:admin) |
| `activate_all_tools` | `src/mcp_fred/servers/admin.py` | Enable all tool tiers at once |
| `list_tool_tiers` | `src/mcp_fred/servers/admin.py` | Show available tool categories and how to activate them |

---

## Utility Components

**Supporting infrastructure for tools**

| Component | Implementation File | Purpose | Used By |
|-----------|---------------------|---------|---------|
| Smart Output | `src/mcp_fred/servers/common.py` | Intelligent output routing (screen vs file) | All FastMCP tools |
| Token Estimator | `src/mcp_fred/utils/token_estimator.py` | Estimate token count using tiktoken | smart_output |
| JSON to CSV Converter | `src/mcp_fred/utils/json_to_csv.py` | Convert FRED JSON to CSV | smart_output |
| File Writer | `src/mcp_fred/utils/file_writer.py` | Stream data to CSV/JSON files | smart_output |
| Path Resolver | `src/mcp_fred/utils/path_resolver.py` | Secure path resolution | File operations |
| Job Manager | `src/mcp_fred/utils/job_manager.py` | Async job tracking | Series, Maps tools |
| Background Worker | `src/mcp_fred/utils/background_worker.py` | Background job processing | Series, Maps tools |
| Output Handler | `src/mcp_fred/utils/output_handler.py` | Legacy output routing | Legacy tools only |

**Architecture Reference:** [ARCHITECTURE.md → Large Data Handling Strategy](ARCHITECTURE.md#large-data-handling-strategy)

---

## FRED API Parameters Reference

**Common parameters used across all endpoints**

| Parameter | Type | Used In | Description | Example |
|-----------|------|---------|-------------|---------|
| `api_key` | string | All | FRED API key (required) | Set via `FRED_API_KEY` env var |
| `file_type` | string | All | Response format: json, xml | `json` (default in our client) |
| `realtime_start` | date | Many | Start date for real-time period | `2023-01-01` |
| `realtime_end` | date | Many | End date for real-time period | `2023-12-31` |
| `limit` | integer | Many | Maximum results to return | `1000` |
| `offset` | integer | Many | Pagination offset | `0` |
| `order_by` | string | Many | Sort field | `series_id`, `observation_date` |
| `sort_order` | string | Many | Sort direction: asc, desc | `asc` |
| `series_id` | string | Series | FRED series ID | `GNPCA` |
| `observation_start` | date | Series | Start date for observations | `2000-01-01` |
| `observation_end` | date | Series | End date for observations | `2023-12-31` |
| `units` | string | Series | Data transformation | `lin`, `chg`, `pch`, `pc1`, `log` |
| `frequency` | string | Series | Data frequency | `d`, `w`, `m`, `q`, `a` |
| `aggregation_method` | string | Series | Aggregation method | `avg`, `sum`, `eop` |

**Full Parameter Reference:** [FRED_API_REFERENCE.md → Common Parameters](FRED_API_REFERENCE.md#common-parameters)

---

## Response Format Patterns

### Standard API Response

```json
{
  "realtime_start": "2023-01-01",
  "realtime_end": "2023-12-31",
  "observation_start": "2000-01-01",
  "observation_end": "2023-12-31",
  "units": "lin",
  "output_type": 1,
  "file_type": "json",
  "order_by": "observation_date",
  "sort_order": "asc",
  "count": 285,
  "offset": 0,
  "limit": 1000,
  "observations": [...]
}
```

### MCP Tool Response (Inline)

```json
{
  "status": "success",
  "output_mode": "screen",
  "data": {...}
}
```

### MCP Tool Response (File Output)

```json
{
  "status": "success",
  "output_mode": "file",
  "file_path": "/Users/username/Documents/fred-data/project-name/series/GNPCA_observations_20251008_143022.csv",
  "rows_written": 45000,
  "file_size_mb": 2.3,
  "estimated_tokens": 85000,
  "message": "Data saved. Processing complete."
}
```

### MCP Tool Response (Async Job)

```json
{
  "status": "accepted",
  "job_id": "fred-job-a3f2b8c4-20251008-143022",
  "message": "Processing in background...",
  "estimated_rows": 75000,
  "estimated_time_seconds": 45,
  "check_status": "Use fred_job_status tool with this job_id"
}
```

---

## Implementation Checklist

When implementing a tool, ensure:

- [ ] API client method implemented in `api/endpoints/*.py`
- [ ] Pydantic response models defined in `api/models/responses.py`
- [ ] MCP tool implemented in `tools/*.py`
- [ ] Operation routing logic added
- [ ] Parameter validation with Pydantic
- [ ] Output handling (output, format, project, filename params)
- [ ] Token estimation for large data operations
- [ ] Async job support for operations that can return >10K rows
- [ ] Error handling for API errors
- [ ] Unit tests in `tests/test_tools/`
- [ ] Integration tests in `tests/test_integration/`
- [ ] Tool documentation in docstrings

---

## Quick Command Reference

```bash
# Run tests for specific tool
pytest tests/test_tools/test_series.py

# Run tests for API endpoint
pytest tests/test_api/test_endpoints/test_series.py

# Test with real FRED API (requires FRED_API_KEY)
FRED_API_KEY=your_key pytest tests/test_integration/

# Lint specific file
ruff check src/mcp_fred/tools/series.py

# Format specific file
ruff format src/mcp_fred/tools/series.py
```

---

**Last Updated:** 2026-01-21
**Document Version:** 2.0 (FastMCP 3.0.0b1 Migration)
