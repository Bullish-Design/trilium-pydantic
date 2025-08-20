#!/usr/bin/env python3
"""Configuration management for trilium-pydantic.

Handles environment-based configuration with validation.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class TriliumConfig(BaseSettings):
    """Configuration for TriliumNext client.

    Loads from environment variables or .env file.
    """

    trilium_url: str = Field(
        default="http://localhost:8081", description="TriliumNext server URL"
    )
    trilium_token: Optional[str] = Field(
        default=None, description="ETAPI authentication token"
    )
    log_level: str = Field(default="INFO", description="Logging level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("trilium_url")
    def validate_url(cls, v: str) -> str:
        """Ensure URL doesn't end with slash."""
        return v.rstrip("/")

    @validator("trilium_token")
    def validate_token(cls, v: Optional[str]) -> Optional[str]:
        """Validate token is not empty."""
        if v is not None and v.strip() == "":
            return None
        return v

    def is_configured(self) -> bool:
        """Check if minimum configuration is present."""
        return self.trilium_token is not None


class ConnectionInfo(BaseModel):
    """Information about TriliumNext server connection."""

    server_url: str
    token_preview: str
    is_connected: bool = False
    app_version: Optional[str] = None
    build_date: Optional[str] = None

    @classmethod
    def from_config(cls, config: TriliumConfig) -> ConnectionInfo:
        """Create connection info from config."""
        token_preview = ""
        if config.trilium_token:
            token = config.trilium_token
            if len(token) > 10:
                token_preview = f"{token[:5]}***{token[-3:]}"
            else:
                token_preview = "***"

        return cls(server_url=config.trilium_url, token_preview=token_preview)
