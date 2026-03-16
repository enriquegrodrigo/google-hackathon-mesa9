from google.adk.agents import Agent
from google.adk.tools import google_search

from ..config import MODEL

# TODO: Implement the Researcher Agents
# 1. `researcher`: Performs initial research.
# 2. `critique_researcher`: Performs follow-up research based on critique.

researcher = None
critique_researcher = None

researcher = Agent(
	name="researcher",
	model=MODEL,
	description="Runs initial web research for the essay plan.",
	instruction="""You are a web research specialist.
Use Google Search to gather credible, relevant information for the current writing task.

Context available in state:
- Outline: {plan}

Return:
- 6-10 concise bullet points of factual findings.
- Include source titles and links when available.
- Focus on directly useful evidence for writing.
""",
	tools=[google_search],
	output_key="latest_research",
)

critique_researcher = Agent(
	name="critique_researcher",
	model=MODEL,
	description="Runs targeted follow-up research from critique gaps.",
	instruction="""You are a follow-up research specialist.
Use Google Search to address weaknesses identified in the latest critique.

Context available in state:
- Existing draft: {draft}
- Critique: {critique}

Return:
- 4-8 targeted findings that specifically address critique points.
- Include source titles and links when available.
- Avoid repeating already-covered points unless adding stronger evidence.
""",
	tools=[google_search],
	output_key="latest_research",
)
