# README.md

Type-safe Python client for the TriliumNext ETAPI, built on top of \[`trilium-py`]. It wraps ETAPI calls in a small `TriliumClient` and uses Pydantic models for request/response validation, including strongly-typed note attributes.

## Features

* **Typed models** for notes, attributes, app info, search results, etc.
* **Simple client** for common operations:

  * `test_connection()`, `get_app_info()`
  * `get_note()`, `get_note_content()`
  * `create_note()`, `update_note()`, `update_note_content()`
  * `search_notes()`
  * `delete_note()`
* **Config via env** (`TRILIUM_URL`, `TRILIUM_TOKEN`) using `pydantic-settings`.
* **Strongly-typed attributes** with `NoteAttribute` parsed from ETAPI responses.
* **Clear exceptions**: `TriliumAPIError`, `TriliumConnectionError`, `TriliumConfigError`.

> **Python**: 3.11+

## Quickstart

Set the required environment variables:

* `TRILIUM_TOKEN` – your ETAPI token (required)
* `TRILIUM_URL` – TriliumNext server (default: `http://localhost:8081`)

```python
from trilium_pydantic import (
    TriliumClient, TriliumConfig,
    CreateNoteRequest, UpdateNoteRequest, SearchRequest,
)

config = TriliumConfig()               # reads env / .env
client = TriliumClient(config)

# 1) Connectivity
print(client.test_connection())

# 2) Create
create = CreateNoteRequest(
    parent_note_id="root",
    title="Hello from trilium-pydantic",
    content="<p>Created via typed client</p>",
    note_type="text",
)
created = client.create_note(create)
note_id = created.note.note_id

# 3) Read
note = client.get_note(note_id)
print(note.title, note.note_type, len(note.attributes))

# 4) Update props & content
client.update_note(note_id, UpdateNoteRequest(title="Updated title"))
client.update_note_content(note_id, "<p>Updated content</p>")

# 5) Search (lightweight dict results)
results = client.search_notes(SearchRequest(search="Updated title", limit=5))
print(len(results.results), "hits")

# 6) Delete
client.delete_note(note_id)
```

## Models (selected)

* `CreateNoteRequest`, `UpdateNoteRequest`, `SearchRequest`
* `Note`, `NoteAttribute` (alias-aware; timestamps parsed to `datetime`)
* `AppInfo`, `SearchResult`, `CreateNoteResponse`, `ConnectionTest`

Example (attributes):

```python
for attr in note.attributes:
    print(attr.name, attr.value, attr.type, attr.is_inheritable)
```

## Exceptions

* `TriliumConnectionError` – no token / connection errors
* `TriliumAPIError` – ETAPI call failures
* `TriliumConfigError` – invalid configuration

## Project Layout

```
src/trilium_pydantic/
  client.py         # TriliumClient, wraps trilium_py.ETAPI
  config.py         # TriliumConfig (env-backed), ConnectionInfo
  models.py         # Pydantic request/response models (incl. NoteAttribute)
  exceptions.py     # Custom error types
  example_script.py # demo (rich UI)
tests/              # unit tests for attributes + client parsing
```

## Known quirks (v0.1.x)

**Absolute imports** in `client.py` / `example_script.py` should be made relative when used as an installed package.

```diff
- from config import TriliumConfig, ConnectionInfo
- from models import (...)
- from exceptions import ...
+ from .config import TriliumConfig, ConnectionInfo
+ from .models import (...)
+ from .exceptions import ...
```

`SearchResult.results` are raw dicts (ETAPI passthrough) rather than `Note` models by design (search often returns partial fields).

## Testing

```bash
pytest -v
```

## License

MIT

---

# quickstart - MVP example script

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#   "trilium-py>=1.2.0",
#   "pydantic>=2.5.0",
#   "pydantic-settings>=2.0.0",
#   "trilium-pydantic @ file://.",
# ]
# ///
from __future__ import annotations

import sys

from trilium_pydantic import (
    TriliumClient, TriliumConfig,
    CreateNoteRequest, UpdateNoteRequest, SearchRequest,
    TriliumAPIError, TriliumConnectionError,
)


def main() -> int:
    cfg = TriliumConfig()  # reads TRILIUM_URL/TRILIUM_TOKEN
    client = TriliumClient(cfg)

    # 1) Smoke test
    ct = client.test_connection()
    if not ct.success:
        print("Connection failed:", ct.error)
        return 1
    print("Connected to", ct.server_url, "version:", getattr(ct.app_info, "app_version", "?"))

    # 2) Create
    created = client.create_note(
        CreateNoteRequest(
            parent_note_id="root",
            title="QP Demo Note",
            content="<p>hello from trilium-pydantic</p>",
            note_type="text",
        )
    )
    note_id = created.note.note_id
    print("Created:", note_id)

    try:
        # 3) Read note + content
        note = client.get_note(note_id)
        content = client.get_note_content(note_id)
        print("Title:", note.title, "| type:", note.note_type, "| content length:", len(content))

        # 4) Update title + content
        client.update_note(note_id, UpdateNoteRequest(title="QP Demo Note (Updated)"))
        client.update_note_content(note_id, "<p>updated content</p>")
        print("Updated note", note_id)

        # 5) Search
        sr = client.search_notes(SearchRequest(search="QP Demo Note", limit=5))
        print("Search hits:", len(sr.results))

    finally:
        # 6) Cleanup
        if client.delete_note(note_id):
            print("Deleted:", note_id)
        else:
            print("Delete returned False for", note_id)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (TriliumConnectionError, TriliumAPIError) as e:
        print("Error:", e)
        sys.exit(1)
```

