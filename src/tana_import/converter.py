"""Convert ChatGPT conversations to Tana events."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from tana_import.models import ChatGPTConversation, TanaNode

# ChatGPT uses private use unicode characters for file citations
PRIVATE_USE_PATTERN = re.compile(r"[\ue000-\uf8ff]")
# Pattern for ChatGPT file citation markers like fileciteturn0file0
FILE_CITE_PATTERN = re.compile(r"filecite\w+")
# Pattern for parsed text page markers
PARSED_TEXT_PATTERN = re.compile(r"<PARSED TEXT FOR PAGE:[^>]+>")
# Markdown header pattern (captures level and title)
MARKDOWN_HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
# Bullet pattern
BULLET_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")

# Patterns for tool/system instructions that should be skipped
TOOL_INSTRUCTION_PATTERNS = [
    "Make sure to include",
    "Remember you have access to rendered images",
    "The file contents provided above are truncated",
]

# Max length for a single node name
MAX_NODE_LENGTH = 4000
# Maximum payload size for Tana API
MAX_PAYLOAD_SIZE = 4800


def is_tool_instruction(content: str) -> bool:
    """Check if content is a tool instruction that should be skipped."""
    for pattern in TOOL_INSTRUCTION_PATTERNS:
        if pattern in content[:200]:
            return True
    return False


def sanitize_text(text: str) -> str:
    """Sanitize text content for Tana."""
    if not text:
        return ""
    # Remove private use unicode characters
    result = PRIVATE_USE_PATTERN.sub("", text)
    # Remove file citation markers
    result = FILE_CITE_PATTERN.sub("[file]", result)
    # Remove parsed text page markers
    result = PARSED_TEXT_PATTERN.sub("", result)
    # Normalize line endings
    result = result.replace("\r\n", "\n").replace("\r", "\n")
    # Remove control characters (keep newlines and tabs)
    result = "".join(c for c in result if c in "\n\t" or ord(c) >= 32)
    return result.strip()


def parse_content_to_nodes(content: str) -> List[TanaNode]:
    """Parse markdown content into a list of TanaNodes.
    
    Creates proper Tana-native structure:
    - Each paragraph/bullet becomes a separate node
    - Nested bullets become child nodes
    - Headers become nodes with children
    """
    content = sanitize_text(content)
    if not content:
        return []
    
    lines = content.split("\n")
    result: List[TanaNode] = []
    current_paragraph: List[str] = []
    
    # Stack for tracking indentation: [(indent_level, parent_node), ...]
    indent_stack: List[tuple] = []
    
    def flush_paragraph():
        """Convert accumulated paragraph lines to a node."""
        nonlocal current_paragraph
        if current_paragraph:
            text = " ".join(current_paragraph).strip()
            if text and len(text) <= MAX_NODE_LENGTH:
                add_node_at_level(TanaNode(name=text), 0)
            elif text:
                # Split long paragraph
                chunks = split_text(text, MAX_NODE_LENGTH)
                for chunk in chunks:
                    add_node_at_level(TanaNode(name=chunk), 0)
            current_paragraph = []
    
    def add_node_at_level(node: TanaNode, indent: int):
        """Add a node at the appropriate nesting level."""
        # Pop stack until we find appropriate parent
        while indent_stack and indent_stack[-1][0] >= indent:
            indent_stack.pop()
        
        if indent_stack:
            parent = indent_stack[-1][1]
            if parent.children is None:
                parent.children = []
            parent.children.append(node)
        else:
            result.append(node)
        
        # Push this node as potential parent
        indent_stack.append((indent, node))
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines (flush paragraph)
        if not stripped:
            flush_paragraph()
            indent_stack.clear()  # Reset nesting on blank lines
            continue
        
        # Check for markdown header
        header_match = MARKDOWN_HEADER_RE.match(stripped)
        if header_match:
            flush_paragraph()
            indent_stack.clear()
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            if title:
                node = TanaNode(name=title, children=[])
                result.append(node)
                indent_stack.append((0, node))
            continue
        
        # Check for bullet point
        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            flush_paragraph()
            indent = len(bullet_match.group(1))
            text = bullet_match.group(3).strip()
            if text:
                if len(text) > MAX_NODE_LENGTH:
                    text = text[:MAX_NODE_LENGTH - 3] + "..."
                add_node_at_level(TanaNode(name=text), indent)
            continue
        
        # Check for numbered list that doesn't match BULLET_RE
        if re.match(r'^\d+\.\s+', stripped):
            flush_paragraph()
            text = re.sub(r'^\d+\.\s+', '', stripped)
            if text:
                if len(text) > MAX_NODE_LENGTH:
                    text = text[:MAX_NODE_LENGTH - 3] + "..."
                add_node_at_level(TanaNode(name=text), 0)
            continue
        
        # Regular text - accumulate as paragraph
        current_paragraph.append(stripped)
    
    # Flush any remaining paragraph
    flush_paragraph()
    
    return result


def split_text(text: str, max_length: int) -> List[str]:
    """Split long text into chunks."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    remaining = text
    
    while remaining:
        if len(remaining) <= max_length:
            chunks.append(remaining)
            break
        
        # Find split point at space
        split_point = remaining.rfind(" ", 0, max_length - 3)
        if split_point == -1 or split_point < max_length // 2:
            split_point = max_length - 3
        
        chunks.append(remaining[:split_point].rstrip() + "...")
        remaining = remaining[split_point:].lstrip()
        if remaining:
            remaining = "..." + remaining
    
    return chunks


