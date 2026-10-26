"""The site pages: chat at /chat, knowledge base index and document pages, shared navigation. Offline."""

from __future__ import annotations

from _auth import signed_in_app

from milo.app import build_app
from milo.embed import LexicalEmbedder
from milo.store import MemoryStore
from milo.tools import Backend
from milo.types import ChatReply


class Quiet:
    price_usd_per_mtok = (0.0, 0.0)

    def invoke(self, messages, tools=None):
        return ChatReply(content="ok")


def client():
    store = MemoryStore()
    milo = build_app(Quiet(), LexicalEmbedder(), Backend(store=store))
    milo.store = store
    return signed_in_app(milo)[1]


def test_chat_lives_at_chat_and_the_shared_navigation_is_on_it() -> None:
    page = client().get("/chat").get_data(as_text=True)
    assert "New conversation" in page and 'href="/kb"' in page and "Log out" in page
    assert 'href="/dashboard"' not in page  # the overview is the owner's only
    assert "/static/milo-mark.svg" in page


def test_knowledge_base_index_lists_documents_by_section() -> None:
    page = client().get("/kb").get_data(as_text=True)
    assert "Knowledge base" in page and "Service areas" in page and "Past cases" in page
    assert "/kb/solutions/request-dispatch" in page


def test_document_page_shows_the_text_and_refuses_paths_outside_the_knowledge_base() -> (
    None
):
    c = client()
    ok = c.get("/kb/solutions/request-dispatch")
    assert ok.status_code == 200 and "Request and dispatch management" in ok.get_data(
        as_text=True
    )
    assert c.get("/kb/../../pyproject").status_code == 404
    assert c.get("/kb/does/not/exist").status_code == 404


def test_milo_icon_is_served() -> None:
    resp = client().get("/static/milo-mark.svg")
    assert resp.status_code == 200 and b"<svg" in resp.data
