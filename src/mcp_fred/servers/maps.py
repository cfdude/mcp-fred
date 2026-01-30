"""FRED GeoFRED Maps tools for FastMCP.

This module provides tools for accessing geographic economic data
through the GeoFRED service.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Iterable

    from ..api.endpoints import MapsAPI
    from ..utils.background_worker import BackgroundWorker
    from ..utils.job_manager import JobManager
    from ..utils.output_handler import ResultOutputHandler
    from ..utils.token_estimator import TokenEstimator


def _get_maps(ctx: Context) -> MapsAPI:
    """Get MapsAPI from lifespan context."""
    return ctx.lifespan_context["maps"]


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


async def _schedule_maps_job(
    ctx: Context,
    *,
    operation: str,
    project: str,
    filename: str | None,
    format: str,
    params: dict[str, Any],
    record_getter: Callable[[Any], Iterable[Any]],
    fetcher: Callable[[], Awaitable[Any]],
) -> dict[str, Any]:
    """Schedule a background job for large map data requests."""
    job_manager = _get_job_manager(ctx)
    background_worker = _get_background_worker(ctx)
    output_handler = _get_output_handler(ctx)

    job = await job_manager.create_job()
    await job_manager.update_progress(
        job.job_id,
        project=project,
        request={"tool": f"fred_maps_{operation}", "params": dict(params)},
    )
    await background_worker.start()

    async def _job_runner() -> None:
        try:
            response = await fetcher()
            records = list(record_getter(response))
            estimated_tokens = _estimate_tokens(ctx, records)
            payload = await output_handler.handle(
                data=response,
                operation=operation,
                output="file",
                format=format,
                project=project,
                filename=filename,
                estimated_rows=len(records),
                estimated_tokens=estimated_tokens,
                subdir="maps",
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

    return {
        "status": "accepted",
        "job_id": job.job_id,
        "message": "Large map dataset detected. Processing in background...",
        "operation": operation,
        "project": project,
        "check_status": "Use fred_job_status tool with this job_id",
    }


@mcp.tool(
    tags={"domain:maps", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_maps_shapes(
    shape: str,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get geographic shape data from GeoFRED.

    Geographic shapes include states, counties, MSAs, etc.
    Note: Shape data can be large and is typically saved to file.

    Args:
        shape: Shape type (bea, msa, state, county, country, censusdivision,
               censusregion, necta)
        output: Output mode (auto defaults to file for large data)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        Geographic shape data with region codes and names
    """
    await ctx.debug(f"Fetching shapes for {shape}")
    try:
        maps = _get_maps(ctx)
        config = ctx.lifespan_context["config"]

        # Shape data is typically large, default to file output
        output_mode = output or "file"
        fmt = format or "csv"
        project_name = project or config.storage.default_project

        if output_mode == "file":
            return await _schedule_maps_job(
                ctx,
                operation="shapes",
                project=project_name,
                filename=filename,
                format=fmt,
                params={"shape": shape},
                record_getter=lambda resp: resp.shape_values,
                fetcher=lambda: maps.get_shapes(shape),
            )

        result = await maps.get_shapes(shape)
        estimated_tokens = _estimate_tokens(ctx, result.shape_values)
        options = OutputOptions(
            output=output_mode,
            format=fmt,
            project=project_name,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="maps_shapes",
            options=options,
            estimated_rows=len(result.shape_values),
            estimated_tokens=estimated_tokens,
            subdir="maps",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:maps", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_maps_series_group(
    series_id: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get the series group for a GeoFRED series.

    Series groups contain related regional series.

    Args:
        series_id: A GeoFRED series ID

    Returns:
        Series group information with related series
    """
    await ctx.debug(f"Fetching series group for {series_id}")
    try:
        maps = _get_maps(ctx)
        result = await maps.get_series_group(series_id)
        estimated_tokens = _estimate_tokens(ctx, result.series)
        return await smart_output(
            ctx,
            result,
            operation="maps_series_group",
            options=OutputOptions(),
            estimated_rows=len(result.series),
            estimated_tokens=estimated_tokens,
            subdir="maps",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:maps", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_maps_regional_data(
    series_group: str | None = None,
    region_type: str | None = None,
    date: str | None = None,
    start_date: str | None = None,
    frequency: str | None = None,
    units: str | None = None,
    season: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get regional data from GeoFRED.

    Retrieve economic data aggregated by geographic region.
    Note: Regional data can be large and is typically saved to file.

    Args:
        series_group: Series group ID
        region_type: Region type (bea, msa, state, county, etc.)
        date: Specific date (YYYY-MM-DD)
        start_date: Start date for range
        frequency: Data frequency (a, sa, q, m, w, d)
        units: Data units
        season: Seasonal adjustment
        output: Output mode (auto defaults to file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        Regional economic data by geography
    """
    await ctx.debug("Fetching regional data")
    try:
        maps = _get_maps(ctx)
        config = ctx.lifespan_context["config"]

        params: dict[str, Any] = {}
        if series_group:
            params["series_group"] = series_group
        if region_type:
            params["region_type"] = region_type
        if date:
            params["date"] = date
        if start_date:
            params["start_date"] = start_date
        if frequency:
            params["frequency"] = frequency
        if units:
            params["units"] = units
        if season:
            params["season"] = season

        # Regional data is typically large, default to file output
        output_mode = output or "file"
        fmt = format or "csv"
        project_name = project or config.storage.default_project

        if output_mode == "file":
            return await _schedule_maps_job(
                ctx,
                operation="regional_data",
                project=project_name,
                filename=filename,
                format=fmt,
                params=params,
                record_getter=lambda resp: resp.regional_data,
                fetcher=lambda: maps.get_regional_data(params=params or None),
            )

        result = await maps.get_regional_data(params=params or None)
        estimated_tokens = _estimate_tokens(ctx, result.regional_data)
        options = OutputOptions(
            output=output_mode,
            format=fmt,
            project=project_name,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="maps_regional_data",
            options=options,
            estimated_rows=len(result.regional_data),
            estimated_tokens=estimated_tokens,
            subdir="maps",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:maps", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_maps_series_data(
    series_id: str,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get data for a specific GeoFRED series.

    Note: Series data can be large and is typically saved to file.

    Args:
        series_id: GeoFRED series ID
        output: Output mode (auto defaults to file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        Time series data for the geographic series
    """
    await ctx.debug(f"Fetching data for series {series_id}")
    try:
        maps = _get_maps(ctx)
        config = ctx.lifespan_context["config"]

        # Series data is typically large, default to file output
        output_mode = output or "file"
        fmt = format or "csv"
        project_name = project or config.storage.default_project

        if output_mode == "file":
            return await _schedule_maps_job(
                ctx,
                operation="series_data",
                project=project_name,
                filename=filename,
                format=fmt,
                params={"series_id": series_id},
                record_getter=lambda resp: resp.series_data,
                fetcher=lambda: maps.get_series_data(series_id),
            )

        result = await maps.get_series_data(series_id)
        estimated_tokens = _estimate_tokens(ctx, result.series_data)
        options = OutputOptions(
            output=output_mode,
            format=fmt,
            project=project_name,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="maps_series_data",
            options=options,
            estimated_rows=len(result.series_data),
            estimated_tokens=estimated_tokens,
            subdir="maps",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_maps_regional_data",
    "fred_maps_series_data",
    "fred_maps_series_group",
    "fred_maps_shapes",
]
