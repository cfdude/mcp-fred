"""Command-line interface for running MCP-FRED.

Supports both the new FastMCP transport (default) and the legacy STDIO transport.
"""

from __future__ import annotations

import os
from contextlib import suppress


def main() -> None:
    """Run the MCP-FRED server.

    Uses FastMCP by default. Set MCPFRED_LEGACY=1 to use the old STDIO transport.
    """
    use_legacy = os.getenv("MCPFRED_LEGACY", "").lower() in ("1", "true", "yes")

    if use_legacy:
        # Use legacy STDIO transport
        import asyncio

        from .server import build_server_context
        from .transports.stdio import STDIOTransport

        context = build_server_context()
        transport = STDIOTransport(context)
        with suppress(KeyboardInterrupt):
            asyncio.run(transport.run())
    else:
        # Use new FastMCP server (default)
        from .fastmcp_server import run_server

        with suppress(KeyboardInterrupt):
            run_server()


if __name__ == "__main__":
    main()
