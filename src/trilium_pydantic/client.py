#!/usr/bin/env python3
"""TriliumNext Pydantic client.

Type-safe wrapper around trilium-py with Pydantic models.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Optional

from trilium_py.client import ETAPI

from .config import TriliumConfig, ConnectionInfo
from .models import (
    AppInfo,
    CreateNoteRequest,
    CreateNoteResponse,
    Note,
    SearchRequest,
    SearchResult,
    UpdateNoteRequest,
    ConnectionTest,
    ErrorResponse,
)
from .exceptions import TriliumAPIError, TriliumConnectionError


logger = logging.getLogger(__name__)


class TriliumClient:
    """Type-safe TriliumNext client with Pydantic models."""

    def __init__(self, config: Optional[TriliumConfig] = None):
        """Initialize client with configuration.

        Args:
            config: TriliumConfig instance. If None, loads from environment.
        """
        self.config = config or TriliumConfig()
        self._etapi: Optional[ETAPI] = None

        if not self.config.is_configured():
            raise TriliumConnectionError(
                "No TRILIUM_TOKEN found. Set environment variable or pass config."
            )

    @property
    def etapi(self) -> ETAPI:
        """Get or create ETAPI client instance."""
        if self._etapi is None:
            self._etapi = ETAPI(
                server_url=self.config.trilium_url, token=self.config.trilium_token
            )
        return self._etapi

    def test_connection(self) -> ConnectionTest:
        """Test connection to TriliumNext server.

        Returns:
            ConnectionTest with success status and app info.
        """
        try:
            app_info_raw = self.etapi.app_info()
            # print(f"\nApp Info: {app_info_raw}\n\n")
            app_info = AppInfo(**app_info_raw)
            # print(f"\nParsed App Info: {app_info}\n\n")

            return ConnectionTest(
                success=True, server_url=self.config.trilium_url, app_info=app_info
            )
        except Exception as e:
            return ConnectionTest(
                success=False, server_url=self.config.trilium_url, error=str(e)
            )

    def get_app_info(self) -> AppInfo:
        """Get TriliumNext application information.

        Returns:
            AppInfo model with server details.

        Raises:
            TriliumAPIError: If API call fails.
        """
        try:
            app_info_raw = self.etapi.app_info()
            return AppInfo(**app_info_raw)
        except Exception as e:
            raise TriliumAPIError(f"Failed to get app info: {e}")

    def get_note(self, note_id: str) -> Note:
        """Get note by ID.

        Args:
            note_id: Note identifier.

        Returns:
            Note model.

        Raises:
            TriliumAPIError: If note not found or API call fails.
        """
        try:
            note_raw = self.etapi.get_note(note_id)
            return Note(**note_raw)
        except Exception as e:
            raise TriliumAPIError(f"Failed to get note {note_id}: {e}")

    def get_note_content(self, note_id: str) -> str:
        """Get note content.

        Args:
            note_id: Note identifier.

        Returns:
            Note content as string.

        Raises:
            TriliumAPIError: If note not found or API call fails.
        """
        try:
            return self.etapi.get_note_content(note_id)
        except Exception as e:
            raise TriliumAPIError(f"Failed to get note content {note_id}: {e}")

    def create_note(self, request: CreateNoteRequest) -> CreateNoteResponse:
        """Create new note.

        Args:
            request: CreateNoteRequest with note details.

        Returns:
            CreateNoteResponse with created note.

        Raises:
            TriliumAPIError: If creation fails.
        """
        try:
            response_raw = self.etapi.create_note(
                parentNoteId=request.parent_note_id,
                title=request.title,
                type=request.note_type,
                content=request.content,
                mime=request.mime,
                notePosition=request.note_position,
                prefix=request.prefix,
                isExpanded=request.is_expanded,
                noteId=request.note_id,
                branchId=request.branch_id,
            )

            # Convert raw response to typed models
            note_data = response_raw["note"]
            branch_data = response_raw["branch"]

            note = Note(**note_data)

            return CreateNoteResponse(note=note, branch=branch_data)
        except Exception as e:
            raise TriliumAPIError(f"Failed to create note: {e}")

    def update_note_content(self, note_id: str, content: str) -> bool:
        """Update note content.

        Args:
            note_id: Note identifier.
            content: New content.

        Returns:
            True if successful.

        Raises:
            TriliumAPIError: If update fails.
        """
        try:
            return self.etapi.update_note_content(note_id, content)
        except Exception as e:
            raise TriliumAPIError(f"Failed to update note content {note_id}: {e}")

    def update_note(self, note_id: str, request: UpdateNoteRequest) -> Note:
        """Update note properties.

        Args:
            note_id: Note identifier.
            request: UpdateNoteRequest with changes.

        Returns:
            Updated Note model.

        Raises:
            TriliumAPIError: If update fails.
        """
        try:
            # Build update parameters
            update_params = {}
            if request.title is not None:
                update_params["title"] = request.title
            if request.note_type is not None:
                update_params["type"] = request.note_type
            if request.mime is not None:
                update_params["mime"] = request.mime

            updated_raw = self.etapi.patch_note(note_id, **update_params)
            return Note(**updated_raw)
        except Exception as e:
            raise TriliumAPIError(f"Failed to update note {note_id}: {e}")

    def search_notes(self, request: SearchRequest) -> SearchResult:
        """Search notes.

        Args:
            request: SearchRequest with search parameters.

        Returns:
            SearchResult with matching notes.

        Raises:
            TriliumAPIError: If search fails.
        """
        try:
            # Build search parameters
            params = {
                "fastSearch": request.fast_search,
                "includeArchivedNotes": request.include_archived_notes,
            }

            if request.ancestor_note_id:
                params["ancestorNoteId"] = request.ancestor_note_id
            if request.order_by:
                params["orderBy"] = request.order_by
            if request.limit:
                params["limit"] = request.limit

            result_raw = self.etapi.search_note(request.search, **params)
            return SearchResult(**result_raw)
        except Exception as e:
            raise TriliumAPIError(f"Failed to search notes: {e}")

    def delete_note(self, note_id: str) -> bool:
        """Delete note.

        Args:
            note_id: Note identifier.

        Returns:
            True if successful.

        Raises:
            TriliumAPIError: If deletion fails.
        """
        try:
            return self.etapi.delete_note(note_id)
        except Exception as e:
            raise TriliumAPIError(f"Failed to delete note {note_id}: {e}")

    def get_connection_info(self) -> ConnectionInfo:
        """Get connection information.

        Returns:
            ConnectionInfo with current connection details.
        """
        conn_info = ConnectionInfo.from_config(self.config)

        # Test if actually connected
        test_result = self.test_connection()
        conn_info.is_connected = test_result.success

        if test_result.app_info:
            conn_info.app_version = test_result.app_info.app_version
            conn_info.build_date = test_result.app_info.build_date

        return conn_info
