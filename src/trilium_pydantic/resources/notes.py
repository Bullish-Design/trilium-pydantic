"""Notes resource for TriliumNext API operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..exceptions import TriliumAPIError
from ..models.notes import (
    AppInfo,
    CreateNoteRequest,
    Note,
    SearchResponse,
)

if TYPE_CHECKING:
    from ..client import TriliumClient


class NotesResource:
    """Handle note-related API operations."""
    
    def __init__(self, client: TriliumClient):
        self._client = client
    
    def create(self, request: CreateNoteRequest) -> Note:
        """Create a new note."""
        try:
            response = self._client._http_client.post(
                "/etapi/notes",
                json=request.model_dump(exclude_none=True),
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return Note.model_validate(response.json()["note"])
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to create note: {e}")
    
    def get(self, note_id: str) -> Note:
        """Get a note by ID."""
        try:
            response = self._client._http_client.get(
                f"/etapi/notes/{note_id}",
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return Note.model_validate(response.json())
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to get note: {e}")
    
    def update(self, note: Note) -> Note:
        """Update an existing note."""
        try:
            response = self._client._http_client.patch(
                f"/etapi/notes/{note.note_id}",
                json={"title": note.title},
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return Note.model_validate(response.json())
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to update note: {e}")
    
    def delete(self, note_id: str) -> bool:
        """Delete a note."""
        try:
            response = self._client._http_client.delete(
                f"/etapi/notes/{note_id}",
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to delete note: {e}")
    
    def search(self, query: str, limit: int = 50) -> SearchResponse:
        """Search for notes."""
        try:
            response = self._client._http_client.get(
                "/etapi/notes",
                params={"search": query, "limit": limit},
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return SearchResponse.model_validate(response.json())
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to search notes: {e}")
    
    def get_content(self, note_id: str) -> str:
        """Get note content."""
        try:
            response = self._client._http_client.get(
                f"/etapi/notes/{note_id}/content",
                headers=self._client._get_headers(),
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to get note content: {e}")
