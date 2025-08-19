#!/usr/bin/env python3
"""Test TriliumNext connection and basic operations."""
# /// script
# dependencies = [
#   "pydantic>=2.5.0",
#   "pydantic-settings>=2.0.0",
#   "httpx>=0.25.0",
#   "python-dotenv>=1.0.0",
#   "structlog>=23.0.0",
#   "rich>=13.0.0",
# ]
# ///

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from trilium_pydantic import TriliumClient
from trilium_pydantic.exceptions import TriliumConfigError, TriliumAPIError
from trilium_pydantic.models import CreateNoteRequest

console = Console()


def test_connection() -> bool:
    """Test basic connection to TriliumNext."""
    try:
        with TriliumClient() as client:
            # Test connection
            console.print(f"\nChecking Client Connection...\n")
            app_info = client.app_info()
            console.print(
                Panel.fit(
                    f"[green]✓ Connected to TriliumNext[/green]\n"
                    f"Version: {app_info.app_version}\n"
                    f"Database: v{app_info.db_version}",
                    title="Connection Successful",
                    border_style="green",
                )
            )
            console.print(f"\nCreating Test Note...\n")
            # Test note operations
            note_request = CreateNoteRequest(
                parent_note_id="root",
                title="Test Connection Note",
                content="This note was created by trilium-pydantic test.",
                note_type="text",
            )

            note = client.notes.create(note_request)
            console.print(f"[blue]Created note:[/blue] {note.note_id}")

            # Retrieve and verify
            retrieved = client.notes.get(note.note_id)
            console.print(f"[blue]Retrieved note:[/blue] {retrieved.title}")

            # Clean up
            client.notes.delete(note.note_id)
            console.print(f"[blue]Deleted test note[/blue]")

            return True

    except TriliumConfigError as e:
        console.print(
            Panel.fit(
                f"[red]Configuration Error:[/red] {e}\n\n"
                "Please create a .env file with:\n"
                "TRILIUM_URL=http://localhost:8080\n"
                "TRILIUM_TOKEN=your_token_here",
                title="Configuration Required",
                border_style="yellow",
            )
        )
        return False

    except TriliumAPIError as e:
        console.print(
            Panel.fit(
                f"[red]API Error:[/red] {e}\n\n"
                "Check that TriliumNext is running and token is valid.",
                title="Connection Failed",
                border_style="red",
            )
        )
        return False

    except Exception as e:
        console.print(
            Panel.fit(
                f"[red]Unexpected Error:[/red] {e}",
                title="Test Failed",
                border_style="red",
            )
        )
        return False


if __name__ == "__main__":
    console.print("[bold]Testing trilium-pydantic connection...[/bold]")
    success = test_connection()
    sys.exit(0 if success else 1)
