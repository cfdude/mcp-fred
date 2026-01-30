"""FRED Admin tools for FastMCP.

This module provides administrative tools for:
- Project management (storage organization)
- Job management (async task tracking)
- Progressive disclosure (tool activation)
"""

from __future__ import annotations

import datetime as dt
import json
import re
from typing import TYPE_CHECKING, Any

from fastmcp.server.context import Context
from fastmcp.server.dependencies import CurrentContext

from .base import mcp
from .common import OutputOptions, smart_output

if TYPE_CHECKING:
    from ..utils.job_manager import Job, JobManager
    from ..utils.path_resolver import PathResolver


VALID_PROJECT_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
SUBDIRECTORIES = ["series", "maps", "releases", "categories", "sources", "tags"]
VALID_STATUSES = {None, "accepted", "processing", "completed", "failed", "cancelled"}


def _get_job_manager(ctx: Context) -> JobManager:
    """Get JobManager from lifespan context."""
    return ctx.lifespan_context["job_manager"]


def _get_path_resolver(ctx: Context) -> PathResolver:
    """Get PathResolver from lifespan context."""
    return ctx.lifespan_context["path_resolver"]


def _serialize_job(job: Job) -> dict[str, Any]:
    """Serialize a Job object to a dictionary."""
    return {
        "job_id": job.job_id,
        "status": job.status.value,
        "progress": job.progress,
        "result": job.result,
        "error": job.error,
        "retry_count": job.retry_count,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
    }


# =============================================================================
# Progressive Disclosure Tools (Always Visible)
# =============================================================================


