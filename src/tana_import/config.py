"""Configuration handling for Tana API."""

import os
from dataclasses import dataclass


@dataclass
class TanaConfig:
    """Configuration for Tana API connection."""

    api_endpoint: str
    api_token: str
    inbox_node_id: str

    @classmethod
    def from_env(cls) -> "TanaConfig":
        """Load configuration from environment variables.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        api_endpoint = os.getenv("TANA_API_ENDPOINT")
        api_token = os.getenv("TANA_API_TOKEN")
        inbox_node_id = os.getenv("TANA_INBOX_NODE_ID")

        missing = []
        if not api_endpoint:
            missing.append("TANA_API_ENDPOINT")
        if not api_token:
            missing.append("TANA_API_TOKEN")
        if not inbox_node_id:
            missing.append("TANA_INBOX_NODE_ID")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                "Please set these variables before running the tool."
            )

        # At this point we know all values are non-None
        assert api_endpoint is not None
        assert api_token is not None
        assert inbox_node_id is not None

        return cls(
            api_endpoint=api_endpoint,
            api_token=api_token,
            inbox_node_id=inbox_node_id,
        )

    def validate(self) -> bool:
        """Validate that all configuration values are set.

        Returns:
            True if all values are non-empty, False otherwise.
        """
        return bool(self.api_endpoint and self.api_token and self.inbox_node_id)
