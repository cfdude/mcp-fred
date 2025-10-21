import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mcp_fred.server import ServerContext, build_server_context  # noqa: E402


@pytest.fixture
async def server_context() -> ServerContext:
    context = build_server_context(fred_api_key="test-key")
    try:
        yield context
    finally:
        await context.background_worker.stop()
        await context.aclose()
