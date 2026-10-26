"""The same tools run by LangChain's `create_agent`, to compare with the app's own loop (`milo.app.App`).

The rules do not change between the two arms: arguments go through `validate_args`, the owner is the caller's id and
never a model argument, and `reset_diagnosis` is paused by a human-in-the-loop middleware until the owner approves.
The retrieval step is not run before the model here: the agent decides whether to call `search_knowledge`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver

from milo.app import SYSTEM
from milo.tools import Backend, specs, validate_args


def make_tools(
    backend: Backend,
    user_id: str,
    calls: list[dict[str, Any]],
    search: Callable[..., str] | None = None,
) -> list[StructuredTool]:
    """The six tools for one owner. `search` replaces the search_knowledge handler (the chat engine numbers the passages)."""
    all_specs = specs()

    def tool_for(spec: Any) -> StructuredTool:
        def run(**args: Any) -> Any:
            problem = validate_args(spec.name, args, all_specs)
            if problem:
                return {"ok": False, "error": problem}
            entry = {"name": spec.name, "args": args, "ok": True}
            calls.append(entry)
            if spec.name == "search_knowledge" and search is not None:
                entry["output"] = search(**args)
                return entry["output"]
            entry["output"] = backend.call(spec.name, args, user_id=user_id)
            return entry["output"]

        return StructuredTool(
            name=spec.name,
            description=spec.description,
            args_schema=spec.parameters,
            func=run,
        )

    return [tool_for(spec) for spec in all_specs]


def run_agent(
    question: str, backend: Backend, user_id: str, model: Any, thread_id: str
) -> dict[str, Any]:
    """One question through `create_agent`. Returns the answer, the calls made, and any calls waiting for approval."""
    calls: list[dict[str, Any]] = []
    agent = create_agent(
        model=model,
        tools=make_tools(backend, user_id, calls),
        system_prompt=SYSTEM,
        middleware=[HumanInTheLoopMiddleware(interrupt_on={"reset_diagnosis": True})],
        checkpointer=InMemorySaver(),
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        {"configurable": {"thread_id": thread_id}},
    )
    waiting = []
    for interrupt in result.get("__interrupt__", []):
        for request in interrupt.value.get("action_requests", []):
            waiting.append(
                {
                    "name": request["name"],
                    "args": request["args"],
                    "status": "needs_approval",
                }
            )
    answer = result["messages"][-1].content
    return {
        "answer": answer if isinstance(answer, str) else str(answer),
        "calls": calls,
        "waiting": waiting,
    }
