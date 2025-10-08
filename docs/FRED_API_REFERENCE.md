# FRED API Reference

## Overview

The Federal Reserve Economic Data (FRED) API provides programmatic access to economic data from the Federal Reserve Bank of St. Louis. This document serves as a reference for implementing the MCP server.

**Base URL:** `https://api.stlouisfed.org/fred/`

**Authentication:** All requests require an API key passed as a query parameter: `api_key=YOUR_API_KEY`

**Official Documentation:** https://fred.stlouisfed.org/docs/api/fred/

---

## API Endpoint Categories

### 1. Categories

Category endpoints provide access to FRED's hierarchical category structure.

**Base Endpoint Pattern:** `/fred/category/*`

**Operations:**
- `GET /category` - Get a category
- `GET /category/children` - Get child categories for a specified parent category
- `GET /category/related` - Get related categories for a category
- `GET /category/series` - Get series in a category
- `GET /category/tags` - Get tags for a category
- `GET /category/related_tags` - Get related tags for a category tag

---

### 2. Releases

Release endpoints provide access to statistical releases and their metadata.

**Base Endpoint Pattern:** `/fred/release/*` and `/fred/releases/*`

**Operations (Plural):**
- `GET /releases` - Get all releases of economic data
- `GET /releases/dates` - Get release dates for all releases

**Operations (Singular):**
- `GET /release` - Get a release of economic data
- `GET /release/dates` - Get release dates for a release
- `GET /release/series` - Get series for a release
- `GET /release/sources` - Get sources for a release
- `GET /release/tags` - Get tags for a release
- `GET /release/related_tags` - Get related tags for a release tag
- `GET /release/tables` - Get release tables for a release

---

### 3. Series

Series endpoints provide access to economic data series, observations, and metadata.

**Base Endpoint Pattern:** `/fred/series/*`

**Operations:**
- `GET /series` - Get an economic data series
- `GET /series/search` - Search for economic data series
- `GET /series/categories` - Get categories for a series
- `GET /series/observations` - Get observations/data values for a series
- `GET /series/release` - Get release for a series
- `GET /series/tags` - Get tags for a series
- `GET /series/search/tags` - Search for series tags
- `GET /series/search/related_tags` - Search for related series tags
- `GET /series/updates` - Get series that have been updated
- `GET /series/vintagedates` - Get vintage dates for a series

---

### 4. Sources

Source endpoints provide access to data sources.

**Base Endpoint Pattern:** `/fred/source/*` and `/fred/sources/*`

**Operations (Plural):**
- `GET /sources` - Get all sources of economic data

**Operations (Singular):**
- `GET /source` - Get a source of economic data
- `GET /source/releases` - Get releases for a source

---

### 5. Tags

Tag endpoints provide access to FRED's tagging system.

**Base Endpoint Pattern:** `/fred/tags/*`

**Operations:**
- `GET /tags` - Get all tags
- `GET /tags/series` - Get series matching tags
- `GET /related_tags` - Get related tags for one or more tags

---

### 6. Maps API

The Maps API provides geographical/regional economic data and shape files.

**Base Endpoint Pattern:** `/geofred/*`

**Operations:**
- `GET /geofred/shapes/file` - Get shape files with geographical information
- `GET /geofred/series/group` - Get series group metadata
- `GET /geofred/regional/data` - Get regional data
- `GET /geofred/series/data` - Get series data for maps

**Special Notes:**
- Maps API uses different base path (`geofred` instead of `fred`)
- Provides geographical boundaries and regional economic statistics
- Shape files can be used for data visualization on maps

---

## Common Parameters

### Required Parameters
- `api_key` - Your FRED API key (required for all requests)

### Common Optional Parameters
- `file_type` - Response format: `json` (default), `xml`
- `realtime_start` - Start date for real-time period (YYYY-MM-DD)
- `realtime_end` - End date for real-time period (YYYY-MM-DD)
- `limit` - Maximum number of results to return
- `offset` - Offset for pagination
- `order_by` - Order results by specific field
- `sort_order` - Sort order: `asc` (ascending) or `desc` (descending)

