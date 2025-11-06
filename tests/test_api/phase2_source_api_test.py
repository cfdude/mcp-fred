import pytest
import respx

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import SourceAPI

BASE_URL = "https://api.stlouisfed.org"

SOURCES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "sources": [
        {
            "id": 99,
            "realtime_start": "2024-01-01",
            "realtime_end": "2024-01-01",
            "name": "Board of Governors",
            "link": "https://example.com",
        }
    ],
}

SOURCE_RELEASES_PAYLOAD = {
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
            "name": "GDP Release",
            "press_release": 0,
            "link": "https://example.com",
            "notes": "",
        }
    ],
}


@pytest.mark.asyncio
async def test_source_api_variants_success() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SourceAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/sources").respond(200, json=SOURCES_PAYLOAD)
            sources = await api.list()
            assert sources.sources[0].id == 99

            mock.get("/fred/source").respond(200, json=SOURCES_PAYLOAD)
            source = await api.get(99)
            assert source.name == "Board of Governors"

            mock.get("/fred/source/releases").respond(200, json=SOURCE_RELEASES_PAYLOAD)
            releases = await api.list_releases(99)
            assert releases.releases[0].id == 1


@pytest.mark.asyncio
async def test_source_api_handles_not_found_and_rate_limit() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SourceAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/source").respond(200, json={**SOURCES_PAYLOAD, "sources": []})
            with pytest.raises(FREDAPIError) as not_found:
                await api.get(1)
            assert not_found.value.code == "NOT_FOUND"

            mock.get("/fred/sources").respond(429, json={}, headers={"Retry-After": "15"})
            with pytest.raises(FREDAPIError) as rate_limited:
                await api.list()
            assert rate_limited.value.code == "RATE_LIMIT_EXCEEDED"
