"""Pytest configuration and fixtures."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def sample_chatgpt_export() -> Dict[str, Any]:
    """Sample ChatGPT export data matching real export format."""
    return {
        "title": "Test Conversation",
        "create_time": 1704153000.0,
        "update_time": 1704153600.0,
        "mapping": {
            "client-created-root": {
                "id": "client-created-root",
                "message": None,
                "parent": None,
                "children": ["aaaaaa01-0000-0000-0000-000000000001"],
            },
            "aaaaaa01-0000-0000-0000-000000000001": {
                "id": "aaaaaa01-0000-0000-0000-000000000001",
                "message": {
                    "id": "aaaaaa01-0000-0000-0000-000000000001",
                    "author": {"role": "system", "name": None, "metadata": {}},
                    "create_time": None,
                    "update_time": None,
                    "content": {"content_type": "text", "parts": [""]},
                    "status": "finished_successfully",
                    "end_turn": True,
                    "weight": 0.0,
                    "metadata": {"is_visually_hidden_from_conversation": True},
                    "recipient": "all",
                    "channel": None,
                },
                "parent": "client-created-root",
                "children": ["aaaaaa01-0000-0000-0000-000000000002"],
            },
            "aaaaaa01-0000-0000-0000-000000000002": {
                "id": "aaaaaa01-0000-0000-0000-000000000002",
                "message": {
                    "id": "aaaaaa01-0000-0000-0000-000000000002",
                    "author": {"role": "user", "name": None, "metadata": {}},
                    "create_time": 1704153000.0,
                    "update_time": None,
                    "content": {"content_type": "text", "parts": ["Hello, world!"]},
                    "status": "finished_successfully",
                    "end_turn": None,
                    "weight": 1.0,
                    "metadata": {},
                    "recipient": "all",
                    "channel": None,
                },
                "parent": "aaaaaa01-0000-0000-0000-000000000001",
                "children": ["aaaaaa01-0000-0000-0000-000000000003"],
            },
            "aaaaaa01-0000-0000-0000-000000000003": {
                "id": "aaaaaa01-0000-0000-0000-000000000003",
                "message": {
                    "id": "aaaaaa01-0000-0000-0000-000000000003",
                    "author": {"role": "assistant", "name": None, "metadata": {}},
                    "create_time": 1704153030.0,
                    "update_time": None,
                    "content": {"content_type": "text", "parts": ["Hi! How can I help you?"]},
                    "status": "finished_successfully",
                    "end_turn": True,
                    "weight": 1.0,
                    "metadata": {"finish_details": {"type": "stop"}},
                    "recipient": "all",
                    "channel": None,
                },
                "parent": "aaaaaa01-0000-0000-0000-000000000002",
                "children": [],
            },
        },
    }


@pytest.fixture
def temp_chatgpt_file(tmp_path: Path, sample_chatgpt_export: Dict[str, Any]) -> Path:
    """Create a temporary ChatGPT export file."""
    file_path = tmp_path / "chatgpt_export.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([sample_chatgpt_export], f)
    return file_path


@pytest.fixture
def mock_tana_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock Tana configuration environment variables."""
    monkeypatch.setenv("TANA_API_ENDPOINT", "https://api.tana.example/addToNodeV2")
    monkeypatch.setenv("TANA_API_TOKEN", "test_token_123")
    monkeypatch.setenv("TANA_INBOX_NODE_ID", "inbox_node_456")