def content_to_tana_nodes(content: str) -> List[TanaNode]:
    """Convert message content to TanaNode children.
    
    Creates proper Tana-native structure with nested nodes.
    """
    if not content:
        return []
    
    content = sanitize_text(content)
    if not content:
        return []
    
    # For very short, simple content - return as single node
    if len(content) <= 200 and "\n" not in content:
        return [TanaNode(name=content)]
    
    # Parse into proper node structure
    return parse_content_to_nodes(content)


def conversation_to_tana_node(
    conversation: ChatGPTConversation, timezone_name: str = "UTC"
) -> TanaNode:
    """Convert a ChatGPT conversation to a Tana node.
    
    Structure: Conversation → Prompt → Response nodes (properly nested)
    """
    dt = datetime.fromtimestamp(conversation.create_time)
    title = f"ChatGPT conversation - {dt.strftime('%Y-%m-%d %H:%M')}"
    
    children: List[TanaNode] = []
    current_prompt: Optional[TanaNode] = None
    
    for message in conversation.messages:
        raw_content = message.content or ""
        if not raw_content.strip():
            continue
        
        # Skip tool instruction messages
        if message.role == "tool" and is_tool_instruction(raw_content):
            continue
        
        if message.role == "user":
            # User prompts as single nodes
            prompt_text = sanitize_text(raw_content.replace("\n", " "))
            if len(prompt_text) > MAX_NODE_LENGTH:
                prompt_text = prompt_text[:MAX_NODE_LENGTH - 3] + "..."
            if prompt_text:
                current_prompt = TanaNode(name=prompt_text, children=[])
                children.append(current_prompt)
        elif message.role in ("assistant", "tool"):
            # Parse assistant responses into structured children
            if current_prompt:
                response_nodes = content_to_tana_nodes(raw_content)
                if current_prompt.children is None:
                    current_prompt.children = []
                current_prompt.children.extend(response_nodes)
    
    return TanaNode(name=title, supertag="ai-chat", children=children)


def estimate_node_size(node: TanaNode) -> int:
    """Estimate JSON size of a node."""
    import json
    return len(json.dumps(node.to_dict()))


