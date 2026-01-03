"""Pytest configuration and fixtures."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def sample_chatgpt_export() -> Dict[str, Any]:
    """Sample ChatGPT export data."""
    return {
        "title": "Test Conversation",
        "create_time": 1704153000.0,
        "update_time": 1704153600.0,
        "mapping": {
            "root": {
                "id": "root",
                "message": None,
                "parent": None,
                "children": ["msg1"],
            },
            "msg1": {
                "id": "msg1",
                "message": {
                    "id": "msg1",
                    "author": {"role": "user"},
                    "content": {"content_type": "text", "parts": ["Hello, world!"]},
                    "create_time": 1704153000.0,
                },
                "parent": "root",
                "children": ["msg2"],
            },
            "msg2": {
                "id": "msg2",
                "message": {
                    "id": "msg2",
                    "author": {"role": "assistant"},
                    "content": {"content_type": "text", "parts": ["Hi! How can I help you?"]},
                    "create_time": 1704153030.0,
                },
                "parent": "msg1",
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
