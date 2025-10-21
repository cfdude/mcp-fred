import pytest
import respx

from mcp_fred.api import FREDAPIError, FREDClient, FREDClientConfig
from mcp_fred.api.endpoints import ReleaseAPI

BASE_URL = "https://api.stlouisfed.org"

RELEASE_LIST_PAYLOAD = {
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
            "name": "Employment Situation",
            "press_release": 0,
            "link": "https://example.com",
            "notes": "",
        }
    ],
}

RELEASE_SINGLE_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "release": RELEASE_LIST_PAYLOAD["releases"][0],
}

RELEASE_DATES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "release_dates": [
        {"date": "2024-01-01"},
    ],
}

RELEASE_SERIES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "seriess": [
        {
            "id": "PAYEMS",
            "title": "All Employees",
            "observation_start": "1939-01-01",
            "observation_end": "2024-01-01",
        }
    ],
}

RELEASE_SOURCES_PAYLOAD = {
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
            "name": "BLS",
            "link": "https://example.com",
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
            "name": "employment",
            "group_id": "macro",
            "notes": "",
            "created": "2024-01-01",
            "popularity": 90,
        }
    ],
}

RELEASE_RELATED_TAGS_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 1,
    "offset": 0,
    "limit": 1000,
    "related_tags": RELEASE_TAGS_PAYLOAD["tags"],
}

RELEASE_TABLES_PAYLOAD = {
    "realtime_start": "2024-01-01",
    "realtime_end": "2024-01-01",
    "count": 0,
    "offset": 0,
    "limit": 1000,
    "release_tables": [
        {"table": "A"},
    ],
}


@pytest.mark.asyncio
async def test_release_api_variants_success() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = ReleaseAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/releases").respond(200, json=RELEASE_LIST_PAYLOAD)
            releases = await api.list()
            assert releases.releases[0].name == "Employment Situation"

            mock.get("/fred/releases/dates").respond(200, json=RELEASE_DATES_PAYLOAD)
            release_dates = await api.list_dates()
            assert release_dates.release_dates[0].date.year == 2024

            mock.get("/fred/release").respond(200, json=RELEASE_SINGLE_PAYLOAD)
            release = await api.get(1)
            assert release.id == 1

            mock.get("/fred/release/dates").respond(200, json=RELEASE_DATES_PAYLOAD)
            dates = await api.get_dates(1)
            assert dates.release_dates[0].date.year == 2024

            mock.get("/fred/release/series").respond(200, json=RELEASE_SERIES_PAYLOAD)
            series = await api.list_series(1)
            assert series.series[0].id == "PAYEMS"

            mock.get("/fred/release/sources").respond(200, json=RELEASE_SOURCES_PAYLOAD)
            sources = await api.list_sources(1)
            assert sources.sources[0].name == "BLS"

            mock.get("/fred/release/tags").respond(200, json=RELEASE_TAGS_PAYLOAD)
            tags = await api.list_tags(1)
            assert tags.tags[0].name == "employment"

            mock.get("/fred/release/related_tags").respond(200, json=RELEASE_RELATED_TAGS_PAYLOAD)
            related_tags = await api.list_related_tags(1, "employment")
            assert related_tags.related_tags[0].name == "employment"

            mock.get("/fred/release/tables").respond(200, json=RELEASE_TABLES_PAYLOAD)
            tables = await api.list_tables(1)
            table_entry = tables.release_tables[0].model_dump()
            assert table_entry["table"] == "A"


@pytest.mark.asyncio
async def test_release_api_handles_not_found_and_rate_limit() -> None:
    async with FREDClient(FREDClientConfig(api_key="test")) as client:
        api = ReleaseAPI(client)
        with respx.mock(base_url=BASE_URL) as mock:
            mock.get("/fred/release").respond(404, json={})
            with pytest.raises(FREDAPIError) as not_found:
                await api.get(999)
            assert not_found.value.code == "NOT_FOUND"

            mock.get("/fred/release/tags").respond(
                429,
                json={},
                headers={"Retry-After": "30"},
            )
            with pytest.raises(FREDAPIError) as rate_limited:
                await api.list_tags(1)
            assert rate_limited.value.code == "RATE_LIMIT_EXCEEDED"
