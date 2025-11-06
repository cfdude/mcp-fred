# FRED API to MCP Tool Mapping

**Complete Reference: FRED API Endpoints → MCP Tools → Implementation Files**

This document provides a comprehensive mapping between FRED API endpoints, MCP tool operations, and where they will be implemented in the codebase.

---

## Quick Navigation

- [Category Endpoints](#category-endpoints) → `fred_category` tool
- [Release Endpoints](#release-endpoints) → `fred_release` tool
- [Series Endpoints](#series-endpoints) → `fred_series` tool (CRITICAL: Large Data)
- [Source Endpoints](#source-endpoints) → `fred_source` tool
- [Tag Endpoints](#tag-endpoints) → `fred_tag` tool
- [Maps Endpoints](#maps-endpoints) → `fred_maps` tool (CRITICAL: Large Data)

---

## Category Endpoints

**MCP Tool:** `fred_category`
**Implementation File:** `src/mcp_fred/tools/category.py`
**API Client File:** `src/mcp_fred/api/endpoints/category.py`

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/category` | `get` | `fred_category(operation="get", category_id=125)` | `get_category(category_id)` | Get category metadata |
| `GET /fred/category/children` | `list_children` | `fred_category(operation="list_children", category_id=125)` | `get_category_children(category_id)` | Get child categories |
| `GET /fred/category/related` | `get_related` | `fred_category(operation="get_related", category_id=125)` | `get_category_related(category_id)` | Get related categories |
| `GET /fred/category/series` | `get_series` | `fred_category(operation="get_series", category_id=125)` | `get_category_series(category_id)` | List series in category |
| `GET /fred/category/tags` | `get_tags` | `fred_category(operation="get_tags", category_id=125)` | `get_category_tags(category_id)` | Get category tags |
| `GET /fred/category/related_tags` | `get_related_tags` | `fred_category(operation="get_related_tags", category_id=125, tag_names="gdp")` | `get_category_related_tags(category_id, tag_names)` | Get related tags |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)
**TODO Reference:** [TODO.md → Phase 4 → Category Tool](TODO.md#category-tool)

---

## Release Endpoints

**MCP Tool:** `fred_release`
**Implementation File:** `src/mcp_fred/tools/release.py`
**API Client File:** `src/mcp_fred/api/endpoints/release.py`

### Plural Endpoints (All Releases)

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/releases` | `list` | `fred_release(operation="list")` | `get_releases()` | Get all releases |
| `GET /fred/releases/dates` | `get_dates` | `fred_release(operation="get_dates")` | `get_releases_dates()` | All release dates |

### Singular Endpoints (Specific Release)

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/release` | `get` | `fred_release(operation="get", release_id=53)` | `get_release(release_id)` | Get release metadata |
| `GET /fred/release/dates` | `get_release_dates` | `fred_release(operation="get_release_dates", release_id=53)` | `get_release_dates(release_id)` | Release dates for specific release |
| `GET /fred/release/series` | `get_series` | `fred_release(operation="get_series", release_id=53)` | `get_release_series(release_id)` | Series in release |
| `GET /fred/release/sources` | `get_sources` | `fred_release(operation="get_sources", release_id=53)` | `get_release_sources(release_id)` | Sources for release |
| `GET /fred/release/tags` | `get_tags` | `fred_release(operation="get_tags", release_id=53)` | `get_release_tags(release_id)` | Tags for release |
| `GET /fred/release/related_tags` | `get_related_tags` | `fred_release(operation="get_related_tags", release_id=53, tag_names="gdp")` | `get_release_related_tags(release_id, tag_names)` | Related tags |
| `GET /fred/release/tables` | `get_tables` | `fred_release(operation="get_tables", release_id=53)` | `get_release_tables(release_id)` | Release tables |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)
**TODO Reference:** [TODO.md → Phase 4 → Release Tool](TODO.md#release-tool)

---

## Series Endpoints

**⚠️ CRITICAL: Large Data Handling Required**

**MCP Tool:** `fred_series`
**Implementation File:** `src/mcp_fred/tools/series.py`
**API Client File:** `src/mcp_fred/api/endpoints/series.py`

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Large Data Risk | Notes |
|-------------------|---------------|-------------------|-------------------|-----------------|-------|
| `GET /fred/series` | `get` | `fred_series(operation="get", series_id="GNPCA")` | `get_series(series_id)` | Low | Series metadata only |
| `GET /fred/series/search` | `search` | `fred_series(operation="search", search_text="gdp")` | `search_series(search_text)` | Medium | Can return many results |
| `GET /fred/series/categories` | `get_categories` | `fred_series(operation="get_categories", series_id="GNPCA")` | `get_series_categories(series_id)` | Low | Categories for series |
| `GET /fred/series/observations` | `get_observations` | `fred_series(operation="get_observations", series_id="GNPCA")` | `get_series_observations(series_id)` | **CRITICAL** | **Up to 100K observations** |
| `GET /fred/series/release` | `get_release` | `fred_series(operation="get_release", series_id="GNPCA")` | `get_series_release(series_id)` | Low | Release for series |
| `GET /fred/series/tags` | `get_tags` | `fred_series(operation="get_tags", series_id="GNPCA")` | `get_series_tags(series_id)` | Low | Tags for series |
| `GET /fred/series/search/tags` | `search_tags` | `fred_series(operation="search_tags", series_search_text="gdp")` | `search_series_tags(series_search_text)` | Low | Search for tags |
| `GET /fred/series/search/related_tags` | `search_related_tags` | `fred_series(operation="search_related_tags", series_search_text="gdp")` | `search_series_related_tags(series_search_text)` | Low | Related tags search |
| `GET /fred/series/updates` | `get_updates` | `fred_series(operation="get_updates")` | `get_series_updates()` | Medium | Recently updated series |
| `GET /fred/series/vintagedates` | `get_vintage_dates` | `fred_series(operation="get_vintage_dates", series_id="GNPCA")` | `get_series_vintage_dates(series_id)` | Low | Vintage dates |

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

**MCP Tool:** `fred_source`
**Implementation File:** `src/mcp_fred/tools/source.py`
**API Client File:** `src/mcp_fred/api/endpoints/source.py`

### Plural Endpoints (All Sources)

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/sources` | `list` | `fred_source(operation="list")` | `get_sources()` | Get all sources |

### Singular Endpoints (Specific Source)

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/source` | `get` | `fred_source(operation="get", source_id=1)` | `get_source(source_id)` | Get source metadata |
| `GET /fred/source/releases` | `get_releases` | `fred_source(operation="get_releases", source_id=1)` | `get_source_releases(source_id)` | Releases from source |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)
**TODO Reference:** [TODO.md → Phase 4 → Source Tool](TODO.md#source-tool)

---

## Tag Endpoints

**MCP Tool:** `fred_tag`
**Implementation File:** `src/mcp_fred/tools/tag.py`
**API Client File:** `src/mcp_fred/api/endpoints/tag.py`

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Notes |
|-------------------|---------------|-------------------|-------------------|-------|
| `GET /fred/tags` | `list` | `fred_tag(operation="list")` | `get_tags()` | Get all tags |
| `GET /fred/tags/series` | `get_series` | `fred_tag(operation="get_series", tag_names="gdp;quarterly")` | `get_tags_series(tag_names)` | Series matching tags |
| `GET /fred/related_tags` | `get_related_tags` | `fred_tag(operation="get_related_tags", tag_names="gdp")` | `get_related_tags(tag_names)` | Related tags |

**Architecture Reference:** [ARCHITECTURE.md → MCP Tool Design](ARCHITECTURE.md#mcp-tool-design)
**TODO Reference:** [TODO.md → Phase 4 → Tag Tool](TODO.md#tag-tool)

---

## Maps Endpoints

**⚠️ CRITICAL: Large Data Handling Required**

**MCP Tool:** `fred_maps`
**Implementation File:** `src/mcp_fred/tools/maps.py`
**API Client File:** `src/mcp_fred/api/endpoints/maps.py`

**Note:** Maps API uses different base path (`/geofred` instead of `/fred`)

| FRED API Endpoint | MCP Operation | Tool Call Example | API Client Method | Large Data Risk | Notes |
|-------------------|---------------|-------------------|-------------------|-----------------|-------|
| `GET /geofred/shapes/file` | `get_shapes` | `fred_maps(operation="get_shapes", shape="state")` | `get_shapes(shape)` | **HIGH** | **Shape files with geo data** |
| `GET /geofred/series/group` | `get_series_group` | `fred_maps(operation="get_series_group", series_id="SMU56000000500000001a")` | `get_series_group(series_id)` | Medium | Series group metadata |
| `GET /geofred/regional/data` | `get_regional_data` | `fred_maps(operation="get_regional_data")` | `get_regional_data()` | **HIGH** | **Regional economic data** |
| `GET /geofred/series/data` | `get_series_data` | `fred_maps(operation="get_series_data", series_id="SMU56000000500000001a")` | `get_series_data(series_id)` | **HIGH** | **Series data for maps** |

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

**Not FRED API endpoints** - Internal MCP server functionality

| MCP Tool | Implementation File | Purpose | Architecture Reference |
|----------|---------------------|---------|----------------------|
| `fred_job_status` | `src/mcp_fred/tools/job_status.py` | Check status of background jobs | [ARCHITECTURE.md → Async Job Management Tool](ARCHITECTURE.md#fred_job_status-tool) |
| `fred_job_list` | `src/mcp_fred/tools/job_list.py` | List recent jobs (optional) | [ARCHITECTURE.md → fred_job_list Tool](ARCHITECTURE.md#fred_job_list-tool-optional) |
| `fred_job_cancel` | `src/mcp_fred/tools/job_cancel.py` | Cancel running jobs (optional) | [ARCHITECTURE.md → fred_job_cancel Tool](ARCHITECTURE.md#fred_job_cancel-tool-optional) |

- `fred_job_status` surfaces job metadata (progress, result, error, timestamps) for a single background operation.
- `fred_job_list` supports filtering by status, pagination (`limit`, `offset`), and sorts jobs by most recent update.
- `fred_job_cancel` marks a job as `cancelled` and records the optional user-supplied reason.

**TODO Reference:** [TODO.md → Phase 4 → Job Management Tools](TODO.md#job-management-tools)

---

## Project Management Tools

**Not FRED API endpoints** - Internal MCP server functionality

| MCP Tool | Implementation File | Purpose | Architecture Reference |
|----------|---------------------|---------|----------------------|
| `fred_project_list` | `src/mcp_fred/tools/project_list.py` | List all projects in storage directory | [ARCHITECTURE.md → fred_project_list Tool](ARCHITECTURE.md#fred_project_list-tool) |
| `fred_project_create` | `src/mcp_fred/tools/project_create.py` | Create new project directory | [ARCHITECTURE.md → fred_project_create Tool](ARCHITECTURE.md#fred_project_create-tool) |
| `fred_project_files` | `src/mcp_fred/tools/project_files.py` | List files in a project | [ARCHITECTURE.md → fred_project_files Tool](ARCHITECTURE.md#fred_project_files-tool) |

- `fred_project_list` returns aggregate metadata (`file_count`, `total_size_bytes`, `latest_modified`) for each project under `FRED_STORAGE_DIR`.
- `fred_project_create` scaffolds the canonical subdirectories (series, maps, releases, categories, sources, tags) and writes `.project.json` metadata.
- `fred_project_files` supports `subdir`, `sort_by` (`name`, `size`, `modified`), and pagination (`limit`, `offset`) while returning per-file size and timestamps.

**TODO Reference:** [TODO.md → Phase 4 → Project Management Tools](TODO.md#project-management-tools)

---

## Utility Components

**Supporting infrastructure for tools**

| Component | Implementation File | Purpose | Used By | Architecture Reference |
|-----------|---------------------|---------|---------|----------------------|
| Token Estimator | `src/mcp_fred/utils/token_estimator.py` | Estimate token count using tiktoken | All tools (auto mode) | [ARCHITECTURE.md → Token Estimation](ARCHITECTURE.md#token-estimation) |
| JSON to CSV Converter | `src/mcp_fred/utils/json_to_csv.py` | Convert FRED JSON to CSV | All tools (CSV output) | [ARCHITECTURE.md → JSON to CSV Conversion](ARCHITECTURE.md#file-formats--json-to-csv-conversion) |
| File Writer | `src/mcp_fred/utils/file_writer.py` | Stream data to CSV/JSON files | All tools (file output) | [ARCHITECTURE.md → Streaming to Files](ARCHITECTURE.md#streaming-to-files) |
| Path Resolver | `src/mcp_fred/utils/path_resolver.py` | Secure path resolution | All tools (file output) | [ARCHITECTURE.md → Security & Validation](ARCHITECTURE.md#security--validation) |
| Job Manager | `src/mcp_fred/utils/job_manager.py` | Async job tracking | Series, Maps tools | [ARCHITECTURE.md → Async Job Architecture](ARCHITECTURE.md#async-job-architecture) |
| Background Worker | `src/mcp_fred/utils/background_worker.py` | Background job processing | Series, Maps tools | [ARCHITECTURE.md → Async Job Architecture](ARCHITECTURE.md#async-job-architecture) |
| Output Handler | `src/mcp_fred/utils/output_handler.py` | Smart output routing | All tools | [ARCHITECTURE.md → Output Handler Integration](ARCHITECTURE.md#output-handler-integration) |

**TODO Reference:** [TODO.md → Phase 3 → Large Data Handling Utilities](TODO.md#large-data-handling-utilities)

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

**Last Updated:** 2025-10-08
**Document Version:** 1.0 (Phase 0.4 Complete)
