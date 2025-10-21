import pytest
import respx

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import CategoryAPI, MapsAPI, ReleaseAPI, SeriesAPI, SourceAPI, TagAPI

BASE_URL = "https://api.stlouisfed.org"

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

RELEASE_TABLES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 0,
    "offset": 0,
    "limit": 1000,
    "release_tables": [],
}

MAP_SHAPES_PAYLOAD = {
    "shape_values": [
        {"id": "01", "name": "Alabama"},
    ],
}

MAP_SERIES_GROUP_PAYLOAD = {
    "seriess": [
        {"series_id": "SMU56000000500000001A", "title": "Employment"},
    ],
}

MAP_REGIONAL_DATA_PAYLOAD = {
    "regional_data": [
        {"series_id": "LAUS", "region": "CA", "value": 4.2},
    ],
}

MAP_SERIES_DATA_PAYLOAD = {
    "series_data": [
        {"date": "2024-01-01", "value": 100.0},
    ],
}


@pytest.mark.asyncio
async def test_category_api_list_children() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = CategoryAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/category/children").respond(200, json=CATEGORY_PAYLOAD)
            result = await api.list_children(0)
            assert result.categories[0].name == "Root"


@pytest.mark.asyncio
async def test_release_api_get_tables() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = ReleaseAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/release/tables").respond(200, json=RELEASE_TABLES_PAYLOAD)
            result = await api.list_tables(1)
            assert result.release_tables == []


@pytest.mark.asyncio
async def test_source_api_get() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SourceAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/source").respond(200, json=SOURCES_PAYLOAD)
            source = await api.get(1)
            assert source.name == "Board of Governors"


@pytest.mark.asyncio
async def test_tag_api_list_related() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = TagAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/related_tags").respond(200, json=RELATED_TAGS_PAYLOAD)
            response = await api.list_related("gdp")
            assert response.related_tags[0].name == "gdp"


@pytest.mark.asyncio
async def test_series_api_get_series() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SeriesAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/series").respond(200, json=SERIES_SINGLE_PAYLOAD)
            result = await api.get_series("GDP")
            assert result.series[0].id == "GDP"


@pytest.mark.asyncio
async def test_series_api_get_observations() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SeriesAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/series/observations").respond(200, json=SERIES_OBSERVATIONS_PAYLOAD)
            result = await api.get_series_observations("GDP")
            assert len(result.observations) == 2


@pytest.mark.asyncio
async def test_series_api_not_found() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = SeriesAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/series").respond(200, json=SERIES_PAYLOAD)
            with pytest.raises(FREDAPIError):
                await api.get_series("GDP")


@pytest.mark.asyncio
async def test_maps_api_get_shapes() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = MapsAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/geofred/shapes/file").respond(200, json=MAP_SHAPES_PAYLOAD)
            result = await api.get_shapes("state")
            assert result.shape_values[0]["name"] == "Alabama"


@pytest.mark.asyncio
async def test_maps_api_get_series_group() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = MapsAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/geofred/series/group").respond(200, json=MAP_SERIES_GROUP_PAYLOAD)
            result = await api.get_series_group("SMU")
            assert result.series[0]["series_id"].startswith("SMU")


@pytest.mark.asyncio
async def test_maps_api_series_data() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = MapsAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/geofred/regional/data").respond(200, json=MAP_REGIONAL_DATA_PAYLOAD)
            mock.get("/geofred/series/data").respond(200, json=MAP_SERIES_DATA_PAYLOAD)
            regional = await api.get_regional_data()
            series = await api.get_series_data("SMU")
            assert regional.regional_data[0]["region"] == "CA"
            assert series.series_data[0]["value"] == 100.0
