from google.adk.agents import Agent

from ..config import MODEL

# TODO: Implement the Planner Agent
# Use the `Agent` class to create a planner that generates an outline for the essay.
# See instructions in README.md

planner = None
planner = Agent(
	name="planner",
	model=MODEL,
	description="Builds a concise essay outline and research direction.",
	instruction="""You are a planning assistant for a research-writing workflow.
Create a concise, high-quality outline for the user request.

Requirements:
- Produce a 5-section outline suitable for a short essay.
- Include one short objective sentence per section.
- Include 4-6 suggested web research queries at the end.
- Keep the output factual, structured, and concise.
""",
	output_key="plan",
)
