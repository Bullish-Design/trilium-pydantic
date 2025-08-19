"""Custom exceptions for trilium-pydantic."""

from __future__ import annotations


class TriliumError(Exception):
    """Base exception for trilium-pydantic."""
    pass


class TriliumAPIError(TriliumError):
    """API-related errors."""
    
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TriliumConfigError(TriliumError):
    """Configuration-related errors."""
    pass


class TriliumValidationError(TriliumError):
    """Validation-related errors."""
    pass