@mcp.tool(
    tags={"tier:core"},
    annotations={"readOnlyHint": False, "idempotentHint": True},
)
async def activate_data_tools(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Activate data retrieval tools for this session.

    Call this when you need to retrieve actual economic data values
    like time series observations, release dates, or geographic data.

    Returns:
        Confirmation of activation with list of enabled tools
    """
    await ctx.info("Activating data tools for session")
    await ctx.enable_components(tags={"tier:data"})

    return {
        "status": "activated",
        "tier": "data",
        "description": "Data retrieval tools are now available for this session",
        "enabled_tools": [
            "fred_series_observations - Get time series data points",
            "fred_release_dates - Get release date schedules",
            "fred_release_series - Get series in a release",
            "fred_release_get_dates - Get dates for a specific release",
            "fred_maps_shapes - Get geographic shape data",
            "fred_maps_regional_data - Get regional economic data",
            "fred_maps_series_data - Get GeoFRED series data",
        ],
    }


@mcp.tool(
    tags={"tier:core"},
    annotations={"readOnlyHint": False, "idempotentHint": True},
)
async def activate_advanced_tools(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Activate advanced query tools for this session.

    Call this when you need complex tag queries, related tag discovery,
    vintage date access, or release table structures.

    Returns:
        Confirmation of activation with list of enabled tools
    """
    await ctx.info("Activating advanced tools for session")
    await ctx.enable_components(tags={"tier:advanced"})

    return {
        "status": "activated",
        "tier": "advanced",
        "description": "Advanced query tools are now available for this session",
        "enabled_tools": [
            "fred_category_related_tags - Find tags related to category tags",
            "fred_series_search_tags - Get tags for search results",
            "fred_series_search_related_tags - Find related tags in search",
            "fred_series_vintage_dates - Get revision history dates",
            "fred_release_related_tags - Find tags related to release tags",
            "fred_release_tables - Get release data tables",
        ],
    }


@mcp.tool(
    tags={"tier:core"},
    annotations={"readOnlyHint": False, "idempotentHint": True},
)
async def activate_admin_tools(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Activate administrative tools for this session.

    Call this when you need project management or job tracking capabilities.

    Returns:
        Confirmation of activation with list of enabled tools
    """
    await ctx.info("Activating admin tools for session")
    await ctx.enable_components(tags={"tier:admin"})

    return {
        "status": "activated",
        "tier": "admin",
        "description": "Administrative tools are now available for this session",
        "enabled_tools": [
            "fred_project_list - List project workspaces",
            "fred_project_create - Create a new project",
            "fred_job_list - List background jobs",
            "fred_job_cancel - Cancel a background job",
        ],
    }


@mcp.tool(
    tags={"tier:core"},
    annotations={"readOnlyHint": False, "idempotentHint": True},
)
async def activate_all_tools(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Activate all FRED tools for this session.

    Call this for full API access including data, advanced, and admin tools.

    Returns:
        Confirmation of activation with summary of all enabled tiers
    """
    await ctx.info("Activating all tools for session")
    await ctx.enable_components(tags={"tier:data", "tier:advanced", "tier:admin"})

    return {
        "status": "activated",
        "description": "All FRED tools are now available for this session",
        "enabled_tiers": {
            "data": {
                "count": 7,
                "description": "Time series observations, release data, geographic data",
            },
            "advanced": {
                "count": 6,
                "description": "Complex tag queries, vintage dates, release tables",
            },
            "admin": {
                "count": 4,
                "description": "Project and job management",
            },
        },
        "total_additional_tools": 17,
    }


@mcp.tool(
    tags={"tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def list_tool_tiers(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List all FRED tool tiers and how to activate them.

    Shows available tool categories with their activation commands.

    Returns:
        Summary of tool tiers with activation instructions
    """
    return {
        "total_tools": 39,
        "always_available": {
            "core": {
                "count": 8,
                "description": "Essential tools for basic operations",
                "examples": ["fred_category_get", "fred_series_get", "fred_release_get"],
            },
            "discovery": {
                "count": 15,
                "description": "Tools for exploring and searching data",
                "examples": ["fred_series_search", "fred_tag_list", "fred_category_children"],
            },
        },
        "activatable_tiers": {
            "data": {
                "count": 7,
                "description": "Tools for retrieving actual data values",
                "examples": ["fred_series_observations", "fred_maps_regional_data"],
                "activate_with": "activate_data_tools()",
            },
            "advanced": {
                "count": 6,
                "description": "Complex query and exploration tools",
                "examples": ["fred_series_vintage_dates", "fred_release_tables"],
                "activate_with": "activate_advanced_tools()",
            },
            "admin": {
                "count": 4,
                "description": "Project and job management",
                "examples": ["fred_project_list", "fred_job_status"],
                "activate_with": "activate_admin_tools()",
            },
        },
        "tip": "Use activate_all_tools() to enable all tiers at once",
    }


# =============================================================================
# Job Management Tools
# =============================================================================


@mcp.tool(
    tags={"domain:admin", "tier:core"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_job_status(
    job_id: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Get the status of a background job.

    Use this to check on large data requests that were processed asynchronously.

    Args:
        job_id: The job ID returned when a background job was started

    Returns:
        Job status including progress, result, or error information
    """
    await ctx.debug(f"Checking status of job {job_id}")
    job_manager = _get_job_manager(ctx)

    job = await job_manager.get_job(job_id)
    if job is None:
        return {
            "error": {
                "code": "JOB_NOT_FOUND",
                "message": f"Job '{job_id}' was not found.",
                "details": {"job_id": job_id},
            }
        }

    payload = _serialize_job(job)
    return await smart_output(
        ctx,
        payload,
        operation="job_status",
        options=OutputOptions(),
        estimated_rows=1,
    )


@mcp.tool(
    tags={"domain:admin", "tier:admin"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_job_list(
    status: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List background jobs.

    Args:
        status: Filter by status (accepted, processing, completed, failed, cancelled)
        limit: Maximum jobs to return
        offset: Pagination offset

    Returns:
        List of jobs with their status and metadata
    """
    await ctx.debug("Listing jobs")
    job_manager = _get_job_manager(ctx)

    # Validate status filter
    if status is not None and status not in VALID_STATUSES:
        return {
            "error": {
                "code": "INVALID_STATUS_FILTER",
                "message": f"Status '{status}' is not supported.",
                "details": {"allowed": sorted([s for s in VALID_STATUSES if s])},
            }
        }

    jobs_map = await job_manager.list_jobs()
    jobs = sorted(jobs_map.values(), key=lambda j: j.updated_at, reverse=True)

    # Filter by status if provided
    if status:
        jobs = [j for j in jobs if j.status.value == status]

    total = len(jobs)
    end = offset + limit if limit is not None else None
    sliced = jobs[offset:end]

    payload = {
        "count": total,
        "offset": offset,
        "limit": limit,
        "jobs": [_serialize_job(job) for job in sliced],
    }

    return await smart_output(
        ctx,
        payload,
        operation="job_list",
        options=OutputOptions(),
        estimated_rows=len(sliced),
        subdir="jobs",
    )


@mcp.tool(
    tags={"domain:admin", "tier:admin"},
    annotations={"readOnlyHint": False, "idempotentHint": False},
)
async def fred_job_cancel(
    job_id: str,
    reason: str | None = None,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Cancel a background job.

    Args:
        job_id: The job ID to cancel
        reason: Optional reason for cancellation

    Returns:
        Confirmation of cancellation
    """
    await ctx.debug(f"Cancelling job {job_id}")
    job_manager = _get_job_manager(ctx)

    cancelled = await job_manager.cancel_job(job_id, reason)
    if not cancelled:
        return {
            "error": {
                "code": "JOB_NOT_FOUND",
                "message": f"Job '{job_id}' was not found.",
                "details": {"job_id": job_id},
            }
        }

    payload = {
        "job_id": job_id,
        "status": "cancelled",
        "reason": reason,
    }

    return await smart_output(
        ctx,
        payload,
        operation="job_cancel",
        options=OutputOptions(),
        estimated_rows=1,
        subdir="jobs",
    )


# =============================================================================
# Project Management Tools
# =============================================================================


@mcp.tool(
    tags={"domain:admin", "tier:admin"},
    annotations={"readOnlyHint": True, "idempotentHint": True},
)
async def fred_project_list(
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """List available project workspaces.

    Projects organize downloaded data into separate directories.

    Returns:
        List of projects with their paths and metadata
    """
    await ctx.debug("Listing projects")
    path_resolver = _get_path_resolver(ctx)

    root = path_resolver.root
    if not root.exists():
        return {
            "error": {
                "code": "STORAGE_NOT_AVAILABLE",
                "message": "The configured storage directory is not accessible.",
                "details": {"directory": str(root)},
            }
        }

    projects = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir():
            projects.append(_gather_project_metadata(entry))

    payload = {
        "count": len(projects),
        "projects": projects,
    }

    return await smart_output(
        ctx,
        payload,
        operation="project_list",
        options=OutputOptions(),
        estimated_rows=len(projects),
        subdir="projects",
    )


def _gather_project_metadata(project_dir: Any) -> dict[str, Any]:
    """Gather metadata about a project directory."""
    total_size = 0
    file_count = 0
    latest_modified: dt.datetime | None = None

    for item in project_dir.rglob("*"):
        if item.is_file():
            file_count += 1
            try:
                stat = item.stat()
            except OSError:
                continue
            total_size += stat.st_size
            mtime = dt.datetime.fromtimestamp(stat.st_mtime, tz=dt.UTC)
            if latest_modified is None or mtime > latest_modified:
                latest_modified = mtime

    return {
        "project": project_dir.name,
        "path": str(project_dir),
        "file_count": file_count,
        "total_size_bytes": total_size,
        "latest_modified": latest_modified.isoformat() if latest_modified else None,
    }


@mcp.tool(
    tags={"domain:admin", "tier:admin"},
    annotations={"readOnlyHint": False, "idempotentHint": False},
)
async def fred_project_create(
    project: str,
    ctx: Context = CurrentContext(),
) -> dict[str, Any]:
    """Create a new project workspace.

    Projects organize downloaded data into separate directories with
    standardized subdirectories for different data types.

    Args:
        project: Project name (letters, numbers, hyphens, underscores only)

    Returns:
        Project creation confirmation with paths
    """
    await ctx.debug(f"Creating project '{project}'")
    path_resolver = _get_path_resolver(ctx)

    # Validate project name
    if not project or not VALID_PROJECT_NAME.fullmatch(project):
        return {
            "error": {
                "code": "INVALID_PROJECT_NAME",
                "message": "Project names must use letters, numbers, hyphens, or underscores only.",
                "details": {"project": project},
            }
        }

    root = path_resolver.root
    project_dir = root / project
    if project_dir.exists():
        return {
            "error": {
                "code": "PROJECT_EXISTS",
                "message": f"Project '{project}' already exists.",
                "details": {"project": project},
            }
        }

    # Create project directory and subdirectories
    project_dir.mkdir(parents=True, exist_ok=True)
    for subdir in SUBDIRECTORIES:
        (project_dir / subdir).mkdir(exist_ok=True)

    # Create metadata file
    metadata_path = project_dir / ".project.json"
    metadata = {
        "project": project,
        "created_at": dt.datetime.now(dt.UTC).isoformat(),
        "subdirectories": SUBDIRECTORIES,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {
        "project": project,
        "path": str(project_dir),
        "metadata_file": str(metadata_path),
    }

    await ctx.info(f"Created project '{project}' at {project_dir}")

    return await smart_output(
        ctx,
        payload,
        operation="project_create",
        options=OutputOptions(),
        estimated_rows=1,
        subdir="projects",
    )


__all__ = [
    "activate_admin_tools",
    "activate_advanced_tools",
    "activate_all_tools",
    "activate_data_tools",
    "fred_job_cancel",
    "fred_job_list",
    "fred_job_status",
    "fred_project_create",
    "fred_project_list",
    "list_tool_tiers",
]
