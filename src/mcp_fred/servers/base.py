"""FastMCP server base module.

This module creates the FastMCP server instance and lifespan context.
Tool modules import `mcp` from here to register their tools.
"""

from __future__ import annotations

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan

from ..api import FREDClient, FREDClientConfig
from ..api.endpoints import CategoryAPI, MapsAPI, ReleaseAPI, SeriesAPI, SourceAPI, TagAPI
from ..config import load_config
from ..utils.background_worker import BackgroundWorker
from ..utils.file_writer import FileWriter
from ..utils.job_manager import JobManager
from ..utils.json_to_csv import JSONToCSVConverter
from ..utils.output_handler import ResultOutputHandler
from ..utils.path_resolver import PathResolver
from ..utils.token_estimator import TokenEstimator


@lifespan
async def fred_lifespan(server: FastMCP):
    """Initialize shared FRED resources for all tools.

    Yields a context dictionary containing:
    - config: AppConfig instance
    - client: FREDClient for API calls
    - categories: CategoryAPI endpoint wrapper
    - releases: ReleaseAPI endpoint wrapper
    - series: SeriesAPI endpoint wrapper
    - sources: SourceAPI endpoint wrapper
    - tags: TagAPI endpoint wrapper
    - maps: MapsAPI endpoint wrapper
    - output_handler: ResultOutputHandler for smart output routing
    - job_manager: JobManager for async job tracking
    - background_worker: BackgroundWorker for long-running tasks
    - token_estimator: TokenEstimator for payload sizing
    - path_resolver: PathResolver for file paths
    """
    load_dotenv()
    config = load_config()

    # Initialize FRED client with rate limiting and retry
    client_cfg = FREDClientConfig(
        api_key=config.fred_api_key,
        base_url=config.fred_base_url,
        timeout=30.0,
        max_requests_per_minute=config.rate_limit.max_requests_per_minute,
        max_retries=config.rate_limit.max_retries,
        retry_backoff_factor=config.rate_limit.retry_backoff_factor,
        retry_jitter=config.rate_limit.retry_jitter,
    )
    client = FREDClient(client_cfg)

    # Initialize endpoint wrappers
    categories = CategoryAPI(client)
    releases = ReleaseAPI(client)
    series = SeriesAPI(client)
    sources = SourceAPI(client)
    tags = TagAPI(client)
    maps = MapsAPI(client)

    # Initialize utility services
    token_estimator = TokenEstimator(
        assume_context_used=config.output.assume_context_used,
        default_safe_limit=config.output.safe_token_limit,
    )
    csv_converter = JSONToCSVConverter()
    path_resolver = PathResolver(config.storage.directory)
    file_writer = FileWriter()
    job_manager = JobManager(retention_hours=config.job.retention_hours)
    background_worker = BackgroundWorker(
        job_manager,
        max_retries=config.job.max_retries,
        initial_retry_delay=config.job.initial_retry_delay,
        retry_backoff_factor=config.job.retry_backoff_factor,
    )

    # Initialize output handler
    output_handler = ResultOutputHandler(
        config,
        token_estimator,
        csv_converter,
        path_resolver,
        file_writer,
        job_manager,
    )

    try:
        yield {
            # Config
            "config": config,
            # FRED client and endpoints
            "client": client,
            "categories": categories,
            "releases": releases,
            "series": series,
            "sources": sources,
            "tags": tags,
            "maps": maps,
            # Utilities
            "output_handler": output_handler,
            "job_manager": job_manager,
            "background_worker": background_worker,
            "token_estimator": token_estimator,
            "path_resolver": path_resolver,
            "csv_converter": csv_converter,
            "file_writer": file_writer,
        }
    finally:
        await client.aclose()


# Create main FastMCP server with lifespan
mcp = FastMCP(
    name="FRED MCP Server",
    instructions="""
    This server provides access to the Federal Reserve Economic Data (FRED) API.

    Available tool categories:
    - Core tools (always available): Category browsing, series lookup
    - Data tools: Time series observations, release data
    - Discovery tools: Search, tag exploration
    - Admin tools: Project and job management

    Use 'activate_data_tools' or 'activate_all_tools' to unlock additional functionality.
    Large datasets are automatically saved to files to preserve context window.
    """,
    lifespan=fred_lifespan,
)


__all__ = ["mcp"]
