"""FRED Release tools for FastMCP.

This module provides tools for accessing economic data releases,
which group related series that are published together.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output

if TYPE_CHECKING:
    from ..api.endpoints import ReleaseAPI


def _get_releases(ctx: Context) -> ReleaseAPI:
    """Get ReleaseAPI from lifespan context."""
    return ctx.lifespan_context["releases"]


@mcp.tool(
    tags={"domain:release", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_list(
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List all FRED releases.

    Releases are economic data publications that group related series.

    Args:
        limit: Maximum releases to return (default 100)
        offset: Pagination offset
        order_by: Sort field (release_id, name, press_release, etc.)
        sort_order: Sort direction (asc or desc)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of releases with IDs, names, and links
    """
    await ctx.debug("Listing all releases")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await releases.list(params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="release_list",
            options=options,
            estimated_rows=len(result.releases),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_dates(
    limit: int = 100,
    offset: int = 0,
    include_release_dates_with_no_data: bool = False,
    order_by: str | None = None,
    sort_order: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List release dates for all releases.

    Get upcoming and past release dates for economic data publications.

    Args:
        limit: Maximum dates to return (default 100)
        offset: Pagination offset
        include_release_dates_with_no_data: Include dates with no data yet
        order_by: Sort field (release_id, release_date)
        sort_order: Sort direction (asc or desc)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of release dates with release IDs and dates
    """
    await ctx.debug("Listing release dates")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if include_release_dates_with_no_data:
            params["include_release_dates_with_no_data"] = "true"
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await releases.list_dates(params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="release_dates",
            options=options,
            estimated_rows=len(result.release_dates),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_get(
    release_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get details for a specific release.

    Args:
        release_id: The FRED release ID

    Returns:
        Release details including name, link, and notes
    """
    await ctx.debug(f"Fetching release {release_id}")
    try:
        releases = _get_releases(ctx)
        result = await releases.get(release_id)
        return await smart_output(
            ctx,
            result,
            operation="release_get",
            options=OutputOptions(),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_get_dates(
    release_id: int,
    limit: int = 100,
    offset: int = 0,
    include_release_dates_with_no_data: bool = False,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get release dates for a specific release.

    Args:
        release_id: The FRED release ID
        limit: Maximum dates to return (default 100)
        offset: Pagination offset
        include_release_dates_with_no_data: Include dates with no data
        sort_order: Sort direction (asc or desc)

    Returns:
        List of dates when this release is/was published
    """
    await ctx.debug(f"Fetching dates for release {release_id}")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if include_release_dates_with_no_data:
            params["include_release_dates_with_no_data"] = "true"
        if sort_order:
            params["sort_order"] = sort_order

        result = await releases.get_dates(release_id, params=params)
        return await smart_output(
            ctx,
            result,
            operation="release_get_dates",
            options=OutputOptions(),
            estimated_rows=len(result.release_dates),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:data"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_series(
    release_id: int,
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
    """List all series in a release.

    Args:
        release_id: The FRED release ID
        limit: Maximum series to return (default 100, max 1000)
        offset: Pagination offset
        order_by: Sort field (series_id, title, units, frequency, etc.)
        sort_order: Sort direction (asc or desc)
        filter_variable: Filter by variable (frequency, units, etc.)
        filter_value: Value to filter on
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of series in this release with metadata
    """
    await ctx.debug(f"Listing series for release {release_id}")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order
        if filter_variable:
            params["filter_variable"] = filter_variable
        if filter_value:
            params["filter_value"] = filter_value

        result = await releases.list_series(release_id, params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="release_series",
            options=options,
            estimated_rows=len(result.series),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_sources(
    release_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get the sources for a release.

    Sources are organizations that provide the data.

    Args:
        release_id: The FRED release ID

    Returns:
        List of sources that provide data for this release
    """
    await ctx.debug(f"Fetching sources for release {release_id}")
    try:
        releases = _get_releases(ctx)
        result = await releases.list_sources(release_id)
        return await smart_output(
            ctx,
            result,
            operation="release_sources",
            options=OutputOptions(),
            estimated_rows=len(result.sources),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_tags(
    release_id: int,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get tags associated with a release.

    Args:
        release_id: The FRED release ID
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field (series_count, popularity, name, etc.)
        sort_order: Sort direction (asc or desc)

    Returns:
        List of tags for this release
    """
    await ctx.debug(f"Fetching tags for release {release_id}")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await releases.list_tags(release_id, params=params)
        return await smart_output(
            ctx,
            result,
            operation="release_tags",
            options=OutputOptions(),
            estimated_rows=len(result.tags),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_related_tags(
    release_id: int,
    tag_names: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get tags related to specified tags within a release.

    Args:
        release_id: The FRED release ID
        tag_names: Semicolon-separated list of tag names
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field
        sort_order: Sort direction (asc or desc)

    Returns:
        List of related tags
    """
    await ctx.debug(f"Finding related tags for release {release_id}")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await releases.list_related_tags(release_id, tag_names, params=params)
        return await smart_output(
            ctx,
            result,
            operation="release_related_tags",
            options=OutputOptions(),
            estimated_rows=len(result.related_tags),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:release", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_release_tables(
    release_id: int,
    element_id: int | None = None,
    include_observation_values: bool = False,
    observation_date: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get tables (data elements) for a release.

    Some releases organize data into table structures.

    Args:
        release_id: The FRED release ID
        element_id: Specific table element ID (optional)
        include_observation_values: Include actual data values
        observation_date: Date for observation values (YYYY-MM-DD)

    Returns:
        Release tables with structure and optionally data
    """
    await ctx.debug(f"Fetching tables for release {release_id}")
    try:
        releases = _get_releases(ctx)
        params: dict[str, Any] = {}
        if element_id is not None:
            params["element_id"] = element_id
        if include_observation_values:
            params["include_observation_values"] = "true"
        if observation_date:
            params["observation_date"] = observation_date

        result = await releases.list_tables(release_id, params=params or None)
        return await smart_output(
            ctx,
            result,
            operation="release_tables",
            options=OutputOptions(),
            estimated_rows=len(result.release_tables),
            subdir="releases",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_release_dates",
    "fred_release_get",
    "fred_release_get_dates",
    "fred_release_list",
    "fred_release_related_tags",
    "fred_release_series",
    "fred_release_sources",
    "fred_release_tables",
    "fred_release_tags",
]
