"""Note-related Pydantic models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class CreateNoteRequest(BaseModel):
    """Request model for creating a note."""
    
    parent_note_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(default="")
    note_type: str = Field(default="text")
    mime: str = Field(default="text/html")
    note_id: str | None = None
    
    @validator("note_type")
    def validate_note_type(cls, v: str) -> str:
        """Validate note type."""
        valid_types = {"text", "code", "relationMap", "canvas", "book"}
        if v not in valid_types:
            raise ValueError(f"Invalid note type: {v}")
        return v


class Note(BaseModel):
    """TriliumNext note model."""
    
    note_id: str
    title: str
    note_type: str
    mime: str
    is_protected: bool
    created_date: datetime
    modified_date: datetime
    parent_note_ids: list[str]
    child_note_ids: list[str]
    branch_id: str | None = None
    content: str | None = None
    
    class Config:
        """Pydantic configuration."""
        alias_generator = lambda field_name: "".join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split("_"))
        )
        populate_by_name = True


class SearchResult(BaseModel):
    """Search result model."""
    
    note_id: str
    title: str
    
    class Config:
        """Pydantic configuration."""
        alias_generator = lambda field_name: "".join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split("_"))
        )


class SearchResponse(BaseModel):
    """Search response model."""
    
    notes: list[SearchResult]
    search_string: str
    
    class Config:
        """Pydantic configuration."""
        alias_generator = lambda field_name: "".join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split("_"))
        )


class AppInfo(BaseModel):
    """Application info model."""
    
    app_version: str
    db_version: int
    sync_version: int
    build_date: str
    build_revision: str
    data_directory: str
    
    class Config:
        """Pydantic configuration."""
        alias_generator = lambda field_name: "".join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split("_"))
        )