def split_node_into_batches(node: TanaNode, max_size: int = MAX_PAYLOAD_SIZE) -> List[TanaNode]:
    """Split a large node into multiple smaller nodes that fit within payload limits."""
    import json
    
    # Recursively split any children that are too large
    if node.children:
        new_children = []
        for child in node.children:
            child_size = estimate_node_size(child)
            if child_size > max_size:
                # Recursively split this child
                if child.children:
                    split_children = split_large_child(child, max_size)
                    new_children.extend(split_children)
                else:
                    # Single node too large - truncate
                    if len(child.name) > max_size - 100:
                        child.name = child.name[:max_size - 103] + "..."
                    new_children.append(child)
            else:
                new_children.append(child)
        node.children = new_children
    
    base_size = estimate_node_size(node)
    
    if base_size <= max_size:
        return [node]
    
    if not node.children:
        return [node]
    
    # Split children into batches
    batches: List[List[TanaNode]] = []
    current_children: List[TanaNode] = []
    overhead = 200  # Approximate overhead for wrapper
    current_size = overhead
    
    for child in node.children:
        child_size = estimate_node_size(child)
        
        # If single child is still too large after splitting, we need to split it again
        if child_size > max_size - overhead:
            if child.children:
                # Further split this child
                sub_splits = split_large_child(child, max_size - overhead)
                for sub in sub_splits:
                    sub_size = estimate_node_size(sub)
                    if current_size + sub_size > max_size and current_children:
                        batches.append(current_children)
                        current_children = []
                        current_size = overhead
                    current_children.append(sub)
                    current_size += sub_size
            else:
                # Truncate if needed
                if len(child.name) > max_size - overhead - 50:
                    child.name = child.name[:max_size - overhead - 53] + "..."
                if current_children:
                    batches.append(current_children)
                    current_children = []
                    current_size = overhead
                current_children.append(child)
                current_size += estimate_node_size(child)
        else:
            if current_size + child_size > max_size and current_children:
                batches.append(current_children)
                current_children = []
                current_size = overhead
            
            current_children.append(child)
            current_size += child_size
    
    if current_children:
        batches.append(current_children)
    
    # Create nodes for each batch
    result = []
    total_batches = len(batches)
    
    for i, children in enumerate(batches):
        if total_batches == 1:
            batch_name = node.name
        elif i == 0:
            batch_name = f"{node.name} (1/{total_batches})"
        else:
            batch_name = f"{node.name} (continued {i+1}/{total_batches})"
        
        result.append(TanaNode(
            name=batch_name,
            supertag=node.supertag or "ai-chat",
            children=children
        ))
    
    return result


def split_large_child(node: TanaNode, max_size: int) -> List[TanaNode]:
    """Split a large child node's children into multiple sibling nodes.
    
    Recursively handles nested children that are also too large.
    """
    if not node.children:
        return [node]
    
    # First, recursively process any children that are too large
    processed_children = []
    for child in node.children:
        child_size = estimate_node_size(child)
        if child_size > max_size - 200 and child.children:
            # Recursively split this child
            split_parts = split_large_child(child, max_size - 200)
            processed_children.extend(split_parts)
        else:
            processed_children.append(child)
    
    # Now batch the processed children
    result = []
    current_children = []
    overhead = len(node.name) + 100
    current_size = overhead
    
    for child in processed_children:
        child_size = estimate_node_size(child)
        
        # If single child is too large, truncate its content
        if child_size > max_size - overhead:
            if child.children:
                # Flatten - take only first few children
                kept = []
                kept_size = 0
                for subchild in child.children:
                    sub_size = estimate_node_size(subchild)
                    if kept_size + sub_size < max_size - overhead - 200:
                        kept.append(subchild)
                        kept_size += sub_size
                    else:
                        break
                if len(kept) < len(child.children):
                    kept.append(TanaNode(name=f"[{len(child.children) - len(kept)} more items...]"))
                child.children = kept
                child_size = estimate_node_size(child)
            elif len(child.name) > max_size - overhead - 50:
                child.name = child.name[:max_size - overhead - 53] + "..."
                child_size = estimate_node_size(child)
        
        if current_size + child_size > max_size and current_children:
            result.append(TanaNode(
                name=node.name,
                children=current_children
            ))
            current_children = []
            current_size = overhead
        
        current_children.append(child)
        current_size += child_size
    
    if current_children:
        result.append(TanaNode(
            name=node.name,
            children=current_children
        ))
    
    # Update part numbers if we split
    if len(result) > 1:
        total = len(result)
        for i, n in enumerate(result):
            n.name = f"{node.name} (part {i+1}/{total})"
    
    return result


def create_tana_events(
    conversations: List[ChatGPTConversation],
    target_node_id: str,
) -> List[Dict[str, Any]]:
    """Create Tana API events from conversations.
    
    Large conversations are automatically split into multiple events.
    """
    events: List[Dict[str, Any]] = []
    
    for conversation in conversations:
        conv_node = conversation_to_tana_node(conversation)
        batches = split_node_into_batches(conv_node)
        
        for batch in batches:
            event = batch.to_dict()
            event["target"] = target_node_id
            events.append(event)
    
    return events
