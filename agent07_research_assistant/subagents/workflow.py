from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

# TODO: Implement Workflow Agents
# 1. `ResearchAppender`: Appends research results to the "content" state.
# 2. `RevisionController`: Controls the number of revisions.


class ResearchAppender(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        state = ctx.session.state
        latest_research = state.get("latest_research")
        existing_content = state.get("content", [])

        if not isinstance(existing_content, list):
            existing_content = [str(existing_content)]

        if latest_research:
            updated_content = [*existing_content, latest_research]
            yield Event(
                author=self.name,
                actions=EventActions(
                    stateDelta={
                        "content": updated_content,
                    }
                ),
            )
            return

        # Always ensure `content` exists in session state for downstream prompts.
        yield Event(
            author=self.name,
            actions=EventActions(
                stateDelta={
                    "content": existing_content,
                }
            ),
        )


class RevisionController(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        state = ctx.session.state
        revision_number = int(state.get("revision_number", 0))
        max_revisions = int(state.get("max_revisions", 2))

        next_revision_number = revision_number + 1
        should_exit_loop = next_revision_number >= max_revisions

        actions = EventActions(
            stateDelta={"revision_number": next_revision_number},
            escalate=should_exit_loop,
        )
        yield Event(author=self.name, actions=actions)
