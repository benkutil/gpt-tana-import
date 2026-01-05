"""Tests for converter module."""

from tana_import.converter import conversation_to_tana_node, create_tana_events
from tana_import.models import ChatGPTConversation, ChatGPTMessage


def test_conversation_to_tana_node() -> None:
    """Test converting a conversation to a Tana node."""
    messages = [
        ChatGPTMessage(role="user", content="Hello", create_time=1704153000.0),
        ChatGPTMessage(role="assistant", content="Hi there!", create_time=1704153030.0),
    ]
    conversation = ChatGPTConversation(title="Test", create_time=1704153000.0, messages=messages)
    node = conversation_to_tana_node(conversation)
    assert "ChatGPT conversation" in node.name
    assert node.supertag == "ai-chat"
    assert node.children is not None
    assert len(node.children) == 1  # One prompt node
    assert node.children[0].name == "Hello"
    assert node.children[0].children is not None
    assert len(node.children[0].children) == 1  # One response node
    assert node.children[0].children[0].name == "Hi there!"


def test_create_tana_events() -> None:
    """Test creating Tana API events from conversations."""
    conversations = [
        ChatGPTConversation(title="Test 1", create_time=1704153000.0, messages=[]),
        ChatGPTConversation(title="Test 2", create_time=1704153100.0, messages=[]),
    ]
    events = create_tana_events(conversations, "inbox_123")
    assert isinstance(events, list)
    assert len(events) == 2
    assert events[0]["target"] == "inbox_123"
    assert events[0]["supertag"] == "ai-chat"
    assert "name" in events[0]
