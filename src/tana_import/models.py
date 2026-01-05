"""Data models for ChatGPT exports and Tana events."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ChatGPTMessage:
    """Represents a single message in a ChatGPT conversation."""

    role: str
    content: Optional[str]
    create_time: Optional[float]


@dataclass
class ChatGPTConversation:
    """Represents a ChatGPT conversation."""

    title: str
    create_time: float
    messages: List[ChatGPTMessage]


@dataclass
class TanaNode:
    """Represents a Tana node to be created.

    Uses 'name' field to match supertag-mcp format used by tana-chat-sync.
    """

    name: str
    children: Optional[List["TanaNode"]] = None
    supertag: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API payload.

        Uses 'name' for node content and 'supertag' for tagging,
        matching the format used by supertag-mcp.
        """
        result: Dict[str, Any] = {"name": self.name}
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        if self.supertag:
            result["supertag"] = self.supertag
        return result
