"""FRED Category tools for FastMCP.

This module provides tools for browsing and navigating FRED categories,
which organize economic data series into a hierarchical taxonomy.
"""

from __future__ import annotations

from typing import Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from ..api import FREDAPIError
from ..api.endpoints import CategoryAPI
from .base import mcp
from .common import OutputOptions, format_api_error, smart_output


def _get_categories(ctx: Context) -> CategoryAPI:
    """Get CategoryAPI from lifespan context."""
    return ctx.lifespan_context["categories"]


@mcp.tool(
    tags={"domain:category", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_get(
    category_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get details for a specific FRED category.

    Args:
        category_id: The FRED category ID (e.g., 0 for root, 125 for Trade)

    Returns:
        Category details including name, parent_id, and notes
    """
    await ctx.debug(f"Fetching category {category_id}")
    try:
        categories = _get_categories(ctx)
        result = await categories.get(category_id)
        return await smart_output(
            ctx,
            result,
            operation="category_get",
            options=OutputOptions(),
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:category", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_children(
    category_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List child categories under a parent category.

    Use this to navigate down the FRED category hierarchy.
    Start with category_id=0 to see top-level categories.

    Args:
        category_id: Parent category ID (0 for root categories)

    Returns:
        List of child categories with their IDs, names, and parent_ids
    """
    await ctx.debug(f"Listing children of category {category_id}")
    try:
        categories = _get_categories(ctx)
        result = await categories.list_children(category_id)
        return await smart_output(
            ctx,
            result,
            operation="category_children",
            options=OutputOptions(),
            estimated_rows=len(result.categories),
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:category", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_related(
    category_id: int,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List categories related to the given category.

    Related categories share similar economic themes or data types.

    Args:
        category_id: The FRED category ID to find related categories for

    Returns:
        List of related categories with their IDs and names
    """
    await ctx.debug(f"Finding categories related to {category_id}")
    try:
        categories = _get_categories(ctx)
        result = await categories.list_related(category_id)
        return await smart_output(
            ctx,
            result,
            operation="category_related",
            options=OutputOptions(),
            estimated_rows=len(result.categories),
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:category", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_series(
    category_id: int,
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
    """List economic data series within a category.

    Use this to discover what data series are available in a category.
    Results may be large - use limit/offset for pagination.

    Args:
        category_id: The FRED category ID
        limit: Maximum number of series to return (default 100, max 1000)
        offset: Pagination offset for large result sets
        order_by: Sort field (series_id, title, units, frequency, etc.)
        sort_order: Sort direction (asc or desc)
        filter_variable: Filter by variable (frequency, units, seasonal_adjustment)
        filter_value: Value to filter on
        output: Output mode (auto, screen, file)
        format: File format when saving (csv, json)
        project: Project name for file storage
        filename: Custom filename for saved output

    Returns:
        List of series with metadata (id, title, units, frequency, etc.)
    """
    await ctx.debug(f"Listing series in category {category_id}")
    try:
        categories = _get_categories(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order
        if filter_variable:
            params["filter_variable"] = filter_variable
        if filter_value:
            params["filter_value"] = filter_value

        result = await categories.list_series(category_id, params=params)

        options = OutputOptions(
            output=output or "auto",
            format=format or "csv",
            project=project,
            filename=filename,
        )
        return await smart_output(
            ctx,
            result,
            operation="category_series",
            options=options,
            estimated_rows=len(result.series),
            subdir="categories",
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:category", "tier:discovery"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_tags(
    category_id: int,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List tags associated with a category's series.

    Tags help describe and categorize economic data series.

    Args:
        category_id: The FRED category ID
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field (series_count, popularity, created, name, group_id)
        sort_order: Sort direction (asc or desc)

    Returns:
        List of tags with names, group_ids, and series counts
    """
    await ctx.debug(f"Listing tags for category {category_id}")
    try:
        categories = _get_categories(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await categories.list_tags(category_id, params=params)
        return await smart_output(
            ctx,
            result,
            operation="category_tags",
            options=OutputOptions(),
            estimated_rows=len(result.tags),
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


@mcp.tool(
    tags={"domain:category", "tier:advanced"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_category_related_tags(
    category_id: int,
    tag_names: str,
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
    sort_order: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get tags related to specified tags within a category.

    Find tags that commonly appear together with the given tags
    in series within this category.

    Args:
        category_id: The FRED category ID
        tag_names: Semicolon-separated list of tag names (e.g., "gdp;annual")
        limit: Maximum tags to return (default 100)
        offset: Pagination offset
        order_by: Sort field (series_count, popularity, created, name, group_id)
        sort_order: Sort direction (asc or desc)

    Returns:
        List of related tags with co-occurrence information
    """
    await ctx.debug(f"Finding tags related to '{tag_names}' in category {category_id}")
    try:
        categories = _get_categories(ctx)
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if order_by:
            params["order_by"] = order_by
        if sort_order:
            params["sort_order"] = sort_order

        result = await categories.list_related_tags(category_id, tag_names, params=params)
        return await smart_output(
            ctx,
            result,
            operation="category_related_tags",
            options=OutputOptions(),
            estimated_rows=len(result.related_tags),
        )
    except FREDAPIError as exc:
        return format_api_error(exc)


__all__ = [
    "fred_category_children",
    "fred_category_get",
    "fred_category_related",
    "fred_category_related_tags",
    "fred_category_series",
    "fred_category_tags",
]
