"""Implement the `fred_project_files` MCP tool."""

from __future__ import annotations

import datetime as dt
import re
from typing import TYPE_CHECKING, Any

from . import _common

if TYPE_CHECKING:  # pragma: no cover - typing helper
    from pathlib import Path

    from ..server import ServerContext


SUPPORTED_OPERATIONS = ["list"]
VALID_SUBDIRS = {None, "series", "maps", "releases", "categories", "sources", "tags"}
VALID_SORT_FIELDS = {"name", "size", "modified"}
VALID_SORT_ORDERS = {"asc", "desc"}
VALID_PROJECT_NAME = re.compile(r"^[A-Za-z0-9_-]+$")


def _missing_project(project: str) -> dict[str, Any]:
    return {
        "error": {
            "code": "PROJECT_NOT_FOUND",
            "message": f"Project '{project}' does not exist.",
            "details": {"project": project},
        }
    }


def _invalid_subdir(subdir: str) -> dict[str, Any]:
    return {
        "error": {
            "code": "INVALID_SUBDIRECTORY",
            "message": f"Subdirectory '{subdir}' is not supported.",
            "details": {"allowed": sorted(v for v in VALID_SUBDIRS if v)},
        }
    }


def _invalid_sort(field: str) -> dict[str, Any]:
    return {
        "error": {
            "code": "INVALID_SORT_FIELD",
            "message": f"Sort field '{field}' is not supported.",
            "details": {"allowed": sorted(VALID_SORT_FIELDS)},
        }
    }


def _invalid_sort_order(order: str) -> dict[str, Any]:
    return {
        "error": {
            "code": "INVALID_SORT_ORDER",
            "message": f"Sort order '{order}' is not supported.",
            "details": {"allowed": sorted(VALID_SORT_ORDERS)},
        }
    }


def _parse_int(value: Any, name: str) -> tuple[int | None, dict[str, Any] | None]:
    if value is None:
        return None, None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None, _common.invalid_parameter(name, "an integer")
    if parsed < 0:
        return None, _common.invalid_parameter(name, "a non-negative integer")
    return parsed, None


def _gather_files(project_dir: Path, target_dir: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in target_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        files.append(
            {
                "name": path.name,
                "relative_path": str(path.relative_to(project_dir)),
                "size_bytes": stat.st_size,
                "modified_at": dt.datetime.fromtimestamp(stat.st_mtime, tz=dt.UTC).isoformat(),
                "path": str(path),
            }
        )
    return files


def _sort_files(files: list[dict[str, Any]], field: str, order: str) -> None:
    reverse = order == "desc"
    if field == "name":
        files.sort(key=lambda item: item["relative_path"], reverse=reverse)
    elif field == "size":
        files.sort(key=lambda item: item["size_bytes"], reverse=reverse)
    else:
        files.sort(key=lambda item: item["modified_at"], reverse=reverse)


async def fred_project_files(
    context: ServerContext, operation: str, **kwargs: Any
) -> dict[str, Any]:
    project_value = kwargs.get("project")
    subdir_value = kwargs.get("subdir")
    sort_field = kwargs.get("sort_by", "name")
    sort_order = kwargs.get("sort_order", "asc")
    limit_value = kwargs.get("limit")
    offset_value = kwargs.get("offset")

    options, error = _common.prepare_output(kwargs)
    if error:
        return error

    if operation != "list":
        return _common.unknown_operation(operation, SUPPORTED_OPERATIONS)

    if project_value is None:
        return _common.missing_parameter("project")

    project_name = str(project_value)
    if not VALID_PROJECT_NAME.fullmatch(project_name):
        return _common.invalid_parameter("project", "letters, numbers, hyphens, or underscores")
    root = context.path_resolver.root
    project_dir = root / project_name
    if not project_dir.exists():
        return _missing_project(project_name)

    target_dir = project_dir
    if subdir_value:
        subdir_text = str(subdir_value)
        if subdir_text not in VALID_SUBDIRS:
            return _invalid_subdir(subdir_text)
        target_dir = project_dir / subdir_text
    elif subdir_value is not None:
        return _invalid_subdir(str(subdir_value))

    if not target_dir.exists():
        return (
            _invalid_subdir(str(subdir_value)) if subdir_value else _missing_project(project_name)
        )

    sort_field = str(sort_field)
    if sort_field not in VALID_SORT_FIELDS:
        return _invalid_sort(sort_field)

    sort_order = str(sort_order).lower()
    if sort_order not in VALID_SORT_ORDERS:
        return _invalid_sort_order(sort_order)

    limit, err = _parse_int(limit_value, "limit")
    if err:
        return err
    offset, err = _parse_int(offset_value, "offset")
    if err:
        return err

    files = _gather_files(project_dir, target_dir)
    total = len(files)
    _sort_files(files, sort_field, sort_order)

    start = offset or 0
    end = start + limit if limit is not None else None
    sliced = files[start:end]

    payload = {
        "project": project_name,
        "subdirectory": str(subdir_value) if subdir_value else None,
        "count": total,
        "offset": start,
        "limit": limit,
        "files": sliced,
    }

    return await _common.success_response(
        context,
        payload,
        operation=operation,
        options=options,
        estimated_rows=len(sliced),
        category="projects",
    )


__all__ = ["fred_project_files"]