### Series-Specific Parameters
- `series_id` - FRED series ID
- `observation_start` - Start date of observation period (YYYY-MM-DD)
- `observation_end` - End date of observation period (YYYY-MM-DD)
- `units` - Data value transformation: `lin`, `chg`, `ch1`, `pch`, `pc1`, `pca`, `cch`, `cca`, `log`
- `frequency` - Data frequency: `d`, `w`, `bw`, `m`, `q`, `sa`, `a`
- `aggregation_method` - Aggregation method: `avg`, `sum`, `eop`
- `output_type` - Output type for observations

---

## Response Format

All API responses follow a consistent JSON structure:

```json
{
  "realtime_start": "YYYY-MM-DD",
  "realtime_end": "YYYY-MM-DD",
  "observation_start": "YYYY-MM-DD",
  "observation_end": "YYYY-MM-DD",
  "units": "lin",
  "output_type": 1,
  "file_type": "json",
  "order_by": "observation_date",
  "sort_order": "asc",
  "count": 100,
  "offset": 0,
  "limit": 100,
  "[resource_name]": []
}
```

---

## Rate Limits

FRED API rate limits:
- **120 requests per minute** (confirmed)
- No daily limit documented
- Rate limit headers may be returned in responses

### Handling Rate Limits in MCP Server

The MCP server implements:
- Client-side rate limiting to stay under 120 req/min
- Exponential backoff on 429 responses
- Request queue management for concurrent operations

---

## Error Handling

FRED API returns standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

Error responses include a message field describing the error.

---

## Large Dataset Considerations

### Observation Limits

- **Series observations**: Up to **100,000 observations** per request
- **Pagination required** for datasets larger than 100,000 observations
- Use `offset` parameter to retrieve additional data

### Maps/GeoFRED Data

- Shape files can be large (geographical boundary data)
- Regional data may contain thousands of data points
- Series group metadata can reference multiple related series

### MCP Server Strategy for Large Data

The MCP server implements smart output handling:

1. **Token Estimation**: Estimate result size before returning to AI agent
2. **Auto Mode** (default): Automatically save large results to files
3. **File Output**: Stream large datasets directly to CSV/JSON files
4. **Project Organization**: Store data in `{MCP_CLIENT_ROOT}/fred-data/{project-name}/`

**Example Usage with Large Dataset:**

```json
{
  "tool": "fred_series",
  "operation": "get_observations",
  "series_id": "GNPCA",
  "output": "auto",
  "format": "csv",
  "project": "economic-analysis"
}
```

**Response for Large Dataset:**

```json
{
  "status": "success",
  "output_mode": "file",
  "message": "Large dataset detected. Data saved to file.",
  "file_path": "/project/fred-data/economic-analysis/series/GNPCA_observations_20251008_143022.csv",
  "rows_written": 75234,
  "file_size_mb": 3.2,
  "estimated_tokens": 180000,
  "reason": "Estimated 180K tokens exceeds safe limit for Claude Sonnet (140K)"
}
```

### Best Practices

1. **Use `limit` parameter** for exploratory queries
2. **Request file output** (`output=file`) for known large datasets
3. **Specify project name** to organize data by analysis project
4. **Use pagination** for datasets > 100K observations
5. **Monitor rate limits** when making multiple large requests

---

## Notes for Implementation

1. All date parameters use YYYY-MM-DD format
2. Series IDs are case-sensitive
3. The Maps API uses a different base path (`geofred`)
4. Some endpoints support both JSON and XML responses
5. Pagination is supported via `limit` and `offset` parameters
6. Real-time data periods allow querying historical revisions of data
7. **Large datasets** (>100K observations) require pagination or file output

---

## References

- Official FRED API Documentation: https://fred.stlouisfed.org/docs/api/fred/
- FRED Website: https://fred.stlouisfed.org/
- Get API Key: https://fred.stlouisfed.org/docs/api/api_key.html
