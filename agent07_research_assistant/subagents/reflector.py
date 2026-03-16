from google.adk.agents import Agent

from ..config import MODEL

# TODO: Implement the Reflector Agent
# Create an agent that acts as a teacher/grader to provide critique on the essay.

reflector = None
reflector = Agent(
	name="reflector",
	model=MODEL,
	description="Critiques the draft and suggests concrete improvements.",
	instruction="""You are a strict but constructive writing coach.
Review the current essay draft and provide actionable critique.

Focus areas:
- Thesis clarity and structure
- Evidence quality and specificity
- Coherence between paragraphs
- Gaps, inaccuracies, or unsupported claims

Output format:
1) Overall score out of 10
2) Top 3 strengths
3) Top 3 weaknesses
4) 3 concrete revision actions

Draft to critique:
{draft}
""",
	output_key="critique",
)
