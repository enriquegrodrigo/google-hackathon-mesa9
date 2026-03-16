import asyncio
import os

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from agent07_research_assistant.agent import root_agent


async def main():
    print("Starting Research Assistant Test...")

    session_service = InMemorySessionService()

    # Run the agent with a sample query
    runner = Runner(
        agent=root_agent, app_name="test_app", session_service=session_service
    )

    user_id = "test_user"
    session_id = "test_session"

    await session_service.create_session(
        app_name="test_app", user_id=user_id, session_id=session_id
    )

    # Iterate over events (run_async is a generator)
    async for event in runner.run_async(
        new_message=types.Content(
            role="user",
            parts=[
                types.Part(
                    text="Write a short essay about the benefits of specialized autonomous agents."
                )
            ],
        ),
        user_id=user_id,
        session_id=session_id,
    ):
        pass  # We just consume events for now

    # Get final state
    session = await session_service.get_session(
        app_name="test_app", user_id=user_id, session_id=session_id
    )

    state = session.state

    print("\n--- Final State Keys ---")
    print(state.keys())

    if "plan" in state:
        print("\n--- Plan ---")
        print(state["plan"])
    else:
        print("\nERROR: No plan generated.")

    if "content" in state:
        print(f"\n--- Research Content Items: {len(state['content'])} ---")
        # print(state["content"]) # Might be long
    else:
        print("\nERROR: No research content found.")

    if "draft" in state:
        print("\n--- Final Draft ---")
        print(state["draft"])
    else:
        print("\nERROR: No draft generated.")

    if "critique" in state:
        print("\n--- Last Critique ---")
        print(state["critique"])

    print("\nTest Complete.")


if __name__ == "__main__":
    asyncio.run(main())
