"""Pydantic models for trilium-pydantic."""

from __future__ import annotations

from .notes import (
    AppInfo,
    CreateNoteRequest,
    Note,
    SearchResponse,
    SearchResult,
)

__all__ = [
    "AppInfo",
    "CreateNoteRequest", 
    "Note",
    "SearchResponse",
    "SearchResult",
]
