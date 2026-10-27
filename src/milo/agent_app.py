"""The chat engine on LangChain's `create_agent`. It replaces the app's own loop for live answers.

Same app around it: the store, the history, the flow record, the policy rules, the overview and the web routes are the
`App` ones. Only `_ask` changes: the agent decides when to search (the `search_knowledge` tool) and which tools to call.
Every search numbers its passages, so the citations [n] in the answer point at the sources list. A destructive call
is paused by a human-in-the-loop middleware and is never executed without the owner's approval.

If the agent fails (provider error, bad output), the app's own loop runs instead, with its retries and local fallback.
"""

from __future__ import annotations

import os
import time
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from milo.agent_arm import make_tools
from milo.app import ABSTAIN, INVALID_MSG, App, _ms
from milo.llm import DEFAULT_PRICE
from milo.types import Response, Source, ToolResult

MAX_TOOL_STEPS = 6


class AgentApp(App):
    def __init__(self, *args: Any, agent_model: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.agent_model = agent_model
        self._hits: list[Source] = []

    def _numbered_search(self, query: str, section: str | None = None) -> str:
        """The search tool: retrieves, numbers each passage once per answer, and returns the numbered passages."""
        hits = super()._retrieve(query)
        if section:
            hits = [h for h in hits if self.chunks[h.chunk_id].section == section]
        if not hits:
            return "No passage matched."
        lines = []
        for h in hits:
            number = next(
                (i for i, x in enumerate(self._hits) if x.chunk_id == h.chunk_id), None
            )
            if number is None:
                self._hits.append(
                    h
                )  # the sources list keeps the order the numbers were given in
                number = len(self._hits) - 1
            lines.append(f"[{number + 1}] ({h.doc_id}) {h.text}")
        return "\n\n".join(lines)

    def _ask(
        self,
        question: str,
        user_id: str,
        trace: list[dict[str, Any]],
        prior: list[dict[str, str]],
    ) -> Response:
        problem = self._input_problem(question)
        if problem:
            trace.append({"step": "input", "ok": False, "problem": problem})
            return Response(answer=INVALID_MSG, error=f"invalid_input: {problem}")
        self._hits = []
        calls: list[dict[str, Any]] = []
        t0 = time.perf_counter()
        try:
            tools = make_tools(self.tools, user_id, calls, search=self._numbered_search)
            agent = create_agent(
                model=self.agent_model,
                tools=tools,
                system_prompt=self.system_prompt,
                middleware=[
                    HumanInTheLoopMiddleware(interrupt_on={"reset_diagnosis": True})
                ],
                checkpointer=InMemorySaver(),
            )
            config = {
                "configurable": {
                    "thread_id": f"{user_id}:{len(prior)}:{time.time_ns()}"
                },
                "recursion_limit": 2 * MAX_TOOL_STEPS + 4,
            }
            result = agent.invoke(
                {"messages": [*prior, {"role": "user", "content": question}]}, config
            )
        except Exception as e:  # noqa: BLE001 - any agent failure falls back to the app's own loop, which is typed
            trace.append(
                {"step": "agent", "ok": False, "ms": _ms(t0), "error": type(e).__name__}
            )
            return super()._ask(question, user_id, trace, prior)
        waiting = []
        for interrupt in result.get("__interrupt__", []):
            for request in interrupt.value.get("action_requests", []):
                waiting.append({"name": request["name"], "args": request["args"]})
        messages = result["messages"]
        answer = messages[-1].content if messages else ""
        if not isinstance(answer, str):
            answer = str(answer)
        tool_results = [
            ToolResult(
                name=c["name"],
                arguments=c["args"],
                output=c.get("output"),
                ok=c.get("ok", True),
                policy_decision="allowed",
            )
            for c in calls
        ] + [
            ToolResult(
                name=w["name"],
                arguments=w["args"],
                output=None,
                ok=False,
                policy_decision="needs_approval",
            )
            for w in waiting
        ]
        cost = _cost(messages)
        trace.append(
            {
                "step": "agent",
                "ok": True,
                "ms": _ms(t0),
                "calls": [c["name"] for c in calls],
                "waiting": [w["name"] for w in waiting],
            }
        )
        if waiting:
            return Response(
                answer="This action needs your approval first. Nothing was changed.",
                sources=list(self._hits),
                tool_results=tool_results,
                cost_usd=cost,
                stopped=True,
            )
        if not self._hits and not calls:
            return Response(answer=ABSTAIN, cost_usd=cost)
        return Response(
            answer=answer,
            sources=list(self._hits),
            tool_results=tool_results,
            cost_usd=cost,
        )


def _cost(messages: list[Any]) -> float:
    pin = float(os.environ.get("MILO_PRICE_IN", DEFAULT_PRICE[0]))
    pout = float(os.environ.get("MILO_PRICE_OUT", DEFAULT_PRICE[1]))
    total = 0.0
    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        total += (
            usage.get("input_tokens", 0) * pin / 1e6
            + usage.get("output_tokens", 0) * pout / 1e6
        )
    return round(total, 6)
