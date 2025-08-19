"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest

from trilium_pydantic import TriliumClient
from trilium_pydantic.exceptions import TriliumConfigError


@pytest.fixture
def trilium_client():
    """Provide a TriliumClient for integration tests."""
    try:
        with TriliumClient() as client:
            yield client
    except TriliumConfigError:
        pytest.skip("TriliumNext not configured - set TRILIUM_TOKEN in .env")


@pytest.fixture
def skip_if_no_trilium():
    """Skip test if TriliumNext is not available."""
    try:
        TriliumClient()
    except TriliumConfigError:
        pytest.skip("TriliumNext not configured")
