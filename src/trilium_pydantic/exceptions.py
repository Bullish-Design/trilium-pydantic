#!/usr/bin/env python3
"""Custom exceptions for trilium-pydantic."""
from __future__ import annotations


class TriliumError(Exception):
    """Base exception for trilium-pydantic."""
    pass


class TriliumConnectionError(TriliumError):
    """Raised when connection to TriliumNext fails."""
    pass


class TriliumAPIError(TriliumError):
    """Raised when API operation fails."""
    pass


class TriliumConfigError(TriliumError):
    """Raised when configuration is invalid."""
    pass
