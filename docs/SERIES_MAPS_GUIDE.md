# Series & Maps Tool Guide

This guide describes how to use the `fred_series` and `fred_maps` MCP tools,
including recommended parameters, output options, and strategies for handling
large datasets.

## fred_series

### Common Operations

| Operation | Description | Required Parameters |
|-----------|-------------|---------------------|
| `get` | Fetch metadata for a series | `series_id` |
| `get_observations` | Download observations for a series | `series_id`, optional `observation_start`, `observation_end` |
| `search` | Find series by search text | `search_text` |
| `get_categories` | List categories for a series | `series_id` |
| `get_tags` | List tags attached to a series | `series_id` |
| `search_tags` | Find tags for matching series | `series_search_text` |
| `get_updates` | Recently updated series list | optional `filter` params |
| `get_vintage_dates` | Vintage revision dates | `series_id` |

### Output Guidance

- Default `output="auto"` estimates tokens/rows and saves to project storage
  when the payload is large. Override with `screen` for quick inspection.
- Set `project` to group related exports: `project="macro-insights"`.
- Use `filename` to enforce deterministic names for automation.
- Configure chunk size via `FRED_OUTPUT_FILE_CHUNK_SIZE` (default 1000 rows).

### Working With Large Observations

1. Call `fred_series(operation="get", series_id=...)` to confirm metadata.
2. For long history, supply `observation_start` to limit tokens.
3. If the result is still large, the server writes directly to CSV using
   chunked streaming and returns `file_size_bytes` in the response.
4. Large pulls automatically return a `status="accepted"` job response—poll
   `fred_job_status` until `rows_written` and `bytes_written` settle, then
   retrieve the exported file.
5. For background processing tool details, see Phase 3 async job docs.

## fred_maps

### Common Operations

| Operation | Description | Required Parameters |
|-----------|-------------|---------------------|
| `get_shapes` | Download GeoFRED shape data | `shape` (e.g. `state`, `county`) |
| `get_series_group` | Retrieve map series grouping metadata | `series_id` |
| `get_regional_data` | Regional statistics for a map | optional filters |
| `get_series_data` | Region-level values for a series | `series_id` |

### Output Guidance

- Shape responses default to file output to avoid huge screen payloads.
- Use `format="json"` when downstream tools expect raw GeoJSON-like content.
- All exported files are placed under `{project}/maps/`.
- Combine with `fred_series(search=...)` to discover compatible map series.
- CSV exports flatten nested GeoFRED fields (e.g., `properties_state_abbr`, `metadata_units`).
  Refer to `tests/fixtures/maps/` for sample payloads.

### Large Map Data Tips

- For multi-megabyte shape files, rely on the returned `file_size_bytes` to
  estimate download completion.
- When debugging, force `output="screen"` to view a truncated payload.
- Use project-based naming so AI agents can reference previously created maps.
- Background jobs surface `bytes_written` progress—check `fred_job_status` before accessing results.

## Configuration Reference

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `FRED_OUTPUT_MODE` | Default output mode (`auto`, `screen`, `file`) | `auto` |
| `FRED_OUTPUT_FORMAT` | Default format (`csv`, `json`) | `csv` |
| `FRED_OUTPUT_FILE_CHUNK_SIZE` | Rows per CSV write flush | `1000` |
| `FRED_STORAGE_DIR` | Root directory for exports | `./fred-data` |

For full configuration details refer to `docs/DEVELOPMENT_GUIDE.md` and
`docs/ARCHITECTURE.md`.

---

With this guide, you can instruct AI agents to retrieve series and map data
confidently while keeping large responses manageable.
