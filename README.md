# trilium-pydantic

A modern, type-safe Python library for interacting with TriliumNext notes using Pydantic models and ETAPI.

## Overview

`trilium-pydantic` provides a clean, object-oriented interface to TriliumNext's ETAPI with full type safety through Pydantic models. Designed for local development workflows where simplicity and reliability matter most.

### Key Features

- **Type-Safe**: All API responses parsed into Pydantic models
- **Fail-Fast**: Comprehensive validation and error handling
- **Local-First**: Optimized for same-machine TriliumNext instances
- **Developer-Friendly**: Intuitive object-oriented design
- **Modern Python**: Built with latest Python features and best practices

## Installation

```bash
uv add trilium-pydantic
```

## Quick Start

### Configuration

Create a `.env` file in your project root:

```env
TRILIUM_URL=http://localhost:8080
TRILIUM_TOKEN=your_etapi_token_here
```

### Basic Usage

```python
from trilium_pydantic import TriliumClient
from trilium_pydantic.models import CreateNoteRequest

# Initialize client (auto-loads from .env)
client = TriliumClient()

# Create a note
note_request = CreateNoteRequest(
    parent_note_id="root",
    title="My First Note", 
    content="Hello TriliumNext!",
    note_type="text"
)
note = client.notes.create(note_request)
print(f"Created note: {note.note_id}")

# Get note
retrieved_note = client.notes.get(note.note_id)
print(f"Title: {retrieved_note.title}")

# Update note
retrieved_note.title = "Updated Title"
updated_note = client.notes.update(retrieved_note)

# Search notes
results = client.notes.search("python", limit=10)
for result in results.notes:
    print(f"{result.note_id}: {result.title}")
```

## API Design Philosophy

### Pydantic-First

All API interactions use strongly-typed Pydantic models:

```python
# Request models for input validation
create_request = CreateNoteRequest(
    parent_note_id="root",
    title="Code Snippet",
    content="print('hello world')",
    note_type="code", 
    mime="text/x-python"
)

# Response models with full type safety
note: Note = client.notes.create(create_request)
assert isinstance(note.created_date, datetime)
assert isinstance(note.child_note_ids, list)
```

### Fail-Fast Error Handling

The library validates inputs and fails immediately with clear error messages:

```python
try:
    # This will raise ValidationError before making API call
    bad_request = CreateNoteRequest(
        parent_note_id="",  # Invalid empty ID
        title="", # Invalid empty title
        note_type="invalid_type"  # Invalid type
    )
except ValidationError as e:
    logger.error(f"Invalid request: {e}")

try:
    note = client.notes.get("invalid_id")
except TriliumAPIError as e:
    logger.error(f"API error: {e.status_code} - {e.message}")
```

### Resource-Based Organization

API methods are organized by resource type:

```python
client.notes.create(...)      # Note operations
client.notes.get(...)
client.notes.update(...)
client.notes.delete(...)
client.notes.search(...)

client.branches.create(...)   # Hierarchy operations
client.branches.get(...)
client.branches.move(...)

client.attributes.create(...) # Attribute operations
client.attributes.get(...)
client.attributes.delete(...)
```

## MVP Roadmap

### ✅ Phase 1: Core Note Operations
- [x] Note CRUD (Create, Read, Update, Delete)
- [x] Note content management  
- [x] Basic search functionality
- [x] Type-safe request/response models
- [x] Environment-based configuration

### 🚧 Phase 2: Hierarchy Navigation
- [ ] Branch operations (create, move, delete)
- [ ] Tree traversal utilities
- [ ] Parent/child relationship management
- [ ] Note positioning and ordering

### 📋 Phase 3: Attribute Management  
- [ ] Label creation and management
- [ ] Relation handling
- [ ] Attribute inheritance
- [ ] Bulk attribute operations

### 🔮 Future Phases
- [ ] Attachment handling
- [ ] Export/import operations
- [ ] Backup management
- [ ] Advanced search queries
- [ ] Bulk operations
- [ ] Sync utilities

## Development Setup

### Prerequisites

- Python 3.11+
- UV package manager
- Local TriliumNext instance

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/trilium-pydantic.git
cd trilium-pydantic

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit with your TriliumNext details
# TRILIUM_URL=http://localhost:8080
# TRILIUM_TOKEN=your_token_here
# LOG_LEVEL=INFO
```

### Getting Your ETAPI Token

```python
# Quick script to generate token
#!/usr/bin/env python3
"""Get ETAPI token for TriliumNext."""

import requests
from getpass import getpass

server_url = "http://localhost:8080"
password = getpass("TriliumNext password: ")

response = requests.post(
    f"{server_url}/etapi/auth/login",
    json={"password": password}
)

if response.status_code == 200:
    token = response.json()["authToken"]
    print(f"Your ETAPI token: {token}")
    print("Add this to your .env file as TRILIUM_TOKEN")
else:
    print(f"Login failed: {response.status_code}")
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=trilium_pydantic

# Run specific test file
uv run pytest tests/test_notes.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code  
uv run ruff check

# Type checking
uv run mypy src/
```

## Architecture

### Project Structure

```
trilium-pydantic/
├── src/trilium_pydantic/
│   ├── __init__.py
│   ├── client.py              # Main TriliumClient
│   ├── config.py              # Configuration management
│   ├── exceptions.py          # Custom exceptions
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   ├── notes.py          # Note-related models
│   │   ├── branches.py       # Branch-related models
│   │   ├── attributes.py     # Attribute-related models
│   │   └── common.py         # Shared models
│   ├── resources/            # API resource classes
│   │   ├── __init__.py
│   │   ├── notes.py          # Notes resource
│   │   ├── branches.py       # Branches resource  
│   │   └── attributes.py     # Attributes resource
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── http.py           # HTTP client utilities
│       └── logging.py        # Logging configuration
├── tests/                    # Test suite
├── examples/                 # Usage examples
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

### Core Dependencies

- **pydantic** `^2.5.0` - Data validation and parsing
- **httpx** `^0.25.0` - Async HTTP client
- **python-dotenv** `^1.0.0` - Environment management
- **structlog** `^23.0.0` - Structured logging

## Examples

See the `examples/` directory for complete usage examples:

- `basic_crud.py` - Note creation, reading, updating, deletion
- `search_notes.py` - Advanced search patterns
- `hierarchy_management.py` - Working with note trees
- `batch_operations.py` - Bulk note operations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes following the code style guidelines
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/trilium-pydantic/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/trilium-pydantic/discussions)
- **TriliumNext Docs**: [Official Documentation](https://github.com/TriliumNext/Notes)

---

*Built with ❤️ for the TriliumNext community*