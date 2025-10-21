import httpx
import pytest
import respx
from httpx import Response

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig

BASE_URL = "https://api.stlouisfed.org"


@pytest.mark.asyncio
async def test_client_get_success() -> None:
    config = FREDClientConfig(api_key="test-key")
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            mock.get("/fred/category").respond(
                200,
                json={
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "categories": [],
                },
            )
            result = await client.get("/fred/category", params={"category_id": 0})
            assert result["realtime_start"] == "2024-01-01"


@pytest.mark.asyncio
async def test_client_maps_http_errors() -> None:
    config = FREDClientConfig(api_key="test-key")
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            mock.get("/fred/category").respond(404, json={})
            with pytest.raises(FREDAPIError) as excinfo:
                await client.get("/fred/category", params={"category_id": 999})
            assert excinfo.value.code == "NOT_FOUND"


@pytest.mark.asyncio
async def test_client_retries_on_rate_limit() -> None:
    config = FREDClientConfig(api_key="test-key", max_retries=1)
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            route = mock.get("/fred/series").mock(
                side_effect=[
                    Response(429, json={"error_code": "RATE_LIMIT"}),
                    Response(
                        200,
                        json={
                            "seriess": [],
                            "realtime_start": "2024-01-01",
                            "realtime_end": "2024-01-01",
                        },
                    ),
                ]
            )
            result = await client.get("/fred/series", params={"series_id": "GDP"})
            assert result["seriess"] == []
            assert route.call_count == 2


@pytest.mark.asyncio
async def test_client_timeout_error() -> None:
    config = FREDClientConfig(api_key="test-key", max_retries=0)
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            mock.get("/fred/series").mock(side_effect=httpx.TimeoutException("timeout"))
            with pytest.raises(FREDAPIError) as excinfo:
                await client.get("/fred/series", params={"series_id": "GDP"})
            assert excinfo.value.code == "TIMEOUT"


@pytest.mark.asyncio
async def test_client_network_error() -> None:
    config = FREDClientConfig(api_key="test-key", max_retries=0)
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            mock.get("/fred/series").mock(side_effect=httpx.NetworkError("down"))
            with pytest.raises(FREDAPIError) as excinfo:
                await client.get("/fred/series", params={"series_id": "GDP"})
            assert excinfo.value.code == "NETWORK_ERROR"


@pytest.mark.asyncio
async def test_client_unexpected_status_maps_http_error() -> None:
    config = FREDClientConfig(api_key="test-key")
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            mock.get("/fred/series").respond(418, json={})
            with pytest.raises(FREDAPIError) as excinfo:
                await client.get("/fred/series", params={"series_id": "GDP"})
            assert excinfo.value.code == "HTTP_ERROR"


@pytest.mark.asyncio
async def test_compute_retry_delay() -> None:
    config = FREDClientConfig(api_key="test-key")
    client = FREDClient(config)
    delay = client._compute_retry_delay(2)
    assert delay > 0
    await client.aclose()


@pytest.mark.asyncio
async def test_client_injects_api_key() -> None:
    config = FREDClientConfig(api_key="inspect-key")
    async with FREDClient(config) as client:
        with respx.mock(base_url=config.normalised_base_url) as mock:
            route = mock.get("/fred/series").respond(
                200,
                json={"seriess": [], "realtime_start": "2024-01-01", "realtime_end": "2024-01-01"},
            )
            await client.get("/fred/series", params={"series_id": "GDP"})
            request = route.calls[0].request
            assert request.url.params["api_key"] == "inspect-key"
            assert request.url.params["series_id"] == "GDP"
