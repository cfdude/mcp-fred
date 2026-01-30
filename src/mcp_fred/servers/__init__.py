"""FastMCP tool server modules for FRED API.

Each module in this package contains tools for a specific FRED API domain:
- categories: Category browsing and navigation
- releases: Economic data releases
- series: Time series data and metadata
- sources: Data source information
- tags: Tag-based discovery
- maps: GeoFRED geographic data
- admin: Project and job management utilities
"""

__all__ = [
    "admin",
    "categories",
    "maps",
    "releases",
    "series",
    "sources",
    "tags",
]
