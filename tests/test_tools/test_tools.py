import asyncio
import json
import os
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

import pytest
import respx

from mcp_fred.api.models.responses import SeriesObservationsResponse
from mcp_fred.tools.category import fred_category
from mcp_fred.tools.job_cancel import fred_job_cancel
from mcp_fred.tools.job_list import fred_job_list
from mcp_fred.tools.job_status import fred_job_status
from mcp_fred.tools.maps import fred_maps
from mcp_fred.tools.project_create import fred_project_create
from mcp_fred.tools.project_list import fred_project_list
from mcp_fred.tools.release import fred_release
from mcp_fred.tools.series import fred_series
from mcp_fred.tools.source import fred_source
from mcp_fred.tools.tag import fred_tag
from mcp_fred.utils.job_manager import JobStatus

BASE_URL = "https://api.stlouisfed.org"
FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "maps"

CATEGORY_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "categories": [
        {"id": 0, "name": "Root", "parent_id": -1},
    ],
}

SERIES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 0,
    "offset": 0,
    "limit": 1000,
    "seriess": [],
}

SERIES_SINGLE_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "seriess": [
        {
            "id": "GDP",
            "title": "Gross Domestic Product",
            "observation_start": "1947-01-01",
            "observation_end": "2024-01-01",
        }
    ],
}

SERIES_OBSERVATIONS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 2,
    "offset": 0,
    "limit": 1000,
    "observations": [
        {"date": "2024-01-01", "value": "1.0"},
        {"date": "2024-02-01", "value": "2.0"},
    ],
}

RELEASE_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "releases": [
        {
            "id": 1,
            "realtime_start": "2024-01-01",
            "realtime_end": "2024-01-01",
            "name": "Example",
            "press_release": 0,
            "link": "https://example.com",
            "notes": "",
        }
    ],
}

RELEASE_TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "tags": [
        {
            "name": "gdp",
            "group_id": "macro",
            "notes": "",
            "created": "2024-01-01",
            "popularity": 100,
        }
    ],
}

RELEASE_TABLES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 0,
    "offset": 0,
    "limit": 1000,
    "release_tables": [],
}

SOURCES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "sources": [
        {
            "id": 1,
            "realtime_start": "2024-01-01",
            "realtime_end": "2024-01-01",
            "name": "Board of Governors",
            "link": "https://federalreserve.gov",
        }
    ],
}

RELATED_TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "related_tags": RELEASE_TAGS_PAYLOAD["tags"],
}

RELEASE_SINGLE_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "release": RELEASE_PAYLOAD["releases"][0],
}

RELEASE_DATES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "release_dates": [{"date": "2024-01-01"}],
}

SOURCE_RELEASES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "releases": RELEASE_PAYLOAD["releases"],
}

TAG_SERIES_PAYLOAD = SERIES_PAYLOAD

SERIES_UPDATES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "seriess": SERIES_SINGLE_PAYLOAD["seriess"],
}

VINTAGE_DATES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 2,
    "offset": 0,
    "limit": 1000,
    "vintage_dates": ["2024-01-01", "2024-02-01"],
}

MAP_SHAPES_PAYLOAD = json.loads((FIXTURES_DIR / "shape_values.json").read_text(encoding="utf-8"))
MAP_SERIES_GROUP_PAYLOAD = json.loads(
    (FIXTURES_DIR / "series_group.json").read_text(encoding="utf-8")
)
MAP_REGIONAL_DATA_PAYLOAD = json.loads(
    (FIXTURES_DIR / "regional_data.json").read_text(encoding="utf-8")
)
MAP_SERIES_DATA_PAYLOAD = json.loads(
    (FIXTURES_DIR / "series_data.json").read_text(encoding="utf-8")
)


@pytest.mark.asyncio
async def test_fred_category_get(server_context):
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as mock:
        mock.get("/fred/category").respond(200, json=CATEGORY_PAYLOAD)
        result = await fred_category(server_context, "get", category_id=0)
        assert result["status"] == "success"
        assert result["data"]["name"] == "Root"


