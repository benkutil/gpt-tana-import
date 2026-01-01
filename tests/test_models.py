"""Tests for data models."""

from tana_import.models import ChatGPTConversation, ChatGPTMessage, TanaNode


def test_chatgpt_message_creation() -> None:
    """Test ChatGPTMessage creation."""
    message = ChatGPTMessage(role="user", content="Hello", create_time=1704153000.0)
    assert message.role == "user"
    assert message.content == "Hello"
    assert message.create_time == 1704153000.0


def test_chatgpt_conversation_creation() -> None:
    """Test ChatGPTConversation creation."""
    messages = [
        ChatGPTMessage(role="user", content="Hello", create_time=1704153000.0),
        ChatGPTMessage(role="assistant", content="Hi!", create_time=1704153030.0),
    ]
    conversation = ChatGPTConversation(title="Test", create_time=1704153000.0, messages=messages)
    assert conversation.title == "Test"
    assert len(conversation.messages) == 2


def test_tana_node_to_dict() -> None:
    """Test TanaNode to_dict conversion."""
    child_node = TanaNode(text="Child")
    parent_node = TanaNode(text="Parent", children=[child_node], tags=["#test"])

    result = parent_node.to_dict()
    assert result["text"] == "Parent"
    assert result["tags"] == ["#test"]
    assert len(result["children"]) == 1
    assert result["children"][0]["text"] == "Child"


def test_tana_node_without_children_or_tags() -> None:
    """Test TanaNode to_dict without optional fields."""
    node = TanaNode(text="Simple")
    result = node.to_dict()
    assert result == {"text": "Simple"}
