import pytest
import respx
from httpx import Response

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import CategoryAPI, ReleaseAPI, SourceAPI, TagAPI

BASE_URL = "https://api.stlouisfed.org"


@pytest.mark.asyncio
async def test_category_api_get_success_and_tags() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = CategoryAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/category").respond(
                200,
                json={
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "categories": [{"id": 125, "name": "GDP", "parent_id": 0}],
                },
            )
            category = await api.get(125)
            assert category.id == 125

            mock.get("/fred/category/tags").respond(
                200,
                json={
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
                },
            )
            tags = await api.list_tags(125)
            assert tags.tags[0].name == "gdp"


@pytest.mark.asyncio
async def test_category_api_get_not_found() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = CategoryAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/category").respond(
                200,
                json={
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "categories": [],
                },
            )
            with pytest.raises(FREDAPIError):
                await api.get(999)


@pytest.mark.asyncio
async def test_release_api_related_tags() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = ReleaseAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/release/tags").respond(
                200,
                json={
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "count": 1,
                    "offset": 0,
                    "limit": 1000,
                    "tags": [
                        {
                            "name": "employment",
                            "group_id": "macro",
                            "created": "2024-01-01",
                            "notes": "",
                            "popularity": 90,
                        }
                    ],
                },
            )
            tags = await api.list_tags(1)
            assert tags.tags[0].name == "employment"

            mock.get("/fred/release").respond(404, json={})
            with pytest.raises(FREDAPIError):
                await api.get(42)


@pytest.mark.asyncio
async def test_source_api_list_and_error() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = SourceAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/sources").respond(
                200,
                json={
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "count": 1,
                    "offset": 0,
                    "limit": 1000,
                    "sources": [
                        {
                            "id": 10,
                            "realtime_start": "2024-01-01",
                            "realtime_end": "2024-01-01",
                            "name": "Sample",
                            "link": "https://example.com",
                        }
                    ],
                },
            )
            response = await api.list()
            assert response.sources[0].name == "Sample"

            mock.get("/fred/source").mock(return_value=Response(404, json={}))
            with pytest.raises(FREDAPIError) as excinfo:
                await api.get(999)
            assert excinfo.value.code == "NOT_FOUND"


@pytest.mark.asyncio
async def test_tag_api_variants() -> None:
    config = FREDClientConfig(api_key="test")
    async with FREDClient(config) as client:
        api = TagAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/tags").respond(
                200,
                json={
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
                },
            )
            tags = await api.list()
            assert tags.tags[0].name == "recession"

            mock.get("/fred/tags/series").respond(
                200,
                json={
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
                },
            )
            series = await api.list_series("recession")
            assert series.series[0].id == "GDP"
