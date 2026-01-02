"""Convert ChatGPT conversations to Tana events."""

from datetime import datetime
from typing import Any, Dict, List, Optional

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

    # Group messages into prompt-response pairs
    children: List[TanaNode] = []
    current_prompt: Optional[TanaNode] = None

    for message in conversation.messages:
        if message.role == "user":
            # Create a new prompt node
            current_prompt = TanaNode(text=message.content or "", children=[])
            children.append(current_prompt)
        elif message.role in ("assistant", "tool"):
            # Add as child of current prompt
            if current_prompt:
                response_node = TanaNode(text=message.content or "")
                if current_prompt.children is None:
                    current_prompt.children = []
                current_prompt.children.append(response_node)

    return TanaNode(text=title, tags=["#ai-chat"], children=children)


def create_tana_events(
    conversations: List[ChatGPTConversation],
    inbox_node_id: str,
) -> List[Dict[str, Any]]:
    """Create Tana API events from conversations.

    Args:
        conversations: List of ChatGPT conversations.
        inbox_node_id: The Tana node ID where conversations should be placed.

    Returns:
        List of Tana API event dictionaries.
    """
    events: List[Dict[str, Any]] = []

    for conversation in conversations:
        # Convert conversation to node structure
        conv_node = conversation_to_tana_node(conversation)

        # Create an event for this conversation
        event = {
            "type": "addNode",
            "nodeId": inbox_node_id,
            "node": conv_node.to_dict(),
        }
        events.append(event)

    return events