@pytest.mark.asyncio
async def test_fred_category_unsupported_output(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/category").respond(200, json=CATEGORY_PAYLOAD)
        response = await fred_category(
            server_context,
            "get",
            category_id=0,
            output="file",
            format="csv",
        )
        assert response["output_mode"] == "file"


@pytest.mark.asyncio
async def test_fred_category_get_series(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/category/series").respond(200, json=SERIES_PAYLOAD)
        response = await fred_category(server_context, "get_series", category_id=0)
        assert response["data"]["seriess"] == []


@pytest.mark.asyncio
async def test_fred_category_additional_lists(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/category/children").respond(200, json=CATEGORY_PAYLOAD)
        mock.get("/fred/category/related").respond(200, json=CATEGORY_PAYLOAD)
        mock.get("/fred/category/tags").respond(200, json=RELEASE_TAGS_PAYLOAD)
        mock.get("/fred/category/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
        children = await fred_category(server_context, "list_children", category_id=0)
        related = await fred_category(server_context, "list_related", category_id=0)
        tags = await fred_category(server_context, "get_tags", category_id=0)
        related_tags = await fred_category(
            server_context,
            "get_related_tags",
            category_id=0,
            tag_names="gdp",
        )
        assert children["data"]["categories"][0]["name"] == "Root"
        assert related["data"]["categories"][0]["name"] == "Root"
        assert tags["data"]["tags"][0]["name"] == "gdp"
        assert related_tags["data"]["related_tags"][0]["name"] == "gdp"


@pytest.mark.asyncio
async def test_fred_category_invalid_category_id(server_context):
    response = await fred_category(server_context, "get", category_id="abc")
    assert response["error"]["code"] == "INVALID_PARAMETER"


@pytest.mark.asyncio
async def test_fred_category_api_error(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/category").respond(404, json={})
        response = await fred_category(server_context, "get", category_id=0)
        assert response["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_fred_release_list(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/releases").respond(200, json=RELEASE_PAYLOAD)
        response = await fred_release(server_context, "list")
        assert response["data"]["releases"][0]["name"] == "Example"


@pytest.mark.asyncio
async def test_fred_release_get_tags(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/release/tags").respond(200, json=RELEASE_TAGS_PAYLOAD)
        response = await fred_release(server_context, "get_tags", release_id=1)
        assert response["data"]["tags"][0]["name"] == "gdp"
        mock.get("/fred/release/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
        related = await fred_release(
            server_context, "get_related_tags", release_id=1, tag_names="gdp"
        )
        assert related["data"]["related_tags"][0]["name"] == "gdp"


@pytest.mark.asyncio
async def test_fred_release_get_details(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/release").respond(200, json=RELEASE_SINGLE_PAYLOAD)
        mock.get("/fred/release/dates").respond(200, json=RELEASE_DATES_PAYLOAD)
        mock.get("/fred/release/series").respond(200, json=SERIES_PAYLOAD)
        mock.get("/fred/release/sources").respond(200, json=SOURCES_PAYLOAD)
        mock.get("/fred/release/tables").respond(200, json=RELEASE_TABLES_PAYLOAD)
        single = await fred_release(server_context, "get", release_id=1)
        dates = await fred_release(server_context, "get_dates", release_id=1)
        series = await fred_release(server_context, "get_series", release_id=1)
        sources = await fred_release(server_context, "get_sources", release_id=1)
        tables = await fred_release(server_context, "get_tables", release_id=1)
        assert single["data"]["name"] == "Example"
        assert str(dates["data"]["release_dates"][0]["date"]) == "2024-01-01"
        assert series["data"]["seriess"] == []
        assert sources["data"]["sources"][0]["name"] == "Board of Governors"
        assert tables["data"]["release_tables"] == []


@pytest.mark.asyncio
async def test_fred_release_missing_release_id(server_context):
    response = await fred_release(server_context, "get")
    assert response["error"]["code"] == "MISSING_PARAMETER"


@pytest.mark.asyncio
async def test_fred_release_api_error(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/releases").respond(429, json={}, headers={"Retry-After": "60"})
        response = await fred_release(server_context, "list")
        assert response["error"]["code"] == "RATE_LIMIT_EXCEEDED"


@pytest.mark.asyncio
async def test_fred_source_get(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/source").respond(200, json=SOURCES_PAYLOAD)
        response = await fred_source(server_context, "get", source_id=1)
        assert response["data"]["id"] == 1


@pytest.mark.asyncio
async def test_fred_source_get_releases(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/source/releases").respond(200, json=SOURCE_RELEASES_PAYLOAD)
        response = await fred_source(server_context, "get_releases", source_id=1)
        assert response["data"]["releases"][0]["name"] == "Example"


@pytest.mark.asyncio
async def test_fred_source_invalid_source_id(server_context):
    response = await fred_source(server_context, "get", source_id="abc")
    assert response["error"]["code"] == "INVALID_PARAMETER"


@pytest.mark.asyncio
async def test_fred_source_api_error(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/source").respond(404, json={})
        response = await fred_source(server_context, "get", source_id=1)
        assert response["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_fred_tag_get_related(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
        response = await fred_tag(server_context, "get_related", tag_names="gdp")
        assert response["data"]["related_tags"][0]["name"] == "gdp"


@pytest.mark.asyncio
async def test_fred_tag_list_series(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/tags/series").respond(200, json=TAG_SERIES_PAYLOAD)
        response = await fred_tag(server_context, "get_series", tag_names="gdp")
        assert response["data"]["seriess"] == []


@pytest.mark.asyncio
async def test_fred_tag_missing_tag_names(server_context):
    response = await fred_tag(server_context, "get_series")
    assert response["error"]["code"] == "MISSING_PARAMETER"


@pytest.mark.asyncio
async def test_fred_tag_unknown_operation(server_context):
    response = await fred_tag(server_context, "unknown")
    assert response["error"]["code"] == "INVALID_OPERATION"


@pytest.mark.asyncio
async def test_fred_tag_api_error(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/tags").respond(429, json={}, headers={"Retry-After": "30"})
        response = await fred_tag(server_context, "list")
        assert response["error"]["code"] == "RATE_LIMIT_EXCEEDED"


@pytest.mark.asyncio
async def test_fred_job_status_success(server_context):
    job = await server_context.job_manager.create_job()
    response = await fred_job_status(server_context, "get", job_id=job.job_id)
    assert response["status"] == "success"
    assert response["data"]["job_id"] == job.job_id
    assert response["data"]["status"] == job.status.value


@pytest.mark.asyncio
async def test_fred_job_status_missing_job_id(server_context):
    response = await fred_job_status(server_context, "get")
    assert response["error"]["code"] == "MISSING_PARAMETER"


@pytest.mark.asyncio
async def test_fred_job_status_not_found(server_context):
    response = await fred_job_status(server_context, "get", job_id="unknown")
    assert response["error"]["code"] == "JOB_NOT_FOUND"


@pytest.mark.asyncio
async def test_fred_job_list_filtering(server_context):
    job1 = await server_context.job_manager.create_job()
    job2 = await server_context.job_manager.create_job()
    await server_context.job_manager.complete_job(job2.job_id, {"result": "done"})

    all_jobs = await fred_job_list(server_context, "list")
    assert all_jobs["status"] == "success"
    assert len(all_jobs["data"]["jobs"]) == 2
    assert any(job["job_id"] == job1.job_id for job in all_jobs["data"]["jobs"])

    response = await fred_job_list(server_context, "list", status="completed")
    assert response["status"] == "success"
    jobs = response["data"]["jobs"]
    assert len(jobs) == 1
    assert jobs[0]["job_id"] == job2.job_id


@pytest.mark.asyncio
async def test_fred_job_list_invalid_status(server_context):
    response = await fred_job_list(server_context, "list", status="invalid")
    assert response["error"]["code"] == "INVALID_STATUS_FILTER"


@pytest.mark.asyncio
async def test_fred_job_cancel_success(server_context):
    job = await server_context.job_manager.create_job()
    response = await fred_job_cancel(server_context, "cancel", job_id=job.job_id)
    assert response["status"] == "success"
    stored = await server_context.job_manager.get_job(job.job_id)
    assert stored is not None and stored.status.value == "cancelled"


@pytest.mark.asyncio
async def test_fred_job_cancel_missing_id(server_context):
    result = await fred_job_cancel(server_context, "cancel")
    assert result["error"]["code"] == "MISSING_PARAMETER"


@pytest.mark.asyncio
async def test_fred_job_cancel_not_found(server_context):
    result = await fred_job_cancel(server_context, "cancel", job_id="does-not-exist")
    assert result["error"]["code"] == "JOB_NOT_FOUND"


@pytest.mark.asyncio
async def test_fred_project_list(server_context, tmp_path):
    root = server_context.path_resolver.root
    project_dir = root / "project-list-demo"
    (project_dir / "series").mkdir(parents=True, exist_ok=True)
    (project_dir / "series" / "data.csv").write_text("date,value\n", encoding="utf-8")

    response = await fred_project_list(server_context, "list")
    assert response["status"] == "success"
    projects = response["data"]["projects"]
    assert any(project["project"] == "project-list-demo" for project in projects)

    shutil.rmtree(project_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_fred_project_list_metadata(server_context):
    root = server_context.path_resolver.root
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True, exist_ok=True)

    project_name = "metadata-project"
    project_dir = root / project_name
    series_dir = project_dir / "series"
    series_dir.mkdir(parents=True, exist_ok=True)
    file_a = series_dir / "a.csv"
    file_b = series_dir / "b.csv"
    file_a.write_text("date,value\n2024-01-01,1\n", encoding="utf-8")
    file_b.write_text("date,value\n2024-01-02,2\n", encoding="utf-8")

    now = time.time()
    os.utime(file_a, (now - 3600, now - 3600))
    os.utime(file_b, (now, now))

    response = await fred_project_list(server_context, "list")
    assert response["status"] == "success"
    projects = response["data"]["projects"]
    matching = next(project for project in projects if project["project"] == project_name)
    assert matching["file_count"] == 2
    expected_size = file_a.stat().st_size + file_b.stat().st_size
    assert matching["total_size_bytes"] == expected_size
    latest = datetime.fromisoformat(matching["latest_modified"])
    expected_latest = datetime.fromtimestamp(now, tz=UTC)
    assert abs((latest - expected_latest).total_seconds()) < 2

    shutil.rmtree(project_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_fred_project_list_missing_root(server_context):
    root = server_context.path_resolver.root
    shutil.rmtree(root, ignore_errors=True)

    response = await fred_project_list(server_context, "list")
    assert response["error"]["code"] == "STORAGE_NOT_AVAILABLE"

    root.mkdir(parents=True, exist_ok=True)


@pytest.mark.asyncio
async def test_fred_project_create_success(server_context):
    project_name = "project-create-demo"
    root = server_context.path_resolver.root
    project_dir = root / project_name
    shutil.rmtree(project_dir, ignore_errors=True)

    response = await fred_project_create(server_context, "create", project=project_name)
    assert response["status"] == "success"
    expected_subdirs = ["series", "maps", "releases", "categories", "sources", "tags"]
    for subdir in expected_subdirs:
        assert (project_dir / subdir).exists()
    metadata_path = project_dir / ".project.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["project"] == project_name
    assert "created_at" in metadata
    assert metadata["subdirectories"] == expected_subdirs

    shutil.rmtree(project_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_fred_project_create_invalid_name(server_context):
    response = await fred_project_create(server_context, "create", project="bad name")
    assert response["error"]["code"] == "INVALID_PROJECT_NAME"


@pytest.mark.asyncio
async def test_fred_project_create_duplicate(server_context):
    project_name = "duplicate-project"
    root = server_context.path_resolver.root
    project_dir = root / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    response = await fred_project_create(server_context, "create", project=project_name)
    assert response["error"]["code"] == "PROJECT_EXISTS"

    shutil.rmtree(project_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_fred_series_get(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series").respond(200, json=SERIES_SINGLE_PAYLOAD)
        result = await fred_series(server_context, "get", series_id="GDP")
        assert result["status"] == "success"
        assert result["data"]["seriess"][0]["id"] == "GDP"


@pytest.mark.asyncio
async def test_fred_series_observations(server_context):
    preview_payload = {
        **SERIES_OBSERVATIONS_PAYLOAD,
        "observations": [SERIES_OBSERVATIONS_PAYLOAD["observations"][0]],
    }
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series/observations", params={"series_id": "GDP", "limit": "1"}).respond(
            200, json=preview_payload
        )
        mock.get("/fred/series/observations", params={"series_id": "GDP"}).respond(
            200, json=SERIES_OBSERVATIONS_PAYLOAD
        )
        response = await fred_series(server_context, "get_observations", series_id="GDP")
        assert response["data"]["observations"][0]["value"] == "1.0"


@pytest.mark.asyncio
async def test_fred_series_observations_triggers_job(server_context, monkeypatch):
    original_threshold = server_context.config.output.job_row_threshold
    server_context.config.output.job_row_threshold = 1

    async def noop_start() -> None:
        return None

    async def immediate_submit(job_id, factory):
        await server_context.job_manager.start_job(job_id)
        await factory()

    monkeypatch.setattr(server_context.background_worker, "start", noop_start)
    monkeypatch.setattr(server_context.background_worker, "submit", immediate_submit)

    preview_payload = {
        **SERIES_OBSERVATIONS_PAYLOAD,
        "observations": [SERIES_OBSERVATIONS_PAYLOAD["observations"][0]],
    }
    large_payload = {**SERIES_OBSERVATIONS_PAYLOAD, "count": 20000}

    with respx.mock(base_url=BASE_URL) as mock:
        mock.get(
            "/fred/series/observations",
            params={"series_id": "GDP", "limit": "1"},
        ).respond(200, json=preview_payload)
        mock.get("/fred/series/observations").respond(200, json=large_payload)
        response = await fred_series(
            server_context,
            "get_observations",
            series_id="GDP",
            limit=20000,
            project="jobtest",
        )

    try:
        assert response["status"] == "accepted"
        job = await server_context.job_manager.get_job(response["job_id"])
        assert job is not None
        assert job.error is None, job.error
        assert job.status.value == "completed"
        assert job.retry_count == 0
        assert job.progress.get("estimated_total") == 20000
        assert job.result is not None
        file_path = job.result.get("file_path")
        if file_path:
            output_path = Path(file_path)
            if output_path.exists():
                output_path.unlink()
                try:
                    parent = output_path.parent
                    parent.rmdir()
                    if parent.parent != parent:
                        parent.parent.rmdir()
                except OSError:
                    pass
    finally:
        server_context.config.output.job_row_threshold = original_threshold
        await server_context.background_worker.stop()


@pytest.mark.asyncio
async def test_fred_series_job_retries_before_completion(server_context, monkeypatch):
    original_threshold = server_context.config.output.job_row_threshold
    server_context.config.output.job_row_threshold = 1
    attempts = {"count": 0}
    original_submit = server_context.background_worker.submit

    async def flaky_submit(job_id: str, coro_factory):
        async def wrapped() -> None:
            if attempts["count"] == 0:
                attempts["count"] += 1
                raise RuntimeError("transient failure")
            await coro_factory()

        await original_submit(job_id, wrapped)

    monkeypatch.setattr(server_context.background_worker, "submit", flaky_submit)

    async def fake_get_series_observations(series_id: str, params: dict | None = None):
        limit_value = None
        if params is not None:
            limit_value = params.get("limit")
        if limit_value in (1, "1", 1.0):
            payload = {
                **SERIES_OBSERVATIONS_PAYLOAD,
                "count": 20000,
                "observations": [SERIES_OBSERVATIONS_PAYLOAD["observations"][0]],
            }
            return SeriesObservationsResponse.model_validate(payload)
        return SeriesObservationsResponse.model_validate(
            {**SERIES_OBSERVATIONS_PAYLOAD, "count": 20000}
        )

    monkeypatch.setattr(
        server_context.series,
        "get_series_observations",
        fake_get_series_observations,
    )

    response = await fred_series(
        server_context,
        "get_observations",
        series_id="GDP",
        limit=20000,
        project="retrytest",
    )

    try:
        assert response["status"] == "accepted"
        job_id = response["job_id"]
        job = await server_context.job_manager.get_job(job_id)
        assert job is not None
        # Wait for the background worker to process retries and finish.
        for _ in range(60):
            if job.status in (JobStatus.COMPLETED, JobStatus.FAILED):
                break
            await asyncio.sleep(0.05)
            job = await server_context.job_manager.get_job(job_id)
            assert job is not None
        assert job.status == JobStatus.COMPLETED, job.error
        assert job.retry_count == 1
        assert attempts["count"] == 1
        assert job.result is not None
        file_path = job.result.get("file_path")
        if file_path:
            output_path = Path(file_path)
            if output_path.exists():
                output_path.unlink()
                try:
                    parent = output_path.parent
                    parent.rmdir()
                    if parent.parent != parent:
                        parent.parent.rmdir()
                except OSError:
                    pass
    finally:
        server_context.config.output.job_row_threshold = original_threshold


@pytest.mark.asyncio
async def test_fred_series_updates_and_vintages(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series/updates").respond(200, json=SERIES_UPDATES_PAYLOAD)
        mock.get("/fred/series/vintagedates").respond(200, json=VINTAGE_DATES_PAYLOAD)
        updates = await fred_series(server_context, "get_updates")
        vintages = await fred_series(server_context, "get_vintage_dates", series_id="GDP")
        assert updates["data"]["seriess"][0]["id"] == "GDP"
        assert vintages["data"]["vintage_dates"][1] == "2024-02-01"


@pytest.mark.asyncio
async def test_fred_series_categories_and_tags(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series/categories").respond(200, json=CATEGORY_PAYLOAD)
        mock.get("/fred/series/tags").respond(200, json=RELEASE_TAGS_PAYLOAD)
        categories = await fred_series(server_context, "get_categories", series_id="GDP")
        tags = await fred_series(server_context, "get_tags", series_id="GDP")
        assert categories["data"]["categories"][0]["name"] == "Root"
        assert tags["data"]["tags"][0]["name"] == "gdp"


@pytest.mark.asyncio
async def test_fred_series_search_variants(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series/search").respond(200, json=SERIES_SINGLE_PAYLOAD)
        mock.get("/fred/series/search/tags").respond(200, json=RELEASE_TAGS_PAYLOAD)
        mock.get("/fred/series/search/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
        series = await fred_series(server_context, "search", search_text="gdp")
        tags = await fred_series(server_context, "search_tags", series_search_text="gdp")
        related = await fred_series(server_context, "search_related_tags", series_search_text="gdp")
        assert series["data"]["seriess"][0]["id"] == "GDP"
        assert tags["data"]["tags"][0]["name"] == "gdp"
        assert related["data"]["related_tags"][0]["name"] == "gdp"


@pytest.mark.asyncio
async def test_fred_series_missing_series_id(server_context):
    response = await fred_series(server_context, "get")
    assert response["error"]["code"] == "MISSING_PARAMETER"


@pytest.mark.asyncio
async def test_fred_series_unknown_operation(server_context):
    response = await fred_series(server_context, "unknown")
    assert response["error"]["code"] == "INVALID_OPERATION"


@pytest.mark.asyncio
async def test_fred_maps_shapes_triggers_job(server_context, monkeypatch):
    async def noop_start() -> None:
        return None

    async def immediate_submit(job_id, factory):
        await server_context.job_manager.start_job(job_id)
        await factory()

    monkeypatch.setattr(server_context.background_worker, "start", noop_start)
    monkeypatch.setattr(server_context.background_worker, "submit", immediate_submit)

    with respx.mock(base_url=BASE_URL, assert_all_called=False) as mock:
        mock.get("/geofred/shapes/file").respond(200, json=MAP_SHAPES_PAYLOAD)
        response = await fred_maps(server_context, "get_shapes", shape="state", project="maptest")

    assert response["status"] == "accepted"
    job = await server_context.job_manager.get_job(response["job_id"])
    assert job is not None
    assert job.error is None, job.error
    assert job.status.value == "completed"
    assert job.progress.get("bytes_written") is not None
    file_path = job.result.get("file_path") if job.result else None
    if file_path:
        output_path = Path(file_path)
        if output_path.exists():
            output_path.unlink()
            try:
                parent = output_path.parent
                parent.rmdir()
                if parent.parent != parent:
                    parent.parent.rmdir()
            except OSError:
                pass


@pytest.mark.asyncio
async def test_fred_maps_job_cancellation_before_execution(server_context, monkeypatch):
    captured = {}

    async def capture_submit(job_id: str, coro_factory):
        captured["job_id"] = job_id
        captured["coro_factory"] = coro_factory
        return None

    monkeypatch.setattr(server_context.background_worker, "submit", capture_submit)

    response = await fred_maps(
        server_context,
        "get_shapes",
        shape="state",
        project="canceltest",
        output="file",
    )

    assert response["status"] == "accepted"
    job_id = response["job_id"]
    assert captured.get("job_id") == job_id
    cancelled = await server_context.job_manager.cancel_job(job_id, reason="test cancel")
    assert cancelled is True
    job = await server_context.job_manager.get_job(job_id)
    assert job is not None
    assert job.status == JobStatus.CANCELLED
    assert job.error is not None and job.error["code"] == "JOB_CANCELLED"
    assert job.result is None
    await server_context.background_worker.stop()


@pytest.mark.asyncio
async def test_fred_maps_series_group(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/geofred/series/group").respond(200, json=MAP_SERIES_GROUP_PAYLOAD)
        response = await fred_maps(server_context, "get_series_group", series_id="SMU")
        assert response["data"]["seriess"][0]["series_id"].startswith("SMU")


@pytest.mark.asyncio
async def test_fred_maps_regional_and_series_data(server_context):
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/geofred/regional/data").respond(200, json=MAP_REGIONAL_DATA_PAYLOAD)
        mock.get("/geofred/series/data").respond(200, json=MAP_SERIES_DATA_PAYLOAD)
        regional = await fred_maps(server_context, "get_regional_data", output="screen")
        series = await fred_maps(
            server_context, "get_series_data", series_id="SMU", output="screen"
        )
        assert regional["data"]["regional_data"][0]["region"] == "04000"
        assert series["data"]["series_data"][0]["value"] == 15234.0


@pytest.mark.asyncio
async def test_fred_maps_series_data_job(server_context, monkeypatch):
    async def noop_start() -> None:
        return None

    async def immediate_submit(job_id, factory):
        await server_context.job_manager.start_job(job_id)
        await factory()

    monkeypatch.setattr(server_context.background_worker, "start", noop_start)
    monkeypatch.setattr(server_context.background_worker, "submit", immediate_submit)

    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/geofred/series/data", params={"series_id": "SMU"}).respond(
            200, json=MAP_SERIES_DATA_PAYLOAD
        )
        response = await fred_maps(
            server_context, "get_series_data", series_id="SMU", project="maptest2"
        )

    assert response["status"] == "accepted"
    job = await server_context.job_manager.get_job(response["job_id"])
    assert job is not None
    assert job.error is None, job.error
    assert job.status.value == "completed"
    assert job.progress.get("bytes_written") is not None
    file_path = job.result.get("file_path") if job.result else None
    if file_path:
        output_path = Path(file_path)
        if output_path.exists():
            output_path.unlink()
            try:
                parent = output_path.parent
                parent.rmdir()
                if parent.parent != parent:
                    parent.parent.rmdir()
            except OSError:
                pass


@pytest.mark.asyncio
async def test_fred_maps_invalid_operation(server_context):
    response = await fred_maps(server_context, "unknown")
    assert response["error"]["code"] == "INVALID_OPERATION"
