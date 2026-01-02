"""Tests for converter module."""

from tana_import.converter import conversation_to_tana_node, create_tana_events
from tana_import.models import ChatGPTConversation


def test_conversation_to_tana_node() -> None:
    """Test converting a conversation to a Tana node."""
    conversation = ChatGPTConversation(title="Test", create_time=1704153000.0, messages=[])
    node = conversation_to_tana_node(conversation)
    assert "ChatGPT conversation" in node.text
    assert "#ai-chat" in (node.tags or [])


def test_create_tana_events() -> None:
    """Test creating Tana API events from conversations."""
    conversations = [
        ChatGPTConversation(title="Test 1", create_time=1704153000.0, messages=[]),
        ChatGPTConversation(title="Test 2", create_time=1704153100.0, messages=[]),
    ]
    events = create_tana_events(conversations, "inbox_123")
    # Placeholder test - implementation pending
    assert isinstance(events, list)
