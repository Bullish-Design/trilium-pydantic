#!/usr/bin/env python3
"""Debug TriliumNext connection issues."""
# /// script
# dependencies = [
#   "httpx>=0.25.0",
#   "python-dotenv>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///

from __future__ import annotations

import base64
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()


def debug_connection():
    """Debug connection to TriliumNext."""
    # Load environment
    load_dotenv()

    import os

    url = os.getenv("TRILIUM_URL", "http://localhost:8081")
    token = os.getenv("TRILIUM_TOKEN", "")

    if not token:
        console.print("[red]No TRILIUM_TOKEN found in environment[/red]")
        return False

    console.print(f"Testing connection to: {url}")
    console.print(f"Using token: {'*' * 8}...{token[-4:]}")

    with httpx.Client() as client:
        # Test 1: Standard ETAPI format (per docs)
        console.print("\n[bold]Test 1: Standard ETAPI Auth[/bold]")
        try:
            response = client.get(
                f"{url}/etapi/app-info", headers={"Authorization": token}
            )
            console.print(f"Status: {response.status_code}")
            if response.status_code == 200:
                console.print("[green]✓ Standard auth working[/green]")
                console.print(f"Response: {response.json()}")
                return True
            else:
                console.print(f"Response: {response.text}")

        except Exception as e:
            console.print(f"[red]Connection failed: {e}[/red]")

        # Test 2: Basic Auth format (since v0.56)
        console.print("\n[bold]Test 2: Basic Auth Format[/bold]")
        try:
            # Create basic auth: base64("etapi:token")
            basic_auth = base64.b64encode(f"etapi:{token}".encode()).decode()
            response = client.get(
                f"{url}/etapi/app-info",
                headers={"Authorization": f"Basic {basic_auth}"},
            )
            console.print(f"Status: {response.status_code}")
            if response.status_code == 200:
                console.print("[green]✓ Basic auth working[/green]")
                console.print(f"Response: {response.json()}")
                return True
            else:
                console.print(f"Response: {response.text}")

        except Exception as e:
            console.print(f"Error: {e}")

        # Test 3: Check if server is reachable
        console.print("\n[bold]Test 3: Server Connectivity[/bold]")
        try:
            response = client.get(f"{url}/etapi/app-info")
            console.print(f"Status without auth: {response.status_code}")
            console.print(f"Response: {response.text[:200]}")
        except Exception as e:
            console.print(f"[red]Server unreachable: {e}[/red]")

    return False


if __name__ == "__main__":
    success = debug_connection()
    sys.exit(0 if success else 1)
