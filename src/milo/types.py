"""The data shapes of the kit's interface (contract/README.md). The kit's tests read these by attribute, so MILO
keeps its own copies instead of importing the kit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ChatReply:
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)


@dataclass
class Document:
    doc_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Source:
    chunk_id: str
    doc_id: str
    score: float
    text: str


@dataclass
class ToolResult:
    name: str
    arguments: dict[str, Any]
    output: Any
    ok: bool
    policy_decision: str  # "allowed" | "needs_approval" | "denied"


@dataclass
class Response:
    answer: str
    sources: list[Source] = field(default_factory=list)
    tool_results: list[ToolResult] = field(default_factory=list)
    cost_usd: float = 0.0
    stopped: bool = False
    error: str | None = None
