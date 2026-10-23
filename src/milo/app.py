"""The app the kit's contract suite builds: `build_app(chat_model, embeddings, tools_backend) -> App`.

T0 is a placeholder: it stores nothing and always answers that it is not built yet, without a model call. M1 adds
retrieval, M3 tools, M4 the policy layer, M5 errors and fallback.
"""

from __future__ import annotations

from typing import Any

from milo.types import Document, Response

NOT_BUILT = "MILO v2 is not built yet: retrieval arrives in milestone M1."


class App:
    def __init__(self, chat_model: Any, embeddings: Any, tools_backend: Any) -> None:
        self.chat = chat_model
        self.embeddings = embeddings
        self.tools = tools_backend

    def ingest(self, docs: list[Document]) -> None:
        pass

    def ask(self, question: str, user_id: str, thread_id: str) -> Response:
        return Response(answer=NOT_BUILT)


def build_app(chat_model: Any, embeddings: Any, tools_backend: Any) -> App:
    return App(chat_model, embeddings, tools_backend)
