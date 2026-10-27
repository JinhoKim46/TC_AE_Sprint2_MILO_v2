"""The chat engine on create_agent, with scripted models. Offline."""

from __future__ import annotations

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from milo.agent_app import AgentApp
from milo.embed import LexicalEmbedder
from milo.store import MemoryStore
from milo.tools import Backend
from milo.types import ChatReply, Document


class Scripted(FakeMessagesListChatModel):
    def bind_tools(
        self, tools, **kwargs
    ):  # the fake model accepts the tool list and replays its script
        return self


class Quiet:
    price_usd_per_mtok = (0.0, 0.0)

    def invoke(self, messages, tools=None):
        return ChatReply(content="loop answer")


DOC = Document(
    "solutions/request-dispatch",
    "# Request and dispatch\n\nOne shared request queue fed from calls, messages and email.",
    {"title": "Request and dispatch management", "section": "solutions"},
)


def app_with(script, store=None):
    store = store or MemoryStore()
    app = AgentApp(
        Quiet(),
        LexicalEmbedder(),
        Backend(store=store),
        store=store,
        agent_model=Scripted(responses=script),
    )
    app.ingest([DOC])
    return app


def test_search_then_answer_numbers_the_sources_the_answer_cites() -> None:
    app = app_with(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_knowledge",
                        "args": {"query": "shared request queue"},
                        "id": "s1",
                    }
                ],
            ),
            AIMessage(content="One shared queue takes calls, messages and email [1]."),
        ]
    )
    reply = app.ask("How are requests taken in?", user_id="u1", thread_id="t1")
    assert reply.answer.endswith("[1].")
    assert reply.sources and reply.sources[0].doc_id == "solutions/request-dispatch"
    assert [t.name for t in reply.tool_results] == ["search_knowledge"]
    assert any(s["step"] == "agent" and s["ok"] is True for s in reply.trace)


def test_a_destructive_call_waits_for_approval_and_is_not_run() -> None:
    store = MemoryStore()
    app = app_with(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "reset_diagnosis", "args": {"diagnosis_id": 1}, "id": "r1"}
                ],
            ),
            AIMessage(content="unused"),
        ],
        store=store,
    )
    reply = app.ask("Delete diagnosis 1.", user_id="u1", thread_id="t1")
    assert reply.stopped is True
    assert any(
        t.name == "reset_diagnosis" and t.policy_decision == "needs_approval"
        for t in reply.tool_results
    )


def test_a_failing_agent_falls_back_to_the_apps_own_loop() -> None:
    class Broken(FakeMessagesListChatModel):
        def bind_tools(self, tools, **kwargs):
            raise RuntimeError("provider down")

    store = MemoryStore()
    app = AgentApp(
        Quiet(),
        LexicalEmbedder(),
        Backend(store=store),
        store=store,
        agent_model=Broken(responses=[]),
    )
    app.ingest([DOC])
    reply = app.ask("Anything about requests?", user_id="u1", thread_id="t1")
    assert reply.answer == "loop answer"
    assert any(s["step"] == "agent" and s["ok"] is False for s in reply.trace)
