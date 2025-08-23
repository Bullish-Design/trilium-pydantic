#!/usr/bin/env python3
"""trilium-pydantic: Type-safe TriliumNext API client with Pydantic models."""

from __future__ import annotations

from .client import TriliumClient
from .config import ConnectionInfo  # TriliumConfig
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

# Import confidantic Settings (with our trilium settings already registered)
from confidantic import Settings


__all__ = [
    "TriliumClient",
    # "TriliumConfig",
    "Settings",
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
