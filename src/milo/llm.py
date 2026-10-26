"""The model client: LangChain `ChatOpenAI` pointed at OpenRouter, behind the kit's `invoke(messages, tools)`.

`live_chat_model()` refuses unless `MILO_LIVE=1` and a key are set, so no test or default command can spend.
`LangChainChat` adapts any LangChain chat model to the kit's interface; tests give it LangChain's fake model.
"""

from __future__ import annotations

import os
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from milo.types import ChatReply, ToolCall, Usage

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_CHAT_MODEL = "anthropic/claude-haiku-5.5"
DEFAULT_PRICE = (
    0.10,
    0.50,
)  # USD per million tokens, input and output (OpenRouter catalogue, 2026-10-23)


class LangChainChat:
    """A LangChain chat model with the kit's interface and its price."""

    def __init__(
        self, model: BaseChatModel, price_usd_per_mtok: tuple[float, float]
    ) -> None:
        self.model = model
        self.price_usd_per_mtok = price_usd_per_mtok

    def invoke(
        self, messages: list[dict[str, Any]], tools: list[Any] | None = None
    ) -> ChatReply:
        model = self.model
        if tools:
            model = self.model.bind_tools([openai_tool(t) for t in tools])
        msg = model.invoke([to_message(m) for m in messages])
        if not isinstance(msg, AIMessage):
            raise TypeError(f"expected an AIMessage, got {type(msg).__name__}")
        usage = msg.usage_metadata or {}
        return ChatReply(
            content=text_of(msg.content),
            tool_calls=[
                ToolCall(c["id"] or "", c["name"], c["args"]) for c in msg.tool_calls
            ],
            usage=Usage(usage.get("input_tokens", 0), usage.get("output_tokens", 0)),
        )


def openai_tool(spec: Any) -> dict[str, Any]:
    """A tool spec in the function-calling shape the OpenRouter endpoint expects."""
    return {
        "type": "function",
        "function": {
            "name": spec.name,
            "description": spec.description,
            "parameters": spec.parameters,
        },
    }


def to_message(m: dict[str, Any]) -> Any:
    """Our role/content dicts as LangChain messages. Assistant tool calls and tool results keep their ids."""
    role = m["role"]
    if role == "system":
        return SystemMessage(content=m["content"])
    if role == "user":
        return HumanMessage(content=m["content"])
    if role == "assistant":
        calls = [
            {
                "name": c["name"],
                "args": c["arguments"],
                "id": c["id"],
                "type": "tool_call",
            }
            for c in m.get("tool_calls", [])
        ]
        return AIMessage(content=m.get("content", ""), tool_calls=calls)
    if role == "tool":
        return ToolMessage(content=m["content"], tool_call_id=m["tool_call_id"])
    raise ValueError(f"unknown role {role}")


def text_of(content: str | list[Any]) -> str:
    """The text of a message. Some providers (Anthropic among them) return a list of content blocks."""
    if isinstance(content, str):
        return content
    return "".join(
        b if isinstance(b, str) else str(b.get("text", ""))
        for b in content
        if isinstance(b, str) or b.get("type") == "text"
    )


def live_chat_model() -> LangChainChat:
    """`ChatOpenAI` on OpenRouter. Building it sends nothing; the first `invoke` does."""
    if os.environ.get("MILO_LIVE") != "1":
        raise PermissionError("a live model needs MILO_LIVE=1 (paid call)")
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        raise PermissionError("OPENROUTER_API_KEY is not set")
    from langchain_openai import ChatOpenAI

    model = os.environ.get("MILO_CHAT_MODEL", DEFAULT_CHAT_MODEL)
    price = (
        float(os.environ.get("MILO_PRICE_IN", DEFAULT_PRICE[0])),
        float(os.environ.get("MILO_PRICE_OUT", DEFAULT_PRICE[1])),
    )
    chat = ChatOpenAI(
        model=model,
        api_key=key,
        base_url=OPENROUTER_BASE_URL,
        temperature=0,
        timeout=30,
        max_retries=0,  # retries are the app's job (M5), so they stay visible and bounded
    )
    return LangChainChat(chat, price)
