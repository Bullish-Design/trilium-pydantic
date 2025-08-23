#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from .client import TriliumClient  # type: ignore
from .models import Note  # type: ignore


class DummyConfig:
    trilium_url = "http://test"
    trilium_token = "x"

    @staticmethod
    def is_configured() -> bool:
        return True


class FakeETAPI:
    def __init__(self, note_payload):
        self._note = note_payload

    def get_note(self, note_id: str):
        return self._note


def test_client_get_note_parses_attributes():
    raw_note = {
        "noteId": "note-999",
        "title": "Client Note",
        "type": "text",
        "mime": "text/html",
        "isProtected": False,
        "dateCreated": "2025-08-18T10:30:00Z",
        "dateModified": "2025-08-18T10:31:00Z",
        "utcDateCreated": "2025-08-18T10:30:00Z",
        "utcDateModified": "2025-08-18T10:31:00Z",
        "parentNoteIds": [],
        "childNoteIds": [],
        "parentBranchIds": [],
        "childBranchIds": [],
        "attributes": [
            {
                "attributeId": "a1",
                "noteId": "note-999",
                "type": "label",
                "name": "status",
                "value": "draft",
                "isInheritable": False,
            }
        ],
    }

    client = TriliumClient(DummyConfig())
    # Inject fake ETAPI to avoid network
    client._etapi = FakeETAPI(raw_note)

    note = client.get_note("note-999")
    assert isinstance(note, Note)
    assert note.note_id == "note-999"
    assert note.attributes and note.attributes[0].name == "status"
    assert note.attributes[0].value == "draft"
