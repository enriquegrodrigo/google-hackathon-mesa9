from google.adk.agents import Agent
from google.adk.tools import google_search

from ..config import (
	AGENT_MISSION,
	FOCUS_COMPANY,
	MIN_PUBLICATION_YEAR,
	MIN_SOURCES,
	MODEL,
	PREFER_LAST_MONTHS,
	PREFERRED_DOMAINS,
)

# TODO: Implement the Researcher Agents
# 1. `researcher`: Performs initial research.
# 2. `critique_researcher`: Performs follow-up research based on critique.

researcher = None
critique_researcher = None

preferred_domains_text = ", ".join(PREFERRED_DOMAINS)

researcher = Agent(
	name="researcher",
	model=MODEL,
	description="Runs initial web research for solving Telefonica-relevant problems with strong citation quality.",
	instruction=f"""You are a web research specialist.
Mission: {AGENT_MISSION}
Use Google Search to gather credible, relevant public information for the current task.

Context available in state:
- Plan: {{plan}}

Flexibility rules:
- Adapt the research scope to the user topic.
- Do not force fixed topic blocks.
- Keep relevance to {FOCUS_COMPANY} whenever possible.

Evidence quality rules:
- Aim for at least {MIN_SOURCES} credible sources overall.
- Prefer sources from the last {PREFER_LAST_MONTHS} months.
- Prefer publication year >= {MIN_PUBLICATION_YEAR} when possible.
- Prioritize these domains when relevant: {preferred_domains_text}
- Every key finding must include source title + URL + publication date.
- If date cannot be verified, mark it as date_unverified.

Return format:
1) Findings table with columns:
	Finding | Why it matters for {FOCUS_COMPANY} | Source title | URL | Publication date | Confidence.
2) Coverage summary (source count + freshness notes).
3) Gaps or weak evidence to improve in revision.
""",
	tools=[google_search],
	output_key="latest_research",
)

critique_researcher = Agent(
	name="critique_researcher",
	model=MODEL,
	description="Runs targeted follow-up research to close evidence gaps for Telefonica decisions.",
	instruction=f"""You are a follow-up research specialist.
Mission: {AGENT_MISSION}
Use Google Search to address weaknesses identified in the latest critique.

Context available in state:
- Existing draft: {{draft}}
- Critique: {{critique}}

Priorities:
1) Strengthen claims without citations.
2) Replace stale or weak evidence with fresher sources where possible.
3) Add missing publication dates and improve source diversity.
4) Improve direct decision value for {FOCUS_COMPANY}.

Rules:
- Use public, credible sources.
- Prefer last {PREFER_LAST_MONTHS} months and year >= {MIN_PUBLICATION_YEAR}.
- Avoid duplicates unless adding stronger evidence.

Return format:
1) Targeted findings with source title, URL, and date.
2) What gaps were closed.
3) Remaining evidence limitations (if any).
""",
	tools=[google_search],
	output_key="latest_research",
)
