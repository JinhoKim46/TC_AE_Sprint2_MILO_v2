"""T0: `build_app` exists with the kit's interface. Later milestones replace the placeholder answer."""

from __future__ import annotations

from milo.app import build_app
from milo.types import Document, Response


class NoCallChat:
    price_usd_per_mtok = (0.0, 0.0)
    calls = 0

    def invoke(self, messages, tools=None):  # pragma: no cover - must not be called
        self.calls += 1
        raise AssertionError("T0 makes no model call")


def test_build_app_has_the_kit_interface() -> None:
    chat = NoCallChat()
    app = build_app(chat, embeddings=None, tools_backend=None)
    app.ingest([Document("kb/x", "text", {})])
    r = app.ask("hello", user_id="u1", thread_id="t1")
    assert isinstance(r, Response)
    assert r.answer and r.sources == [] and r.tool_results == []
    assert r.cost_usd == 0.0 and r.error is None and r.stopped is False
    assert chat.calls == 0
