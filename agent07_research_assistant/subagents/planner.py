from google.adk.agents import Agent

from ..config import (
	AGENT_MISSION,
	FOCUS_COMPANY,
	MIN_PUBLICATION_YEAR,
	MIN_SOURCES,
	MODEL,
	PREFER_LAST_MONTHS,
)

# TODO: Implement the Planner Agent
# Use the `Agent` class to create a planner that generates an outline for the essay.
# See instructions in README.md

planner = None
planner = Agent(
	name="planner",
	model=MODEL,
	description="Builds an adaptive research plan for solving Telefonica-relevant problems.",
	instruction=f"""You are a planning assistant for a research workflow.
Mission: {AGENT_MISSION}
Create a concise plan tailored to the user's request.

Requirements:
- Adapt structure to the topic. Do not force a fixed essay template.
- Propose 3-6 research angles with one objective sentence each.
- Provide 6-10 suggested web research queries.
- Keep output factual, clear, and concise.

Business relevance:
- When possible, frame research angles around impact for {FOCUS_COMPANY}.
- Highlight where findings may affect product strategy, partnerships, operations, or regulation.

Quality targets for downstream research:
- At least {MIN_SOURCES} credible sources overall.
- Prefer publications from the last {PREFER_LAST_MONTHS} months.
- Accept sources published in or after {MIN_PUBLICATION_YEAR} when possible.
""",
	output_key="plan",
)
