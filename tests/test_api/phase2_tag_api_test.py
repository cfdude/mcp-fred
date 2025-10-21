import pytest
import respx

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import TagAPI

BASE_URL = "https://api.stlouisfed.org"

TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "tags": [
        {
            "name": "recession",
            "group_id": "macro",
            "notes": "",
            "created": "2024-01-01",
            "popularity": 100,
        }
    ],
}

SERIES_PAYLOAD = {
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

RELATED_TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "related_tags": TAGS_PAYLOAD["tags"],
}


@pytest.mark.asyncio
async def test_tag_api_variants_success() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = TagAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/tags").respond(200, json=TAGS_PAYLOAD)
            tags = await api.list()
            assert tags.tags[0].name == "recession"

            mock.get("/fred/tags/series").respond(200, json=SERIES_PAYLOAD)
            series = await api.list_series("recession")
            assert series.series[0].id == "GDP"

            mock.get("/fred/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
            related_tags = await api.list_related("recession")
            assert related_tags.related_tags[0].name == "recession"


@pytest.mark.asyncio
async def test_tag_api_handles_not_found_and_rate_limit() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = TagAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/tags/series").respond(404, json={})
            with pytest.raises(FREDAPIError) as not_found:
                await api.list_series("missing")
            assert not_found.value.code == "NOT_FOUND"

            mock.get("/fred/tags").respond(429, json={}, headers={"Retry-After": "45"})
            with pytest.raises(FREDAPIError) as rate_limited:
                await api.list()
            assert rate_limited.value.code == "RATE_LIMIT_EXCEEDED"
