import asyncio
from pathlib import Path

import pytest

from mcp_fred.config import AppConfig, OutputConfig, StorageConfig
from mcp_fred.utils.file_writer import FileWriter
from mcp_fred.utils.job_manager import JobManager
from mcp_fred.utils.json_to_csv import JSONToCSVConverter
from mcp_fred.utils.output_handler import ResultOutputHandler
from mcp_fred.utils.path_resolver import PathResolver
from mcp_fred.utils.token_estimator import TokenEstimator


@pytest.mark.asyncio
async def test_output_handler_screen(tmp_path: Path) -> None:
    config = AppConfig(fred_api_key="test")
    handler = ResultOutputHandler(
        config,
        TokenEstimator(default_safe_limit=50_000),
        JSONToCSVConverter(),
        PathResolver(str(tmp_path)),
        FileWriter(),
        JobManager(),
    )

    payload = {"categories": [{"id": 1, "name": "Root"}]}
    result = await handler.handle(data=payload, operation="get", output="screen")
    assert result["output_mode"] == "screen"
    assert result["data"]["categories"][0]["name"] == "Root"


@pytest.mark.asyncio
async def test_output_handler_file(tmp_path: Path) -> None:
    config = AppConfig(fred_api_key="test", output=OutputConfig(file_chunk_size=2))
    handler = ResultOutputHandler(
        config,
        TokenEstimator(default_safe_limit=10),
        JSONToCSVConverter(),
        PathResolver(str(tmp_path)),
        FileWriter(),
        JobManager(),
    )

    payload = {"categories": [{"id": i, "name": f"Cat {i}"} for i in range(5)]}
    result = await handler.handle(data=payload, operation="categories", output="file", format="csv")
    assert result["output_mode"] == "file"
    path = Path(result["file_path"])
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Cat 0" in content
    assert result["file_size_bytes"] >= len(content)


@pytest.mark.asyncio
async def test_output_handler_maps_csv(tmp_path: Path) -> None:
    config = AppConfig(
        fred_api_key="test",
        storage=StorageConfig(directory=str(tmp_path)),
        output=OutputConfig(file_chunk_size=1),
    )
    job_manager = JobManager()
    handler = ResultOutputHandler(
        config,
        TokenEstimator(default_safe_limit=10),
        JSONToCSVConverter(),
        PathResolver(str(tmp_path)),
        FileWriter(),
        job_manager,
    )

    payload = {
        "shape_values": [
            {"id": "01", "name": "Alabama", "value": 1.0},
            {"id": "02", "name": "Alaska", "value": 2.0},
        ]
    }
    result = await handler.handle(
        data=payload,
        operation="get_shapes",
        output="file",
        format="csv",
        project="geo",
        subdir="maps",
    )
    path = Path(result["file_path"])
    assert path.parent.name == "maps"
    content = path.read_text(encoding="utf-8")
    assert "Alabama" in content
    assert "Alaska" in content


@pytest.mark.asyncio
async def test_output_handler_job_progress(tmp_path: Path) -> None:
    config = AppConfig(
        fred_api_key="test",
        storage=StorageConfig(directory=str(tmp_path)),
        output=OutputConfig(file_chunk_size=1),
    )
    job_manager = JobManager()
    handler = ResultOutputHandler(
        config,
        TokenEstimator(default_safe_limit=10),
        JSONToCSVConverter(),
        PathResolver(str(tmp_path)),
        FileWriter(),
        job_manager,
    )

    job = await job_manager.create_job()
    payload = {
        "series_data": [
            {"date": "2024-01-01", "value": 1},
            {"date": "2024-02-01", "value": 2},
        ]
    }
    result = await handler.handle(
        data=payload,
        operation="get_series_data",
        output="file",
        format="csv",
        project="job-test",
        subdir="maps",
        job_id=job.job_id,
    )
    assert Path(result["file_path"]).exists()
    await asyncio.sleep(0.05)
    stored = await job_manager.get_job(job.job_id)
    assert stored is not None
    assert stored.progress.get("rows_written") == len(payload["series_data"])
    assert stored.progress.get("bytes_written") is not None
    assert stored.progress.get("last_progress_at") is not None
