import pytest
import respx

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
    import json

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
    # MCP protocol wraps result in content array with text
    result_text = response["result"]["content"][0]["text"]
    result_data = json.loads(result_text)
    assert result_data["status"] == "success"


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
    # JSON-RPC uses numeric error codes; -32000 is server error
    assert response["error"]["code"] == -32000
    assert "unknown" in response["error"]["message"].lower()
