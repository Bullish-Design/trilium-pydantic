#!/usr/bin/env python3
"""Complete example of trilium-pydantic usage.

This script demonstrates:
1. Connection setup and testing
2. Basic CRUD operations with type safety
3. Error handling
4. Real-world usage patterns

Usage:
    # Set environment variables first:
    export TRILIUM_URL="http://localhost:8080"
    export TRILIUM_TOKEN="your_etapi_token_here"

    # Then run:
    uv run example.py
"""
# /// script
# dependencies = [
#   "trilium-py>=1.2.0",
#   "pydantic>=2.5.0",
#   "pydantic-settings>=2.0.0",
#   "rich>=13.0.0",
# ]
# ///

from __future__ import annotations

import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import our trilium-pydantic components
# (In real usage, these would be: from trilium_pydantic import ...)
from config import TriliumConfig
from client import TriliumClient
from models import CreateNoteRequest, UpdateNoteRequest, SearchRequest
from exceptions import TriliumAPIError, TriliumConnectionError

console = Console()

test_note_id = "P2dGbFt5Xpx1"


def display_connection_info(client: TriliumClient) -> None:
    """Display connection information in a formatted panel."""
    conn_info = client.get_connection_info()

    status_color = "green" if conn_info.is_connected else "red"
    status_text = "✅ Connected" if conn_info.is_connected else "❌ Disconnected"

    info_text = [
        f"[bold]Server URL:[/bold] {conn_info.server_url}",
        f"[bold]Token:[/bold] {conn_info.token_preview}",
        f"[bold]Status:[/bold] [{status_color}]{status_text}[/{status_color}]",
    ]

    if conn_info.app_version:
        info_text.append(f"[bold]Version:[/bold] {conn_info.app_version}")

    console.print(
        Panel.fit(
            "\n".join(info_text),
            title="TriliumNext Connection",
            border_style=status_color,
        )
    )


def demonstrate_basic_operations(client: TriliumClient) -> Optional[str]:
    """Demonstrate basic CRUD operations with notes.

    Returns:
        Note ID of created note, or None if failed.
    """
    console.print("\n[bold cyan]Demonstrating Basic Operations[/bold cyan]")

    try:
        # 1. Create a new note
        console.print("📝 Creating new note...")
        create_request = CreateNoteRequest(
            parent_note_id="root",
            title="Test Note from Pydantic Client",
            content="<p>This note was created using the Pydantic wrapper!</p>",
            note_type="text",
        )

        create_response = client.create_note(create_request)
        note_id = create_response.note.note_id
        console.print(f"✅ Created note with ID: [green]{note_id}[/green]")

        # 2. Read the note back
        console.print("👀 Reading note...")
        note = client.get_note(test_note_id)
        console.print(f"📖 Title: [blue]{note.title}[/blue]")
        console.print(f"📄 Type: [yellow]{note.note_type}[/yellow]")
        # 2.1 Show attributes (if any)
        if note.attributes:
            console.print("🏷️  Attributes:")
            for a in note.attributes:
                console.print(f"  • {a.name} = {a.value} (type={a.type})")
        else:
            console.print("🏷️  No attributes on this note")

        # 3. Get note content
        content = client.get_note_content(note_id)
        console.print(
            f"📝 Content length: [magenta]{len(content)} characters[/magenta]"
        )

        # 4. Update the note
        console.print("✏️  Updating note...")
        update_request = UpdateNoteRequest(title="Updated Test Note")
        updated_note = client.update_note(note_id, update_request)
        console.print(f"✅ Updated title: [blue]{updated_note.title}[/blue]")

        # 5. Update content
        new_content = "<p>This content was updated via the Pydantic client!</p>"
        client.update_note_content(note_id, new_content)
        console.print("✅ Updated note content")

        return note_id

    except TriliumAPIError as e:
        console.print(f"[red]❌ API Error: {e}[/red]")
        return None


def demonstrate_search(client: TriliumClient) -> None:
    """Demonstrate search functionality."""
    console.print("\n[bold cyan]Demonstrating Search[/bold cyan]")

    try:
        # Search for our test note
        search_request = SearchRequest(search="Test Note", limit=5)

        results = client.search_notes(search_request)

        if results.results:
            console.print(f"🔍 Found {len(results.results)} notes:")

            table = Table(title="Search Results")
            table.add_column("Note ID", style="green")
            table.add_column("Title", style="blue")

            for result in results.results[:3]:  # Show first 3
                table.add_row(result.get("noteId", "N/A"), result.get("title", "N/A"))

            console.print(table)
        else:
            console.print("🔍 No notes found")

    except TriliumAPIError as e:
        console.print(f"[red]❌ Search Error: {e}[/red]")


def cleanup_test_note(client: TriliumClient, note_id: str) -> None:
    """Clean up the test note."""
    console.print(f"\n[bold yellow]Cleaning up test note {note_id}[/bold yellow]")

    try:
        success = client.delete_note(note_id)
        if success:
            console.print("✅ Test note deleted successfully")
        else:
            console.print("⚠️  Note deletion returned False")
    except TriliumAPIError as e:
        console.print(f"[red]❌ Cleanup Error: {e}[/red]")


def main() -> int:
    """Main demonstration function."""
    console.print("[bold green]TriliumNext Pydantic Client Demo[/bold green]")

    try:
        # 1. Initialize configuration
        console.print("\n[bold]Step 1: Loading Configuration[/bold]")
        config = TriliumConfig()

        if not config.is_configured():
            console.print(
                Panel.fit(
                    "[red]❌ Configuration Error[/red]\n\n"
                    "Please set environment variables:\n"
                    "• TRILIUM_URL (e.g., http://localhost:8080)\n"
                    "• TRILIUM_TOKEN (your ETAPI token)\n\n"
                    "Or create a .env file with these values.",
                    title="Missing Configuration",
                    border_style="red",
                )
            )
            return 1

        # 2. Initialize client
        console.print("✅ Configuration loaded")
        console.print("\n[bold]Step 2: Initializing Client[/bold]")
        client = TriliumClient(config)

        # 3. Test connection
        console.print("\n[bold]Step 3: Testing Connection[/bold]")
        connection_test = client.test_connection()

        if not connection_test.success:
            console.print(
                Panel.fit(
                    f"[red]❌ Connection Failed[/red]\n\n"
                    f"Error: {connection_test.error}\n\n"
                    "Please check:\n"
                    "• Server URL is correct\n"
                    "• ETAPI token is valid\n"
                    "• TriliumNext server is running",
                    title="Connection Error",
                    border_style="red",
                )
            )
            return 1

        # 4. Display connection info
        display_connection_info(client)

        # 5. Demonstrate operations
        test_note_id = demonstrate_basic_operations(client)

        # 6. Demonstrate search
        demonstrate_search(client)

        # 7. Cleanup
        if test_note_id:
            cleanup_test_note(client, test_note_id)

        console.print("\n[bold green]🎉 Demo completed successfully![/bold green]")
        return 0

    except TriliumConnectionError as e:
        console.print(f"[red]❌ Connection Error: {e}[/red]")
        return 1
    except Exception as e:
        console.print(f"[red]❌ Unexpected Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
