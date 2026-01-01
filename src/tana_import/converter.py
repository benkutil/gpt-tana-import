"""Convert ChatGPT conversations to Tana events."""

from datetime import datetime
from typing import List

from tana_import.models import ChatGPTConversation, TanaNode


def conversation_to_tana_node(
    conversation: ChatGPTConversation, timezone_name: str = "UTC"  # pylint: disable=unused-argument
) -> TanaNode:
    """Convert a ChatGPT conversation to a Tana node.

    Args:
        conversation: The ChatGPT conversation to convert.
        timezone_name: Timezone name for timestamp conversion.

    Returns:
        TanaNode representing the conversation.
    """
    # Format timestamp as "ChatGPT conversation - YYYY-MM-DD HH:MM"
    dt = datetime.fromtimestamp(conversation.create_time)
    title = f"ChatGPT conversation - {dt.strftime('%Y-%m-%d %H:%M')}"

    # Placeholder implementation
    return TanaNode(text=title, tags=["#ai-chat"], children=[])


def create_tana_events(
    conversations: List[ChatGPTConversation],  # pylint: disable=unused-argument
    inbox_node_id: str,  # pylint: disable=unused-argument
) -> List[dict]:
    """Create Tana API events from conversations.

    Args:
        conversations: List of ChatGPT conversations.
        inbox_node_id: The Tana node ID where conversations should be placed.

    Returns:
        List of Tana API event dictionaries.
    """
    # Placeholder implementation
    return []
