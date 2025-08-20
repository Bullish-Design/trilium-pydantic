#!/usr/bin/env python3
"""trilium-pydantic: Type-safe TriliumNext API client with Pydantic models."""

from __future__ import annotations

from .client import TriliumClient
from .config import TriliumConfig, ConnectionInfo
from .exceptions import (
    TriliumError,
    TriliumAPIError,
    TriliumConnectionError,
    TriliumConfigError,
)
from .models import (
    AppInfo,
    ConnectionTest,
    CreateNoteRequest,
    CreateNoteResponse,
    Note,
    SearchRequest,
    SearchResult,
    UpdateNoteRequest,
    NoteAttribute,
    NoteAttributes,
)

__version__ = "0.1.0"
__all__ = [
    "TriliumClient",
    "TriliumConfig",
    "ConnectionInfo",
    "TriliumError",
    "TriliumAPIError",
    "TriliumConnectionError",
    "TriliumConfigError",
    "AppInfo",
    "ConnectionTest",
    "CreateNoteRequest",
    "CreateNoteResponse",
    "Note",
    "SearchRequest",
    "SearchResult",
    "UpdateNoteRequest",
    "NoteAttribute",
    "NoteAttributes",
]
