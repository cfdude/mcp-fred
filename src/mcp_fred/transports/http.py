"""HTTP transport implementation for MCP-FRED."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from ..server import ServerContext, build_server_context
from . import TOOL_HANDLERS, TOOL_REGISTRY


class HTTPTransport:
    """Minimal ASGI application exposing tool listing and invocation endpoints."""

    def __init__(self, context: ServerContext | None = None) -> None:
        self.context = context or build_server_context()
        self.app = self._asgi_app
        self._lock = asyncio.Lock()

    async def _asgi_app(self, scope: dict[str, Any], receive, send) -> None:  # type: ignore[override]
        if scope.get("type") != "http":  # pragma: no cover - defensive
            await self._send_response(send, 500, {"error": "Unsupported scope"})
            return

        method = scope.get("method", "GET").upper()
        path = scope.get("path", "/")

        if method == "GET" and path == "/health":
            await self._send_response(send, 200, {"status": "ok"})
            return

        if method == "GET" and path == "/tools":
            tools = [
                {
                    "name": spec.name,
                    "summary": spec.summary,
                    "optional": spec.optional,
                }
                for spec in TOOL_REGISTRY.values()
            ]
            await self._send_response(send, 200, {"tools": tools})
            return

        if method == "POST" and path.startswith("/tools/"):
            tool_name = path.split("/", 2)[2]
            if tool_name not in TOOL_HANDLERS:
                await self._send_response(send, 404, {"detail": f"Unknown tool '{tool_name}'"})
                return

            payload = await self._read_body(receive)
            if payload is None:
                await self._send_response(send, 400, {"detail": "Invalid JSON payload"})
                return

            operation = payload.get("operation")
            if not operation:
                await self._send_response(send, 400, {"detail": "'operation' is required"})
                return

            arguments = payload.get("arguments", {})
            handler = TOOL_HANDLERS[tool_name]
            async with self._lock:
                result = await handler(self.context, operation, **arguments)
            await self._send_response(send, 200, {"tool": tool_name, "data": result})
            return

        await self._send_response(send, 404, {"detail": "Not Found"})

    async def _read_body(self, receive) -> dict[str, Any] | None:
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body"):
                break
        if not body:
            return {}
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    async def _send_response(self, send, status: int, data: dict[str, Any]) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers = [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode()),
        ]
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": body})


__all__ = ["HTTPTransport"]
