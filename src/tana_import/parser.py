"""ChatGPT export JSON parser."""

import json
from pathlib import Path
from typing import List

from tana_import.models import ChatGPTConversation


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
    # Validate JSON format by attempting to load
    # TODO: Implement actual parsing logic
    with open(file_path, "r", encoding="utf-8") as f:
        _ = json.load(f)

    # Placeholder implementation - will be replaced with actual parsing
    return []


def parse_conversation(conv_data: dict) -> ChatGPTConversation:
    """Parse a single conversation from ChatGPT export data.

    Args:
        conv_data: Dictionary containing conversation data.

    Returns:
        ChatGPTConversation object.
    """
    # Placeholder implementation
    return ChatGPTConversation(
        title=conv_data.get("title", "Untitled"),
        create_time=conv_data.get("create_time", 0.0),
        messages=[],
    )
