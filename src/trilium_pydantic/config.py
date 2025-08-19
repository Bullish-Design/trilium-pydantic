"""Configuration management for trilium-pydantic."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class TriliumConfig(BaseSettings):
    """TriliumNext configuration settings."""

    url: str = Field(
        default="http://localhost:8081", env="TRILIUM_URL", alias="trilium_url"
    )
    token: str = Field(default="", env="TRILIUM_TOKEN", alias="trilium_token")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config(env_file: Path | str | None = None) -> TriliumConfig:
    """Load configuration from environment or .env file."""
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to load from current directory
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            load_dotenv(env_path)

    return TriliumConfig()
