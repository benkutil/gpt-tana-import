"""ChatGPT export JSON parser."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from tana_import.models import ChatGPTConversation, ChatGPTMessage


def parse_export_file(file_path: Path) -> List[ChatGPTConversation]:
    """Parse a ChatGPT export JSON file.

    Args:
        file_path: Path to the ChatGPT export JSON file.

    Returns:
        List of ChatGPTConversation objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle both single conversation dict and list of conversations
    if isinstance(data, dict):
        conversations_data = [data]
    elif isinstance(data, list):
        conversations_data = data
    else:
        raise ValueError("Invalid ChatGPT export format: expected dict or list")

    conversations = []
    for conv_data in conversations_data:
        conversation = parse_conversation(conv_data)
        conversations.append(conversation)

    return conversations


def parse_conversation(conv_data: Dict[str, Any]) -> ChatGPTConversation:
    """Parse a single conversation from ChatGPT export data.

    Args:
        conv_data: Dictionary containing conversation data.

    Returns:
        ChatGPTConversation object.
    """
    title = conv_data.get("title", "Untitled")
    create_time = conv_data.get("create_time", 0.0)
    mapping = conv_data.get("mapping", {})

    # Linearize the message tree by following the path from root
    messages = _linearize_messages(mapping)

    return ChatGPTConversation(
        title=title,
        create_time=create_time,
        messages=messages,
    )


def _linearize_messages(mapping: Dict[str, Any]) -> List[ChatGPTMessage]:
    """Linearize the message tree into a chronological list.

    Args:
        mapping: The mapping dictionary from ChatGPT export containing message nodes.

    Returns:
        List of ChatGPTMessage objects in chronological order.
    """
    messages: List[ChatGPTMessage] = []

    # Start from the root node and traverse the tree
    current_id: Optional[str] = "root"
    visited = set()

    while current_id and current_id not in visited:
        visited.add(current_id)
        node = mapping.get(current_id)

        if not node:
            break

        # Extract message if it exists (root node has no message)
        message_data = node.get("message")
        if message_data:
            message = _parse_message(message_data)
            if message:
                messages.append(message)

        # Follow the first child (main conversation path)
        children = node.get("children", [])
        if children:
            current_id = children[0]
        else:
            current_id = None

    return messages


def _parse_message(message_data: Dict[str, Any]) -> Optional[ChatGPTMessage]:
    """Parse a single message from message data.

    Args:
        message_data: Dictionary containing message data.

    Returns:
        ChatGPTMessage object or None if message should be skipped.
    """
    author = message_data.get("author", {})
    role = author.get("role", "unknown")

    content_data = message_data.get("content", {})
    content_parts = content_data.get("parts", [])

    # Join content parts into a single string
    content = "\n".join(str(part) for part in content_parts if part)

    create_time = message_data.get("create_time")

    # Skip messages with no content
    if not content:
        return None

    return ChatGPTMessage(
        role=role,
        content=content if content else None,
        create_time=create_time,
    )
