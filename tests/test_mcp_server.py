"""MILO's tools as an MCP server, tested through an in-memory client and server pair. Offline."""

from __future__ import annotations

import asyncio

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from milo.mcp_server import Approvals, build_server, set_current_user
from milo.store import MemoryStore
from milo.tools import Backend

# The asyncio loop opens a local socket pair for itself; these tests open no network connection.
pytestmark = pytest.mark.enable_socket


def make(store: MemoryStore | None = None):
    store = store or MemoryStore()
    return build_server(
        Backend(store=store),
        tokens={"tok-u1": "u1", "tok-u2": "u2"},
        approvals=Approvals(),
    ), store


def call(server, name, args, owner="u1"):
    async def go():
        set_current_user(owner)
        async with create_connected_server_and_client_session(
            server._mcp_server
        ) as client:
            result = await client.call_tool(name, args)
            return result

    return asyncio.run(go())


def test_the_six_tools_are_listed_with_their_arguments_and_no_owner_argument() -> None:
    server, _ = make()

    async def names():
        async with create_connected_server_and_client_session(
            server._mcp_server
        ) as client:
            tools = await client.list_tools()
            return {t.name: t.inputSchema for t in tools.tools}

    schemas = asyncio.run(names())
    assert set(schemas) == {
        "search_knowledge",
        "record_fact",
        "get_recorded_facts",
        "estimate_effect",
        "draft_diagnosis",
        "reset_diagnosis",
    }
    for name, schema in schemas.items():
        assert "user_id" not in schema.get("properties", {}), name
        assert "ctx" not in schema.get("properties", {}), name


def test_a_recorded_fact_belongs_to_the_caller_not_to_an_argument() -> None:
    server, store = make()
    call(
        server,
        "record_fact",
        {
            "field_id": "requests_per_week",
            "value": 40,
            "status": "reported",
            "evidence_text": "40 a week",
            "user_id": "u2",
        },
        owner="u1",
    )
    assert store.facts("u1")["requests_per_week"]
    assert not store.facts("u2")


def test_reset_needs_the_owner_approval_on_the_server() -> None:
    server, _ = make()
    result = call(server, "reset_diagnosis", {"diagnosis_id": 1}, owner="u1")
    assert "needs_approval" in str(result)
    server.approvals.grant("u1", 1)
    granted = call(server, "reset_diagnosis", {"diagnosis_id": 1}, owner="u1")
    assert "needs_approval" not in str(granted)


def test_a_call_without_an_owner_is_refused() -> None:
    server, _ = make()
    result = call(server, "get_recorded_facts", {}, owner=None)
    assert "no owner" in str(result) or "isError=True" in str(result)
