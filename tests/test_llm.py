"""T0: the model client. Offline: LangChain's own fake chat model stands in for OpenRouter."""

from __future__ import annotations

import pytest
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from milo.llm import LangChainChat, live_chat_model


def test_live_client_refuses_without_the_live_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("MILO_LIVE", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    with pytest.raises(PermissionError, match="MILO_LIVE"):
        live_chat_model()


def test_live_client_refuses_without_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MILO_LIVE", "1")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(PermissionError, match="OPENROUTER_API_KEY"):
        live_chat_model()


# Building ChatOpenAI creates (never connects) a socket to probe IPv6 and socket options; the block stays on and
# turns that probe into this warning.
@pytest.mark.filterwarnings("ignore:A test tried to use socket.socket")
def test_live_client_points_at_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MILO_LIVE", "1")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    chat = live_chat_model()  # builds the client; no request is sent
    assert chat.price_usd_per_mtok == (0.10, 0.50)
    assert chat.model.model_name == "anthropic/claude-haiku-5.5"
    assert "openrouter.ai" in str(chat.model.openai_api_base)


def test_adapter_returns_the_kit_reply_shape() -> None:
    fake = FakeMessagesListChatModel(
        responses=[
            AIMessage(
                content="Hello.",
                usage_metadata={
                    "input_tokens": 12,
                    "output_tokens": 3,
                    "total_tokens": 15,
                },
            )
        ]
    )
    chat = LangChainChat(fake, price_usd_per_mtok=(0.10, 0.50))
    reply = chat.invoke([{"role": "user", "content": "Hi"}])
    assert reply.content == "Hello."
    assert reply.tool_calls == []
    assert (reply.usage.input_tokens, reply.usage.output_tokens) == (12, 3)


def test_adapter_joins_content_blocks() -> None:
    blocks = [{"type": "text", "text": "Two "}, {"type": "text", "text": "parts."}]
    fake = FakeMessagesListChatModel(responses=[AIMessage(content=blocks)])
    reply = LangChainChat(fake, (0.1, 0.5)).invoke([{"role": "user", "content": "Hi"}])
    assert reply.content == "Two parts."


def test_adapter_refuses_tools_until_m3() -> None:
    fake = FakeMessagesListChatModel(responses=[AIMessage(content="x")])
    with pytest.raises(NotImplementedError):
        LangChainChat(fake, (0.1, 0.5)).invoke([], tools=[object()])


def test_default_paths_open_no_socket(monkeypatch: pytest.MonkeyPatch) -> None:
    """The fake-model adapter and build_app run with sockets blocked and no warning filter."""
    from milo.app import build_app

    monkeypatch.delenv("MILO_LIVE", raising=False)
    fake = FakeMessagesListChatModel(responses=[AIMessage(content="ok")])
    assert (
        LangChainChat(fake, (0.1, 0.5))
        .invoke([{"role": "user", "content": "x"}])
        .content
        == "ok"
    )
    assert build_app(None, None, None).ask("hi", "u1", "t1").error is None
