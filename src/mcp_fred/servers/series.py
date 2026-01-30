"""FRED Series tools for FastMCP.

This module provides tools for accessing economic time series data,
including observations, metadata, and related information.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..api.endpoints import SeriesAPI
    from ..config import AppConfig
    from ..utils.background_worker import BackgroundWorker
    from ..utils.job_manager import JobManager
    from ..utils.output_handler import ResultOutputHandler
    from ..utils.token_estimator import TokenEstimator


def _get_series(ctx: Context) -> SeriesAPI:
    """Get SeriesAPI from lifespan context."""
    return ctx.lifespan_context["series"]


def _get_config(ctx: Context) -> AppConfig:
    """Get AppConfig from lifespan context."""
    return ctx.lifespan_context["config"]


def _get_token_estimator(ctx: Context) -> TokenEstimator:
    """Get TokenEstimator from lifespan context."""
    return ctx.lifespan_context["token_estimator"]


def _get_job_manager(ctx: Context) -> JobManager:
    """Get JobManager from lifespan context."""
    return ctx.lifespan_context["job_manager"]


def _get_background_worker(ctx: Context) -> BackgroundWorker:
    """Get BackgroundWorker from lifespan context."""
    return ctx.lifespan_context["background_worker"]


def _get_output_handler(ctx: Context) -> ResultOutputHandler:
    """Get ResultOutputHandler from lifespan context."""
    return ctx.lifespan_context["output_handler"]


def _prepare_records(items: Iterable[Any]) -> list[Any]:
    """Convert model objects to dictionaries for token estimation."""
    records: list[Any] = []
    for item in items:
        if hasattr(item, "model_dump"):
            records.append(item.model_dump(by_alias=True))
        else:
            records.append(item)
    return records


def _estimate_tokens(ctx: Context, items: Iterable[Any]) -> int:
    """Estimate token count for a list of items."""
    records = _prepare_records(items)
    if not records:
        return 0
    estimator = _get_token_estimator(ctx)
    return estimator.estimate_records(records)


@mcp.tool(
    tags={"domain:series", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_get(
    series_id: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get metadata for a specific FRED series.

    Returns details about the series including title, units,
    frequency, seasonal adjustment, and observation dates.

    Args:
        series_id: FRED series ID (e.g., "GDP", "UNRATE", "CPIAUCSL")

    Returns:
        Series metadata including title, units, frequency, and date range
    """
    await ctx.debug(f"Fetching series metadata for {series_id}")
    try:
        series = _get_series(ctx)
        result = await series.get_series(series_id)
        estimated_tokens = _estimate_tokens(ctx, result.series)
        return await smart_output(
            ctx,
            result,
            operation="series_get",
            options=OutputOptions(),
            estimated_rows=len(result.series),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_search(
    search_text: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    filter_variable: str | None = None,
    filter_value: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Search for FRED series by keywords.

    Full-text search across series titles, notes, and metadata.
    Use specific economic terms for best results.

    Args:
        search_text: Search query (e.g., "unemployment rate", "GDP growth")
        limit: Maximum results to return (default 100, max 1000)
        offset: Pagination offset
        order_by: Sort field (search_rank, series_id, title, etc.)
        sort_order: Sort direction (asc or desc)
        filter_variable: Filter by variable (frequency, units, etc.)
        filter_value: Value to filter on
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of matching series with relevance scores and metadata
    """
    await ctx.debug(f"Searching series for '{search_text}'")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order
        if filter_variable:
            params["filter_variable"] = filter_variable
        if filter_value:
            params["filter_value"] = filter_value

        result = await series.search_series(search_text, params=params)
        estimated_tokens = _estimate_tokens(ctx, result.series)

        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="series_search",
            options=options,
            estimated_rows=len(result.series),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_observations(
    series_id: str,
    observation_start: str | None = None,
    observation_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    units: str | None = None,
    frequency: str | None = None,
    aggregation_method: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get time series observations (actual data points) for a series.

    This is the primary tool for retrieving economic data values.
    Large requests may be processed asynchronously - check job status if needed.

    Args:
        series_id: FRED series ID (e.g., "GDP", "UNRATE")
        observation_start: Start date (YYYY-MM-DD format)
        observation_end: End date (YYYY-MM-DD format)
        limit: Maximum observations to return
        offset: Pagination offset
        units: Data transformation (lin, chg, ch1, pch, pc1, pca, cch, cca, log)
        frequency: Aggregation frequency (d, w, bw, m, q, sa, a)
        aggregation_method: How to aggregate (avg, sum, eop)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        Time series observations with dates and values
    """
    await ctx.debug(f"Fetching observations for {series_id}")
    try:
        series_api = _get_series(ctx)
        config = _get_config(ctx)
        job_manager = _get_job_manager(ctx)
        background_worker = _get_background_worker(ctx)
        output_handler = _get_output_handler(ctx)

        # Build params
        params: dict[str, Any] = {}
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if units:
            params["units"] = units
        if frequency:
            params["frequency"] = frequency
        if aggregation_method:
            params["aggregation_method"] = aggregation_method

        # Preview to estimate size
        preview_params = dict(params)
        preview_params["limit"] = 1
        preview = await series_api.get_series_observations(series_id, params=preview_params)
        total_count = preview.count if preview.count is not None else len(preview.observations)
        requested_rows = limit if limit is not None else total_count

        # Check if we need background processing
        if requested_rows > config.output.job_row_threshold:
            await ctx.info(f"Large dataset ({requested_rows} rows) - processing in background")
            return await _schedule_observations_job(
                ctx,
                series_id=series_id,
                params=params,
                project=project or config.storage.default_project,
                filename=filename,
                format=format or "csv",
                estimated_rows=requested_rows,
                job_manager=job_manager,
                background_worker=background_worker,
                series_api=series_api,
                output_handler=output_handler,
            )

        # Small enough for direct response
        await ctx.report_progress(0, 100)
        result = await series_api.get_series_observations(series_id, params=params or None)
        await ctx.report_progress(100, 100)

        estimated_tokens = _estimate_tokens(ctx, result.observations)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="series_observations",
            options=options,
            estimated_rows=len(result.observations),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


async def _schedule_observations_job(
    ctx: Context,
    *,
    series_id: str,
    params: dict[str, Any],
    project: str,
    filename: str | None,
    format: str,
    estimated_rows: int,
    job_manager: JobManager,
    background_worker: BackgroundWorker,
    series_api: SeriesAPI,
    output_handler: ResultOutputHandler,
) -> dict[str, Any]:
    """Schedule a background job for large observations requests."""
    job = await job_manager.create_job()
    await job_manager.update_progress(
        job.job_id,
        estimated_total=estimated_rows,
        project=project,
        request={
            "tool": "fred_series_observations",
            "series_id": series_id,
            "params": dict(params),
        },
    )
    await background_worker.start()

    # Capture parameters for the job runner
    original_params = dict(params)

    async def _job_runner() -> None:
        try:
            response = await series_api.get_series_observations(
                series_id, params=original_params or None
            )
            payload = await output_handler.handle(
                data=response,
                operation="series_observations",
                output="file",
                format=format,
                project=project,
                filename=filename,
                estimated_rows=len(response.observations),
                subdir="series",
                job_id=job.job_id,
            )
            await job_manager.complete_job(job.job_id, payload)
        except FREDAPIError as exc:
            await job_manager.fail_job(job.job_id, exc.to_dict())
        except Exception as exc:
            await job_manager.fail_job(
                job.job_id,
                {
                    "code": "JOB_ERROR",
                    "message": str(exc),
                },
            )

    await background_worker.submit(job.job_id, _job_runner)

    estimated_time = max(10, min(900, max(1, estimated_rows // 2000) * 15))

    return {
        "status": "accepted",
        "job_id": job.job_id,
        "message": "Large dataset detected. Processing in background...",
        "estimated_rows": estimated_rows,
        "estimated_time_seconds": estimated_time,
        "output_mode": "file",
        "project": project,
        "series_id": series_id,
        "operation": "series_observations",
        "check_status": "Use fred_job_status tool with this job_id",
    }


@mcp.tool(
    tags={"domain:series", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_categories(
    series_id: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get the categories that contain a specific series.

    Useful for understanding how a series is classified in FRED's taxonomy.

    Args:
        series_id: FRED series ID (e.g., "GDP")

    Returns:
        List of categories containing this series
    """
    await ctx.debug(f"Fetching categories for series {series_id}")
    try:
        series = _get_series(ctx)
        result = await series.get_series_categories(series_id)
        estimated_tokens = _estimate_tokens(ctx, result.categories)
        return await smart_output(
            ctx,
            result,
            operation="series_categories",
            options=OutputOptions(),
            estimated_rows=len(result.categories),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_release(
    series_id: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get the release that contains a specific series.

    Releases group related economic data published together.

    Args:
        series_id: FRED series ID (e.g., "GDP")

    Returns:
        Release details including name, link, and publication info
    """
    await ctx.debug(f"Fetching release for series {series_id}")
    try:
        series = _get_series(ctx)
        result = await series.get_series_release(series_id)
        estimated_tokens = _estimate_tokens(ctx, [result.release])
        return await smart_output(
            ctx,
            result,
            operation="series_release",
            options=OutputOptions(),
            estimated_rows=1,
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_tags(
    series_id: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get tags associated with a specific series.

    Tags describe the series characteristics and enable discovery.

    Args:
        series_id: FRED series ID (e.g., "GDP")
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field (series_count, popularity, created, name, group_id)
        sort_order: Sort direction (asc or desc)

    Returns:
        List of tags with names, group_ids, and metadata
    """
    await ctx.debug(f"Fetching tags for series {series_id}")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await series.get_series_tags(series_id, params=params)
        estimated_tokens = _estimate_tokens(ctx, result.tags)
        return await smart_output(
            ctx,
            result,
            operation="series_tags",
            options=OutputOptions(),
            estimated_rows=len(result.tags),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_search_tags(
    series_search_text: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Search for tags related to a series search.

    Find tags that appear in series matching the search text.

    Args:
        series_search_text: Search query for series
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field
        sort_order: Sort direction (asc or desc)

    Returns:
        List of related tags with series counts
    """
    await ctx.debug(f"Searching tags for series matching '{series_search_text}'")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await series.search_series_tags(series_search_text, params=params)
        estimated_tokens = _estimate_tokens(ctx, result.tags)
        return await smart_output(
            ctx,
            result,
            operation="series_search_tags",
            options=OutputOptions(),
            estimated_rows=len(result.tags),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_search_related_tags(
    series_search_text: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Find tags related to those in series matching a search.

    Discovers tag relationships based on co-occurrence.

    Args:
        series_search_text: Search query for series
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field
        sort_order: Sort direction (asc or desc)

    Returns:
        List of related tags with co-occurrence information
    """
    await ctx.debug(f"Finding related tags for series matching '{series_search_text}'")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await series.search_series_related_tags(series_search_text, params=params)
        estimated_tokens = _estimate_tokens(ctx, result.related_tags)
        return await smart_output(
            ctx,
            result,
            operation="series_search_related_tags",
            options=OutputOptions(),
            estimated_rows=len(result.related_tags),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_updates(
    limit: int = 100,
    offset: int = 0,
    filter_value: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get recently updated FRED series.

    Track what economic data has been recently revised or added.

    Args:
        limit: Maximum series to return (default 100)
        offset: Pagination offset
        filter_value: Filter by update type (all, macro, regional)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of recently updated series with modification timestamps
    """
    await ctx.debug("Fetching recently updated series")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if filter_value:
            params["filter_value"] = filter_value

        result = await series.get_series_updates(params=params)
        estimated_tokens = _estimate_tokens(ctx, result.series)

        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="series_updates",
            options=options,
            estimated_rows=len(result.series),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:series", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_series_vintage_dates(
    series_id: str,
    limit: int | None = None,
    offset: int | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get vintage dates for a series.

    Vintage dates show when data was originally released or revised,
    useful for understanding data revisions over time.

    Args:
        series_id: FRED series ID (e.g., "GDP")
        limit: Maximum dates to return
        offset: Pagination offset
        sort_order: Sort direction (asc or desc)

    Returns:
        List of vintage dates for the series
    """
    await ctx.debug(f"Fetching vintage dates for {series_id}")
    try:
        series = _get_series(ctx)
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_order:
            params["sort_order"] = sort_order

        result = await series.get_series_vintage_dates(series_id, params=params or None)
        estimated_tokens = _estimate_tokens(ctx, result.vintage_dates)
        return await smart_output(
            ctx,
            result,
            operation="series_vintage_dates",
            options=OutputOptions(),
            estimated_rows=len(result.vintage_dates),
            estimated_tokens=estimated_tokens,
            subdir="series",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_series_categories",
    "fred_series_get",
    "fred_series_observations",
    "fred_series_release",
    "fred_series_search",
    "fred_series_search_related_tags",
    "fred_series_search_tags",
    "fred_series_tags",
    "fred_series_updates",
    "fred_series_vintage_dates",
]
