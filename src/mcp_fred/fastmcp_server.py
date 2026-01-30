"""FastMCP server for FRED API.

This module is the entry point for the FastMCP-based FRED server.
It imports all tool modules to register them with the server
and provides the run function.
"""

from __future__ import annotations

# Import all tool modules to register their tools with the server
# The @mcp.tool decorators in each module register the tools on import
from .servers import (
    admin as _admin,  # noqa: F401
    categories as _categories,  # noqa: F401
    maps as _maps,  # noqa: F401
    releases as _releases,  # noqa: F401
    series as _series,  # noqa: F401
    sources as _sources,  # noqa: F401
    tags as _tags,  # noqa: F401
)

# Import the server instance from base (this creates the mcp instance with lifespan)
from .servers.base import mcp

# Progressive Disclosure: Disable data, advanced, and admin tiers by default
# These can be activated per-session using activate_* tools
# Core and discovery tools remain always visible
mcp.disable(tags={"tier:data", "tier:advanced", "tier:admin"})


def run_server():
    """Run the FastMCP server."""
    mcp.run()


__all__ = ["mcp", "run_server"]
