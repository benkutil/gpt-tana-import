"""Tana API client."""

from typing import Any, Dict, List

import requests

from tana_import.config import TanaConfig


class TanaAPIClient:
    """Client for interacting with the Tana Input API."""

    def __init__(self, config: TanaConfig) -> None:
        """Initialize the Tana API client.

        Args:
            config: TanaConfig with API credentials and endpoint.
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {config.api_token}",
                "Content-Type": "application/json",
            }
        )

    def send_events(self, events: List[Dict[str, Any]]) -> requests.Response:
        """Send events to the Tana API.

        Args:
            events: List of event dictionaries to send.

        Returns:
            Response from the Tana API.

        Raises:
            requests.RequestException: If the request fails.
        """
        payload = {"events": events}
        response = self.session.post(self.config.api_endpoint, json=payload)
        response.raise_for_status()
        return response
