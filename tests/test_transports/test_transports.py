import pytest
import respx
from httpx import ASGITransport, AsyncClient

from mcp_fred.transports.http import HTTPTransport
from mcp_fred.transports.stdio import STDIOTransport

BASE_URL = "https://api.stlouisfed.org"


@pytest.mark.asyncio
async def test_stdio_tools_list(server_context):
    transport = STDIOTransport(server_context)
    response = await transport.handle_request({"id": 1, "method": "tools/list"})
    assert "tools" in response["result"]
    assert any(tool["name"] == "fred_series" for tool in response["result"]["tools"])


@pytest.mark.asyncio
async def test_stdio_tool_call(server_context):
    transport = STDIOTransport(server_context)
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/fred/series").respond(
            200,
            json={
                "realtime_start": "2024-01-01",
                "realtime_end": "2024-01-01",
                "seriess": [
                    {
                        "id": "GDP",
                        "title": "Gross Domestic Product",
                    }
                ],
            },
        )
        request = {
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "fred_series",
                "arguments": {"operation": "get", "series_id": "GDP"},
            },
        }
        response = await transport.handle_request(request)
    assert response["result"]["data"]["status"] == "success"


@pytest.mark.asyncio
async def test_stdio_unknown_tool_returns_error(server_context):
    transport = STDIOTransport(server_context)
    response = await transport.handle_request(
        {
            "id": 3,
            "method": "tools/call",
            "params": {"name": "unknown", "arguments": {"operation": "get"}},
        }
    )
    assert response["error"]["code"] == "TRANSPORT_ERROR"


@pytest.mark.asyncio
async def test_http_transport_list_tools(server_context):
    transport = HTTPTransport(server_context)
    asgi_transport = ASGITransport(app=transport.app)
    async with AsyncClient(transport=asgi_transport, base_url="http://test") as client:
        response = await client.get("/tools")
    data = response.json()
    assert response.status_code == 200
    assert any(tool["name"] == "fred_maps" for tool in data["tools"])


@pytest.mark.asyncio
async def test_http_transport_tool_call(server_context):
    transport = HTTPTransport(server_context)
    payload = {"operation": "get_series_group", "arguments": {"series_id": "SMU"}}
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/geofred/series/group").respond(200, json={"seriess": []})
        asgi_transport = ASGITransport(app=transport.app)
        async with AsyncClient(transport=asgi_transport, base_url="http://test") as client:
            response = await client.post("/tools/fred_maps", json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "success"


@pytest.mark.asyncio
async def test_http_transport_unknown_tool(server_context):
    transport = HTTPTransport(server_context)
    asgi_transport = ASGITransport(app=transport.app)
    async with AsyncClient(transport=asgi_transport, base_url="http://test") as client:
        response = await client.post("/tools/unknown", json={"operation": "get"})
    assert response.status_code == 404
