"""FRED Source tools for FastMCP.

This module provides tools for accessing information about data sources,
which are the organizations that provide economic data to FRED.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output

if TYPE_CHECKING:
    from ..api.endpoints import SourceAPI


def _get_sources(ctx: Context) -> SourceAPI:
    """Get SourceAPI from lifespan context."""
    return ctx.lifespan_context["sources"]


@mcp.tool(
    tags={"domain:source", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_source_list(
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
    """List all FRED data sources.

    Sources are organizations that provide economic data (e.g., BLS, BEA, Fed).

    Args:
        limit: Maximum sources to return (default 100)
        offset: Pagination offset
        order_by: Sort field (source_id, name, etc.)
        sort_order: Sort direction (asc or desc)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of data sources with IDs, names, and links
    """
    await ctx.debug("Listing all sources")
    try:
        sources = _get_sources(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await sources.list(params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="source_list",
            options=options,
            estimated_rows=len(result.sources),
            subdir="sources",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:source", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_source_get(
    source_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get details for a specific data source.

    Args:
        source_id: The FRED source ID

    Returns:
        Source details including name, link, and notes
    """
    await ctx.debug(f"Fetching source {source_id}")
    try:
        sources = _get_sources(ctx)
        result = await sources.get(source_id)
        return await smart_output(
            ctx,
            result,
            operation="source_get",
            options=OutputOptions(),
            subdir="sources",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:source", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_source_releases(
    source_id: int,
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
    """List releases from a specific data source.

    Args:
        source_id: The FRED source ID
        limit: Maximum releases to return (default 100)
        offset: Pagination offset
        order_by: Sort field (release_id, name, etc.)
        sort_order: Sort direction (asc or desc)
        output: Output mode (auto, screen, file)
        format: File format (csv, json)
        project: Project name for file storage
        filename: Custom filename

    Returns:
        List of releases from this source
    """
    await ctx.debug(f"Listing releases from source {source_id}")
    try:
        sources = _get_sources(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await sources.list_releases(source_id, params=params)
        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="source_releases",
            options=options,
            estimated_rows=len(result.releases),
            subdir="sources",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_source_get",
    "fred_source_list",
    "fred_source_releases",
]
