"""Tests for parser module."""

from pathlib import Path
from typing import Any, Dict

import pytest

from tana_import.parser import parse_conversation, parse_export_file


def test_parse_export_file_success(temp_chatgpt_file: Path) -> None:
    """Test parsing a valid ChatGPT export file."""
    conversations = parse_export_file(temp_chatgpt_file)
    assert isinstance(conversations, list)
    assert len(conversations) == 1
    assert conversations[0].title == "Test Conversation"
    assert len(conversations[0].messages) > 0


def test_parse_export_file_not_found() -> None:
    """Test parsing a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_export_file(Path("/nonexistent/file.json"))


def test_parse_conversation(sample_chatgpt_export: Dict[str, Any]) -> None:
    """Test parsing a single conversation."""
    conversation = parse_conversation(sample_chatgpt_export)
    assert conversation.title == "Test Conversation"
    assert conversation.create_time == 1704153000.0
    assert len(conversation.messages) == 2  # user and assistant messages
    assert conversation.messages[0].role == "user"
    assert conversation.messages[1].role == "assistant"
