#!/usr/bin/env python3
"""Pydantic models for TriliumNext API interactions.

Type-safe models for requests and responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, validator


# Request Models
class CreateNoteRequest(BaseModel):
    """Request to create a new note."""

    parent_note_id: str = Field(description="ID of parent note")
    title: str = Field(description="Note title")
    content: str = Field(default="", description="Note content")
    note_type: Literal[
        "text", "code", "file", "image", "search", "book", "relationMap", "canvas"
    ] = Field(default="text", description="Type of note")
    mime: Optional[str] = Field(default=None, description="MIME type for code notes")
    note_position: Optional[int] = Field(
        default=None, description="Position among siblings"
    )
    prefix: Optional[str] = Field(default=None, description="Prefix for the note")
    is_expanded: Optional[bool] = Field(
        default=None, description="Whether note is expanded in tree"
    )
    note_id: Optional[str] = Field(
        default=None, description="Specific note ID (optional)"
    )
    branch_id: Optional[str] = Field(
        default=None, description="Specific branch ID (optional)"
    )


class UpdateNoteRequest(BaseModel):
    """Request to update note properties."""

    title: Optional[str] = Field(default=None, description="New title")
    note_type: Optional[str] = Field(default=None, description="New type")
    mime: Optional[str] = Field(default=None, description="New MIME type")


class SearchRequest(BaseModel):
    """Request to search notes."""

    search: str = Field(description="Search query")
    fast_search: bool = Field(default=True, description="Use fast search")
    include_archived_notes: bool = Field(
        default=False, description="Include archived notes"
    )
    ancestor_note_id: Optional[str] = Field(
        default=None, description="Limit search to descendants of this note"
    )
    order_by: Optional[List[str]] = Field(
        default=None, description="Order results by fields"
    )
    limit: Optional[int] = Field(default=None, description="Maximum results to return")


# NEW: strongly-typed note attributes
class NoteAttribute(BaseModel):
    """Attribute attached to a note."""

    attribute_id: Optional[str] = Field(
        default=None, alias="attributeId", description="Attribute ID"
    )
    note_id: Optional[str] = Field(
        default=None, alias="noteId", description="Owning note ID"
    )
    type: str = Field(description="Attribute type")
    name: str = Field(description="Attribute name")
    value: str = Field(description="Attribute value")
    is_inheritable: bool = Field(
        alias="isInheritable",
        default=False,
        description="Whether attribute is inheritable",
    )

    # Often present on ETAPI responses
    date_created: Optional[datetime] = Field(default=None, alias="dateCreated")
    date_modified: Optional[datetime] = Field(default=None, alias="dateModified")
    utc_date_created: Optional[datetime] = Field(default=None, alias="utcDateCreated")
    utc_date_modified: Optional[datetime] = Field(default=None, alias="utcDateModified")

    class Config:
        populate_by_name = True


# Convenience alias
NoteAttributes = List[NoteAttribute]


# Response Models
class Note(BaseModel):
    """TriliumNext note representation."""

    note_id: str = Field(alias="noteId", description="Unique note identifier")
    title: str = Field(description="Note title")
    note_type: str = Field(alias="type", description="Type of note")
    mime: Optional[str] = Field(default=None, description="MIME type")
    is_protected: bool = Field(
        alias="isProtected", description="Whether note is protected"
    )
    date_created: datetime = Field(
        alias="dateCreated", description="Creation timestamp"
    )
    date_modified: datetime = Field(
        alias="dateModified", description="Last modification"
    )
    utc_date_created: datetime = Field(
        alias="utcDateCreated", description="UTC creation"
    )
    utc_date_modified: datetime = Field(
        alias="utcDateModified", description="UTC modification"
    )
    parent_note_ids: List[str] = Field(
        alias="parentNoteIds", description="Parent note IDs"
    )
    child_note_ids: List[str] = Field(
        alias="childNoteIds", description="Child note IDs"
    )
    parent_branch_ids: List[str] = Field(
        alias="parentBranchIds", description="Parent branch IDs"
    )
    child_branch_ids: List[str] = Field(
        alias="childBranchIds", description="Child branch IDs"
    )
    attributes: NoteAttributes = Field(
        default_factory=list, description="Note attributes"
    )

    class Config:
        populate_by_name = True


class AppInfo(BaseModel):
    """TriliumNext application information."""

    app_version: str = Field(alias="appVersion", description="Application version")
    db_version: int = Field(alias="dbVersion", description="Database version")
    node_version: str = Field(alias="nodeVersion", description="Node.js version")
    sync_version: int = Field(alias="syncVersion", description="Sync version")
    build_date: str = Field(alias="buildDate", description="Build timestamp")
    build_revision: str = Field(alias="buildRevision", description="Git revision")
    data_directory: str = Field(
        alias="dataDirectory", description="Data directory path"
    )
    clipper_protocol_version: str = Field(
        alias="clipperProtocolVersion", description="Web clipper protocol version"
    )
    utc_date_time: str = Field(
        alias="utcDateTime", description="Current server UTC time"
    )


class SearchResult(BaseModel):
    """Search operation result."""

    results: List[Dict[str, Any]] = Field(description="List of matching notes")


class CreateNoteResponse(BaseModel):
    """Response from note creation."""

    note: Note = Field(description="Created note")
    branch: Dict[str, Any] = Field(description="Created branch")


class ErrorResponse(BaseModel):
    """API error response."""

    code: str = Field(description="Error code")
    message: str = Field(description="Error message")


# Utility Models
class ConnectionTest(BaseModel):
    """Connection test result."""

    success: bool = Field(description="Whether connection succeeded")
    server_url: str = Field(description="Server URL tested")
    app_info: Optional[AppInfo] = Field(
        default=None, description="Server app info if connected"
    )
    error: Optional[str] = Field(default=None, description="Error message if failed")
