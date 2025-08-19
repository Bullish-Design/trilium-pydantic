"""Main TriliumNext client."""

from __future__ import annotations

import httpx

from .config import TriliumConfig, load_config
from .exceptions import TriliumAPIError, TriliumConfigError
from .models.notes import AppInfo
from .resources.notes import NotesResource


class TriliumClient:
    """Main client for TriliumNext ETAPI."""
    
    def __init__(self, config: TriliumConfig | None = None):
        """Initialize the client."""
        self.config = config or load_config()
        
        if not self.config.token:
            raise TriliumConfigError(
                "No API token provided. Set TRILIUM_TOKEN in environment "
                "or .env file."
            )
        
        self._http_client = httpx.Client(
            base_url=self.config.url,
            timeout=30.0,
        )
        
        # Initialize resource handlers
        self.notes = NotesResource(self)
    
    def _get_headers(self) -> dict[str, str]:
        """Get authorization headers."""
        return {"Authorization": self.config.token}
    
    def app_info(self) -> AppInfo:
        """Get application information."""
        try:
            response = self._http_client.get(
                "/etapi/app-info",
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return AppInfo.model_validate(response.json())
        except httpx.HTTPError as e:
            raise TriliumAPIError(f"Failed to get app info: {e}")
    
    def test_connection(self) -> bool:
        """Test if connection to TriliumNext is working."""
        try:
            self.app_info()
            return True
        except Exception:
            return False
    
    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()
    
    def __enter__(self) -> TriliumClient:
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
