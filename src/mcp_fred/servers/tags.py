"""FRED Tag tools for FastMCP.

This module provides tools for tag-based discovery and exploration
of FRED economic data series.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output

if TYPE_CHECKING:
    from ..api.endpoints import TagAPI


def _get_tags(ctx: Context) -> TagAPI:
    """Get TagAPI from lifespan context."""
    return ctx.lifespan_context["tags"]


@mcp.tool(
    tags={"domain:tag", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_tag_list(
    limit: int = 100,
    offset: int = 0,
    tag_group_id: str | None = None,
    search_text: str | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List FRED tags.

    Tags categorize and describe economic data series.

    Args:
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        tag_group_id: Filter by tag group (freq, gen, geo, geot, rls, seas, src)
        search_text: Filter tags by search text
        order_by: Sort field (series_count, popularity, created, name, group_id)
        sort_order: Sort direction (asc or desc)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of tags with names, group_ids, and series counts
    """
    await ctx.debug("Listing tags")
    try:
        tags = _get_tags(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if tag_group_id:
            params["tag_group_id"] = tag_group_id
        if search_text:
            params["search_text"] = search_text
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await tags.list(params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="tag_list",
            options=options,
            estimated_rows=len(result.tags),
            subdir="tags",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:tag", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_tag_series(
    tag_names: str,
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
    """Get series matching specific tags.

    Find series that have ALL of the specified tags.

    Args:
        tag_names: Semicolon-separated tag names (e.g., "gdp;annual")
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
        List of series with all specified tags
    """
    await ctx.debug(f"Finding series with tags '{tag_names}'")
    try:
        tags = _get_tags(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order
        if filter_variable:
            params["filter_variable"] = filter_variable
        if filter_value:
            params["filter_value"] = filter_value

        result = await tags.list_series(tag_names, params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="tag_series",
            options=options,
            estimated_rows=len(result.series),
            subdir="tags",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:tag", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_tag_related(
    tag_names: str,
    limit: int = 100,
    offset: int = 0,
    exclude_tag_names: str | None = None,
    tag_group_id: str | None = None,
    search_text: str | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Find tags related to specified tags.

    Discovers tags that commonly co-occur with the given tags.

    Args:
        tag_names: Semicolon-separated tag names (e.g., "gdp;annual")
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        exclude_tag_names: Tags to exclude from results
        tag_group_id: Filter by tag group
        search_text: Filter by search text
        order_by: Sort field
        sort_order: Sort direction (asc or desc)

    Returns:
        List of related tags with co-occurrence information
    """
    await ctx.debug(f"Finding tags related to '{tag_names}'")
    try:
        tags = _get_tags(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if exclude_tag_names:
            params["exclude_tag_names"] = exclude_tag_names
        if tag_group_id:
            params["tag_group_id"] = tag_group_id
        if search_text:
            params["search_text"] = search_text
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await tags.list_related(tag_names, params=params)
        return await smart_output(
            ctx,
            result,
            operation="tag_related",
            options=OutputOptions(),
            estimated_rows=len(result.related_tags),
            subdir="tags",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_tag_list",
    "fred_tag_related",
    "fred_tag_series",
]
