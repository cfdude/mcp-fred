import pytest
import respx

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import CategoryAPI

BASE_URL = "https://api.stlouisfed.org"

CATEGORY_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "categories": [
        {"id": 125, "name": "GDP", "parent_id": 0},
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

TAGS_PAYLOAD = {
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

RELATED_TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "related_tags": TAGS_PAYLOAD["tags"],
}


@pytest.mark.asyncio
async def test_category_api_variants_success() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = CategoryAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/category").respond(200, json=CATEGORY_PAYLOAD)
            category = await api.get(125)
            assert category.id == 125

            mock.get("/fred/category/children").respond(200, json=CATEGORY_PAYLOAD)
            children = await api.list_children(125)
            assert children.categories[0].name == "GDP"

            mock.get("/fred/category/related").respond(200, json=CATEGORY_PAYLOAD)
            related = await api.list_related(125)
            assert related.categories[0].id == 125

            mock.get("/fred/category/series").respond(200, json=SERIES_PAYLOAD)
            series = await api.list_series(125)
            assert series.series[0].id == "GDP"

            mock.get("/fred/category/tags").respond(200, json=TAGS_PAYLOAD)
            tags = await api.list_tags(125)
            assert tags.tags[0].name == "gdp"

            mock.get("/fred/category/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
            related_tags = await api.list_related_tags(125, "gdp")
            assert related_tags.related_tags[0].name == "gdp"


@pytest.mark.asyncio
async def test_category_api_handles_not_found_and_rate_limit() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = CategoryAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/category").respond(200, json={**CATEGORY_PAYLOAD, "categories": []})
            with pytest.raises(FREDAPIError) as excinfo:
                await api.get(999)
            assert excinfo.value.code == "NOT_FOUND"

            mock.get("/fred/category/children").respond(
                429,
                json={},
                headers={"Retry-After": "60"},
            )
            with pytest.raises(FREDAPIError) as rate_limit_exc:
                await api.list_children(999)
            assert rate_limit_exc.value.code == "RATE_LIMIT_EXCEEDED"
