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
        # TODO: Implement logic to append research to state['content']
        yield Event(author=self.name)


class RevisionController(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # TODO: Implement logic to check revision_number vs max_revisions
        # Use EventActions(escalate=True) to exit the loop.
        yield Event(author=self.name)
