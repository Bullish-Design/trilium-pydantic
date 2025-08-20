
#!/usr/bin/env python3
import sys
from datetime import datetime, timezone

# Ensure local package imports resolve
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import NoteAttribute, Note  # type: ignore


def test_note_attribute_aliases_and_dump_by_alias():
    raw = {
        "attributeId": "attr-1",
        "noteId": "note-123",
        "type": "label",
        "name": "color",
        "value": "blue",
        "isInheritable": True,
        "dateCreated": "2025-08-18T10:30:00Z",
        "dateModified": "2025-08-18T10:31:00Z",
        "utcDateCreated": "2025-08-18T10:30:00Z",
        "utcDateModified": "2025-08-18T10:31:00Z",
    }

    attr = NoteAttribute(**raw)

    # Access via snake_case field names
    assert attr.attribute_id == "attr-1"
    assert attr.note_id == "note-123"
    assert attr.type == "label"
    assert attr.name == "color"
    assert attr.value == "blue"
    assert attr.is_inheritable is True

    # Dates should be parsed
    assert isinstance(attr.date_created, datetime)
    assert attr.date_created.tzinfo is not None

    dumped = attr.model_dump(by_alias=True, exclude_none=True)
    for k in ["attributeId", "noteId", "type", "name", "value", "isInheritable",
              "dateCreated", "dateModified", "utcDateCreated", "utcDateModified"]:
        assert k in dumped


def test_note_parses_attributes_into_models():
    # Minimal viable raw note matching our Note model fields
    raw_note = {
        "noteId": "note-123",
        "title": "A Note",
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
                "attributeId": "attr-1",
                "noteId": "note-123",
                "type": "label",
                "name": "color",
                "value": "blue",
                "isInheritable": True,
            },
            {
                "attributeId": "attr-2",
                "noteId": "note-123",
                "type": "relation",
                "name": "link",
                "value": "note-xyz",
                "isInheritable": False,
            },
        ],
    }

    note = Note(**raw_note)
    assert isinstance(note.attributes, list)
    assert len(note.attributes) == 2
    assert all(hasattr(a, "attribute_id") for a in note.attributes)
    assert note.attributes[0].name == "color"
    assert note.attributes[1].type == "relation"
