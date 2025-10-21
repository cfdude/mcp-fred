"""Configuration management for MCP-FRED."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class StorageConfig(BaseModel):
    directory: str = Field(default="./fred-data", description="Root directory for project storage")
    default_project: str = Field(default="default", description="Default project name when none provided")


class OutputConfig(BaseModel):
    mode: Literal["auto", "screen", "file"] = Field(default="auto")
    format: Literal["csv", "json"] = Field(default="csv")
    filename_pattern: str = Field(default="{series_id}_{operation}_{date}_{time}")
    screen_row_threshold: int = Field(default=1000, ge=1)
    job_row_threshold: int = Field(default=10_000, ge=1)
    file_chunk_size: int = Field(default=1000, ge=1)
    safe_token_limit: int = Field(default=50_000, ge=1)
    assume_context_used: float = Field(default=0.75, ge=0.0, le=0.99)


class RateLimitConfig(BaseModel):
    max_requests_per_minute: int = Field(default=120, ge=1)
    max_retries: int = Field(default=3, ge=0)
    retry_backoff_factor: float = Field(default=1.5, ge=0.0)
    retry_jitter: float = Field(default=0.25, ge=0.0)


class JobConfig(BaseModel):
    retention_hours: int = Field(default=24, ge=1, description="Number of hours to retain completed jobs")
    max_retries: int = Field(default=3, ge=0, description="Maximum background retry attempts before failing a job")
    initial_retry_delay: float = Field(default=1.0, ge=0.0, description="Initial retry delay in seconds")
    retry_backoff_factor: float = Field(default=2.0, ge=1.0, description="Multiplier applied to retry delays")


class AppConfig(BaseModel):
    fred_api_key: str
    fred_base_url: str = Field(default="https://api.stlouisfed.org")
    storage: StorageConfig = Field(default_factory=StorageConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    job: JobConfig = Field(default_factory=JobConfig)
    transport: Literal["stdio", "http"] = Field(default="stdio")
    http_host: str = Field(default="127.0.0.1")
    http_port: int = Field(default=8000)


def load_config(**overrides: object) -> AppConfig:
    return AppConfig(**overrides)


__all__ = [
    "AppConfig",
    "JobConfig",
    "OutputConfig",
    "RateLimitConfig",
    "StorageConfig",
    "load_config",
]
