"""Tests for API client module."""

import requests
from pytest_mock import MockerFixture

from tana_import.api_client import TanaAPIClient
from tana_import.config import TanaConfig


def test_tana_api_client_init() -> None:
    """Test TanaAPIClient initialization."""
    config = TanaConfig(
        api_endpoint="https://api.example.com",
        api_token="test_token",
        inbox_node_id="inbox_id",
    )
    client = TanaAPIClient(config)
    assert client.config == config
    assert "Bearer test_token" in client.session.headers["Authorization"]


def test_tana_api_client_send_events(mocker: MockerFixture) -> None:
    """Test sending events to Tana API."""
    config = TanaConfig(
        api_endpoint="https://api.example.com",
        api_token="test_token",
        inbox_node_id="inbox_id",
    )
    client = TanaAPIClient(config)

    # Mock the response
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 200
    mocker.patch.object(client.session, "post", return_value=mock_response)

    events = [{"type": "test", "data": "example"}]
    response = client.send_events(events)

    assert response.status_code == 200
    client.session.post.assert_called_once_with(config.api_endpoint, json={"events": events})
