"""MILO's six tools served as an MCP server (streamable HTTP), so other MCP clients can call them.

Rules that hold here as they do in the web app:
- Identity comes from the bearer token of the request, never from a tool argument. The token table is given to
  `build_server`; in-memory tests set the user with `set_current_user`.
- Arguments go through `milo.tools.validate_args` before a handler runs.
- `reset_diagnosis` needs an approval recorded on the server for that owner and diagnosis. Without it the tool returns
  `needs_approval` and changes nothing. The MCP protocol has no approval step of its own.

Run: MILO_MCP_TOKENS='{"<token>": "<owner id>"}' uv run python -m milo.mcp_server  (listens on 127.0.0.1:8765)
"""

from __future__ import annotations

import json
import os
from contextvars import ContextVar
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from milo.tools import Backend, specs, validate_args

_user: ContextVar[str | None] = ContextVar("milo_mcp_user", default=None)


def set_current_user(user_id: str | None) -> None:
    """For in-memory tests and local runs without HTTP: the owner the calls are made for."""
    _user.set(user_id)


class Approvals:
    """Owner approvals of destructive actions, kept on the server. Each approval covers one (owner, diagnosis) pair."""

    def __init__(self) -> None:
        self._pairs: set[tuple[str, int]] = set()

    def grant(self, owner: str, diagnosis_id: int) -> None:
        self._pairs.add((owner, diagnosis_id))

    def has(self, owner: str, diagnosis_id: int) -> bool:
        return (owner, diagnosis_id) in self._pairs


def build_server(
    backend: Backend, tokens: dict[str, str], approvals: Approvals | None = None
) -> FastMCP:
    approvals = approvals or Approvals()
    all_specs = specs()
    mcp = FastMCP("milo-tools")

    def owner_of(ctx: Context | None) -> str:
        request = (
            getattr(getattr(ctx, "request_context", None), "request", None)
            if ctx
            else None
        )
        if request is not None:
            header = request.headers.get("authorization", "")
            token = header.removeprefix("Bearer ").strip()
            if token in tokens:
                return tokens[token]
            raise PermissionError("unknown or missing bearer token")
        owner = _user.get()
        if owner is None:
            raise PermissionError("no owner for this call")
        return owner

    def call(name: str, args: dict[str, Any], ctx: Context | None) -> Any:
        args = {k: v for k, v in args.items() if v is not None}
        problem = validate_args(name, args, all_specs)
        if problem:
            return {"ok": False, "error": problem}
        owner = owner_of(ctx)
        if name == "reset_diagnosis" and not approvals.has(owner, args["diagnosis_id"]):
            return {
                "ok": False,
                "status": "needs_approval",
                "message": "The owner must approve this reset first.",
            }
        return backend.call(name, args, user_id=owner)

    @mcp.tool(
        description=next(
            s.description for s in all_specs if s.name == "search_knowledge"
        )
    )
    def search_knowledge(
        query: str, section: str | None = None, ctx: Context | None = None
    ) -> Any:
        return call("search_knowledge", {"query": query, "section": section}, ctx)

    @mcp.tool(
        description=next(s.description for s in all_specs if s.name == "record_fact")
    )
    def record_fact(
        field_id: str,
        value: str | float | list[str],
        status: str,
        evidence_text: str,
        unit: str | None = None,
        ctx: Context | None = None,
    ) -> Any:
        return call(
            "record_fact",
            {
                "field_id": field_id,
                "value": value,
                "status": status,
                "evidence_text": evidence_text,
                "unit": unit,
            },
            ctx,
        )

    @mcp.tool(
        description=next(
            s.description for s in all_specs if s.name == "get_recorded_facts"
        )
    )
    def get_recorded_facts(ctx: Context | None = None) -> Any:
        return call("get_recorded_facts", {}, ctx)

    @mcp.tool(
        description=next(
            s.description for s in all_specs if s.name == "estimate_effect"
        )
    )
    def estimate_effect(area_id: str, ctx: Context | None = None) -> Any:
        return call("estimate_effect", {"area_id": area_id}, ctx)

    @mcp.tool(
        description=next(
            s.description for s in all_specs if s.name == "draft_diagnosis"
        )
    )
    def draft_diagnosis(area_id: str, ctx: Context | None = None) -> Any:
        return call("draft_diagnosis", {"area_id": area_id}, ctx)

    @mcp.tool(
        description=next(
            s.description for s in all_specs if s.name == "reset_diagnosis"
        )
    )
    def reset_diagnosis(diagnosis_id: int, ctx: Context | None = None) -> Any:
        return call("reset_diagnosis", {"diagnosis_id": diagnosis_id}, ctx)

    mcp.approvals = approvals  # type: ignore[attr-defined]  # the web app grants approvals through this
    return mcp


if __name__ == "__main__":
    from milo.store import MemoryStore

    tokens = json.loads(os.environ.get("MILO_MCP_TOKENS", "{}"))
    if not tokens:
        raise SystemExit("set MILO_MCP_TOKENS to a JSON object of token to owner id")
    server = build_server(Backend(store=MemoryStore()), tokens)
    server.settings.port = 8765
    server.run(transport="streamable-http")
