"""Trilium-pydantic: Type-safe TriliumNext API client."""

from __future__ import annotations

from .client import TriliumClient
from .config import TriliumConfig, load_config
from .exceptions import (
    TriliumAPIError,
    TriliumConfigError,
    TriliumError,
    TriliumValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "TriliumClient",
    "TriliumConfig",
    "load_config",
    "TriliumError",
    "TriliumAPIError",
    "TriliumConfigError",
    "TriliumValidationError",
]
