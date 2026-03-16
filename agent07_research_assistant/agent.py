from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.planner import planner
from .subagents.reflector import reflector
from .subagents.researchers import critique_researcher, researcher
from .subagents.workflow import ResearchAppender, RevisionController
from .subagents.writer import writer

# TODO: Assemble the agents into a workflow
# 1. Define the `revision_loop` using `LoopAgent`.
# 2. Define the `root_agent` using `SequentialAgent`.

# Placeholder:
revision_loop = None
root_agent = None

if __name__ == "__main__":
    print("Agent definition loaded.")
