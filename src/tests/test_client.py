"""Pytest tests for TriliumClient."""

from __future__ import annotations

import pytest

from trilium_pydantic import TriliumClient
from trilium_pydantic.exceptions import TriliumConfigError
from trilium_pydantic.models import CreateNoteRequest


class TestTriliumClient:
    """Test TriliumClient functionality."""
    
    def test_client_requires_token(self):
        """Test that client requires a valid token."""
        # This would fail without proper env setup
        with pytest.raises(TriliumConfigError):
            TriliumClient()
    
    @pytest.mark.integration
    def test_connection(self):
        """Test basic connection to TriliumNext."""
        with TriliumClient() as client:
            app_info = client.app_info()
            assert app_info.app_version
            assert isinstance(app_info.db_version, int)
    
    @pytest.mark.integration
    def test_note_crud(self):
        """Test note CRUD operations."""
        with TriliumClient() as client:
            # Create
            request = CreateNoteRequest(
                parent_note_id="root",
                title="Test Note",
                content="Test content",
                note_type="text"
            )
            note = client.notes.create(request)
            assert note.note_id
            assert note.title == "Test Note"
            
            # Read
            retrieved = client.notes.get(note.note_id)
            assert retrieved.title == "Test Note"
            
            # Update
            retrieved.title = "Updated Title"
            updated = client.notes.update(retrieved)
            assert updated.title == "Updated Title"
            
            # Delete
            assert client.notes.delete(note.note_id)
    
    @pytest.mark.integration
    def test_search(self):
        """Test note search functionality."""
        with TriliumClient() as client:
            results = client.notes.search("root")
            assert len(results.notes) > 0
