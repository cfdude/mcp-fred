"""STDIO transport implementation for MCP-FRED."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from ..server import ServerContext, build_server_context
from . import TOOL_HANDLERS, TOOL_REGISTRY


class STDIOTransport:
    """Simple JSON-RPC transport over stdin/stdout."""

    def __init__(self, context: ServerContext | None = None) -> None:
        self._context = context or build_server_context()
        self._lock = asyncio.Lock()

    async def run(self) -> None:
        """Start processing messages from stdin until EOF."""

        loop = asyncio.get_running_loop()
        try:
            while True:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    await self._write_response(
                        {"error": {"code": "INVALID_JSON", "message": "Failed to decode request"}}
                    )
                    continue
                response = await self.handle_request(request)
                await self._write_response(response)
        finally:
            await self._context.aclose()

    async def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process a single JSON-RPC request."""

        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "tools/list":
                tools = [
                    {
                        "name": spec.name,
                        "summary": spec.summary,
                        "optional": spec.optional,
                    }
                    for spec in TOOL_REGISTRY.values()
                ]
                return {"id": request_id, "result": {"tools": tools}}

            if method == "tools/call":
                name = params.get("name")
                if name not in TOOL_HANDLERS:
                    raise ValueError(f"Unknown tool '{name}'")
                arguments = params.get("arguments", {})
                operation = arguments.pop("operation", None)
                if operation is None:
                    raise ValueError("'operation' parameter is required")
                handler = TOOL_HANDLERS[name]
                async with self._lock:
                    result = await handler(self._context, operation, **arguments)
                return {"id": request_id, "result": {"tool": name, "data": result}}

            if method == "ping":
                return {"id": request_id, "result": {"status": "ok"}}

            raise ValueError(f"Unsupported method '{method}'")
        except Exception as exc:  # pragma: no cover - defensive
            return {
                "id": request_id,
                "error": {
                    "code": "TRANSPORT_ERROR",
                    "message": str(exc),
                },
            }

    async def _write_response(self, response: dict[str, Any]) -> None:
        loop = asyncio.get_running_loop()
        data = json.dumps(response, ensure_ascii=False)
        await loop.run_in_executor(None, sys.stdout.write, data + "\n")
        await loop.run_in_executor(None, sys.stdout.flush)


__all__ = ["STDIOTransport"]
