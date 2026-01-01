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
    """Represents a Tana node to be created."""

    text: str
    children: Optional[List["TanaNode"]] = None
    tags: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API payload."""
        result: Dict[str, Any] = {"text": self.text}
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        if self.tags:
            result["tags"] = self.tags
        return result
