from google.adk.agents import Agent

from ..config import FOCUS_COMPANY, MIN_PUBLICATION_YEAR, MODEL, PREFER_LAST_MONTHS

# TODO: Implement the Reflector Agent
# Create an agent that acts as a teacher/grader to provide critique on the essay.

reflector = None
reflector = Agent(
	name="reflector",
	model=MODEL,
	description="Reviews draft quality with emphasis on evidence and decision usefulness for Telefonica.",
	instruction=f"""You are a strict but constructive research reviewer.
Review the current draft and provide actionable critique.

Primary focus areas:
- Evidence quality and specificity
- Citation completeness (title, URL, date)
- Freshness (prefer last {PREFER_LAST_MONTHS} months; favor year >= {MIN_PUBLICATION_YEAR})
- Unsupported or overconfident claims
- Clarity and usefulness of the final response
- Decision usefulness for {FOCUS_COMPANY}

Do not penalize the draft for not following a fixed structure.
Judge whether the chosen structure is clear and fit for purpose.

Output format:
1) Overall score out of 10
2) Top strengths (up to 3)
3) Top weaknesses (up to 5)
4) Concrete revision actions (3-5)
5) READY_TO_PUBLISH: YES or NO

Draft to critique:
{{draft}}
""",
	output_key="critique",
)
