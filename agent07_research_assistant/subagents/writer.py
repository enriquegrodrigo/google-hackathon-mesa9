from google.adk.agents import Agent

from ..config import MODEL

writer = Agent(
    name="writer",
    model=MODEL,
    instruction="""You are an essay assistant tasked with writing excellent 5-paragraph essays.
    Generate the best essay possible for the user's request and the initial outline.
    If the user provides critique, respond with a revised version of your previous attempts.

    Utilize all the information below as needed:

    ------

    {content}
    """,
    output_key="draft",
)
