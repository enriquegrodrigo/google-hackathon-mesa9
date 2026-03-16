from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.planner import planner
from .subagents.reflector import reflector
from .subagents.researchers import critique_researcher, researcher
from .subagents.workflow import ResearchAppender, RevisionController
from .subagents.writer import writer

# TODO: Assemble the agents into a workflow
# 1. Define the `revision_loop` using `LoopAgent`.
# 2. Define the `root_agent` using `SequentialAgent`.

revision_loop = LoopAgent(
    name="revision_loop",
    description="Iteratively improve essay draft using critique and follow-up research.",
    max_iterations=5,
    sub_agents=[
        writer,
        reflector,
        critique_researcher,
        ResearchAppender(name="research_appender"),
        RevisionController(name="revision_controller"),
    ],
)

root_agent = SequentialAgent(
    name="research_assistant",
    description="Plans, researches, writes, critiques, and revises an essay.",
    sub_agents=[
        planner,
        researcher,
        ResearchAppender(name="initial_research_appender"),
        revision_loop,
    ],
)

if __name__ == "__main__":
    print("Agent definition loaded.")
