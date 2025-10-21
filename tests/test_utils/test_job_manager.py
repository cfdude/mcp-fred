import asyncio
from datetime import timedelta

import pytest

from mcp_fred.utils.background_worker import BackgroundWorker
from mcp_fred.utils.job_manager import JobManager, JobStatus


@pytest.mark.asyncio
async def test_job_manager_lifecycle() -> None:
    manager = JobManager()
    worker = BackgroundWorker(manager)
    await worker.start()

    job = await manager.create_job()

    async def work() -> None:
        await asyncio.sleep(0)
        await manager.complete_job(job.job_id, {"result": "done"})

    await worker.submit(job.job_id, work)
    await asyncio.sleep(0.05)
    stored = await manager.get_job(job.job_id)
    assert stored is not None
    assert stored.status == JobStatus.COMPLETED
    assert stored.result == {"result": "done"}

    await worker.stop()


@pytest.mark.asyncio
async def test_background_worker_retries() -> None:
    manager = JobManager()
    worker = BackgroundWorker(
        manager,
        max_retries=1,
        initial_retry_delay=0.01,
        retry_backoff_factor=1.0,
    )
    await worker.start()

    job = await manager.create_job()
    attempts = {"count": 0}

    async def work() -> None:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("boom")
        await manager.complete_job(job.job_id, {"result": "ok"})

    await worker.submit(job.job_id, work)
    await asyncio.sleep(0.1)
    stored = await manager.get_job(job.job_id)
    assert stored is not None
    assert stored.status == JobStatus.COMPLETED
    assert stored.retry_count == 1

    await worker.stop()


@pytest.mark.asyncio
async def test_background_worker_exceeds_retries() -> None:
    manager = JobManager()
    worker = BackgroundWorker(
        manager,
        max_retries=0,
        initial_retry_delay=0.0,
        retry_backoff_factor=1.0,
    )
    await worker.start()

    job = await manager.create_job()

    async def work() -> None:
        raise RuntimeError("broken")

    await worker.submit(job.job_id, work)
    await asyncio.sleep(0.05)
    stored = await manager.get_job(job.job_id)
    assert stored is not None
    assert stored.status == JobStatus.FAILED
    assert stored.error is not None

    await worker.stop()


@pytest.mark.asyncio
async def test_job_manager_purge_expired() -> None:
    manager = JobManager()
    job = await manager.create_job()
    job.created_at -= timedelta(hours=25)
    job.updated_at = job.created_at
    removed = await manager.purge_expired(timedelta(hours=24))
    assert removed == 1
    assert await manager.get_job(job.job_id) is None


@pytest.mark.asyncio
async def test_background_worker_skips_cancelled_job_before_execution() -> None:
    manager = JobManager()
    worker = BackgroundWorker(manager)
    await worker.start()

    job = await manager.create_job()
    executed = False

    async def work() -> None:
        nonlocal executed
        executed = True

    # Simulate a cancellation request landing before the worker can process the job.
    cancelled = await manager.cancel_job(job.job_id, reason="no longer needed")
    assert cancelled is True

    await worker.submit(job.job_id, work)
    await asyncio.sleep(0.05)

    stored = await manager.get_job(job.job_id)
    assert stored is not None
    assert stored.status == JobStatus.CANCELLED
    assert not executed

    await worker.stop()


@pytest.mark.asyncio
async def test_background_worker_autostart() -> None:
    manager = JobManager()
    worker = BackgroundWorker(manager)

    job = await manager.create_job()

    async def work() -> None:
        await manager.complete_job(job.job_id, {"result": "done"})

    await worker.submit(job.job_id, work)
    await asyncio.sleep(0.05)
    stored = await manager.get_job(job.job_id)
    assert stored is not None
    assert stored.status == JobStatus.COMPLETED

    await worker.stop()


@pytest.mark.asyncio
async def test_job_manager_auto_purge_on_access() -> None:
    manager = JobManager(retention_hours=1)
    job = await manager.create_job()
    job.created_at -= timedelta(hours=2)
    job.updated_at = job.created_at

    assert await manager.get_job(job.job_id) is None
