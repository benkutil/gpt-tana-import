"""Tests for configuration module."""

import pytest

from tana_import.config import TanaConfig


def test_tana_config_from_env_success(mock_tana_config: None) -> None:
    """Test loading configuration from environment variables."""
    config = TanaConfig.from_env()
    assert config.api_endpoint == "https://api.tana.example/addToNodeV2"
    assert config.api_token == "test_token_123"
    assert config.inbox_node_id == "inbox_node_456"


def test_tana_config_from_env_missing_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that missing TANA_API_ENDPOINT raises ValueError."""
    monkeypatch.delenv("TANA_API_ENDPOINT", raising=False)
    monkeypatch.setenv("TANA_API_TOKEN", "test_token")
    monkeypatch.setenv("TANA_INBOX_NODE_ID", "inbox_id")

    with pytest.raises(ValueError, match="TANA_API_ENDPOINT"):
        TanaConfig.from_env()


def test_tana_config_from_env_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that missing TANA_API_TOKEN raises ValueError."""
    monkeypatch.setenv("TANA_API_ENDPOINT", "https://api.example.com")
    monkeypatch.delenv("TANA_API_TOKEN", raising=False)
    monkeypatch.setenv("TANA_INBOX_NODE_ID", "inbox_id")

    with pytest.raises(ValueError, match="TANA_API_TOKEN"):
        TanaConfig.from_env()


def test_tana_config_from_env_missing_inbox(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that missing TANA_INBOX_NODE_ID raises ValueError."""
    monkeypatch.setenv("TANA_API_ENDPOINT", "https://api.example.com")
    monkeypatch.setenv("TANA_API_TOKEN", "test_token")
    monkeypatch.delenv("TANA_INBOX_NODE_ID", raising=False)

    with pytest.raises(ValueError, match="TANA_INBOX_NODE_ID"):
        TanaConfig.from_env()


def test_tana_config_validate() -> None:
    """Test configuration validation."""
    config = TanaConfig(
        api_endpoint="https://api.example.com",
        api_token="token",
        inbox_node_id="inbox",
    )
    assert config.validate() is True

    invalid_config = TanaConfig(api_endpoint="", api_token="token", inbox_node_id="inbox")
    assert invalid_config.validate() is False
