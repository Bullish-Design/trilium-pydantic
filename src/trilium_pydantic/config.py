#!/usr/bin/env python3
"""TriliumNext-specific settings using confidantic.

This module defines trilium-specific configuration fields that extend
confidantic's base Settings class via the plugin system.
"""

from __future__ import annotations

from typing import Optional
from pydantic import Field, field_validator, ConfigDict
from confidantic import PluginRegistry, SettingsType
from dotenv import load_dotenv

load_dotenv()


class TriliumConfig(SettingsType):
    """TriliumNext-specific configuration fields."""

    model_config = ConfigDict(
        # populate_by_name=True,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    trilium_url: str = Field(
        default="http://localhost:8081", description="TriliumNext server URL"
    )
    trilium_token: Optional[str] = Field(
        default=None, description="ETAPI authentication token"
    )
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("trilium_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure URL doesn't end with slash."""
        return v.rstrip("/")

    @field_validator("trilium_token")
    @classmethod
    def validate_token(cls, v: Optional[str]) -> Optional[str]:
        """Validate token is not empty."""
        if v is not None and v.strip() == "":
            return None
        return v

    def is_configured(self) -> bool:
        """Check if minimum configuration is present."""
        return self.trilium_token is not None


# Register the trilium settings with confidantic's plugin system
PluginRegistry.register(TriliumConfig)

TriliumConfig = PluginRegistry.build_class()


class ConnectionInfo:
    """Information about TriliumNext server connection.

    Note: This is kept as a separate class for backward compatibility
    and because it represents derived/computed state rather than configuration.
    """

    def __init__(
        self,
        server_url: str,
        token_preview: str,
        is_connected: bool = False,
        app_version: Optional[str] = None,
        build_date: Optional[str] = None,
    ):
        self.server_url = server_url
        self.token_preview = token_preview
        self.is_connected = is_connected
        self.app_version = app_version
        self.build_date = build_date

    @classmethod
    def from_settings(cls, settings) -> ConnectionInfo:
        """Create connection info from confidantic settings."""
        token_preview = ""
        if settings.trilium_token:
            token = settings.trilium_token
            if len(token) > 10:
                token_preview = f"{token[:5]}***{token[-3:]}"
            else:
                token_preview = "***"

        return cls(server_url=settings.trilium_url, token_preview=token_preview)
