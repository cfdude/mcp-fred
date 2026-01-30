"""Shared utilities for FastMCP tool implementations."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastmcp.server.context import Context

    from ..utils.output_handler import ResultOutputHandler


@dataclass
class OutputOptions:
    """Options controlling how tool results are returned."""

    output: str = "auto"  # auto, screen, file
    format: str = "csv"  # csv, json
    project: str | None = None
    filename: str | None = None


async def smart_output(
    ctx: Context,
    data: Any,
    *,
    operation: str,
    options: OutputOptions | None = None,
    estimated_rows: int | None = None,
    estimated_tokens: int | None = None,
    subdir: str | None = None,
    job_id: str | None = None,
) -> dict[str, Any]:
    """Handle tool output with automatic offloading for large payloads.

    Uses the ResultOutputHandler from lifespan_context to intelligently
    decide whether to return data inline or save to file.
    """
    opts = options or OutputOptions()
    output_handler: ResultOutputHandler = ctx.lifespan_context["output_handler"]

    return await output_handler.handle(
        data=data,
        operation=operation,
        output=opts.output,
        format=opts.format,
        project=opts.project,
        filename=opts.filename,
        estimated_rows=estimated_rows,
        estimated_tokens=estimated_tokens,
        subdir=subdir,
        job_id=job_id,
    )


def extract_output_options(
    output: str | None = None,
    format: str | None = None,
    project: str | None = None,
    filename: str | None = None,
) -> OutputOptions:
    """Create OutputOptions from tool parameters."""
    return OutputOptions(
        output=output or "auto",
        format=format or "csv",
        project=project,
        filename=filename,
    )


def format_api_error(error: Any) -> dict[str, Any]:
    """Format a FREDAPIError for tool response."""
    if hasattr(error, "to_dict"):
        return error.to_dict()
    return {
        "error": {
            "code": "API_ERROR",
            "message": str(error),
        }
    }


def format_timestamp() -> str:
    """Generate a timestamp string for filenames."""
    return dt.datetime.now(dt.UTC).strftime("%Y%m%d_%H%M%S")


__all__ = [
    "OutputOptions",
    "extract_output_options",
    "format_api_error",
    "format_timestamp",
    "smart_output",
]
