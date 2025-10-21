"""Command-line interface for running MCP-FRED transports."""

from __future__ import annotations

import argparse
import asyncio
from contextlib import suppress

from .config import AppConfig, load_config
from .server import build_server_context
from .transports.http import HTTPTransport
from .transports.stdio import STDIOTransport


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the MCP-FRED server")
    parser.add_argument("--transport", choices=["stdio", "http"], help="Transport to use")
    parser.add_argument("--host", help="HTTP host (when using http transport)")
    parser.add_argument("--port", type=int, help="HTTP port (when using http transport)")
    return parser.parse_args()


def _resolve_config(args: argparse.Namespace) -> tuple[str, AppConfig, str | None, int | None]:
    config = load_config()
    transport = args.transport or config.transport
    host = args.host or config.http_host
    port = args.port or config.http_port
    return transport, config, host, port


def main() -> None:
    args = _parse_args()
    transport_name, _, host, port = _resolve_config(args)
    context = build_server_context()

    if transport_name == "stdio":
        transport = STDIOTransport(context)
        with suppress(KeyboardInterrupt):  # pragma: no cover - CLI behaviour
            asyncio.run(transport.run())
        return

    transport = HTTPTransport(context)
    try:
        import uvicorn  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
        raise SystemExit(
            "uvicorn is required to run the HTTP transport. Install uvicorn or use the stdio transport."
        ) from exc

    uvicorn.run(transport.app, host=host, port=port)  # pragma: no cover - requires runtime server


if __name__ == "__main__":  # pragma: no cover
    main()
