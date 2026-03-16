import vertexai
from google.adk.agents.llm_agent import LlmAgent

from agent06_gmail_triage_agent.simple_email_triage_agent.callbacks import (
    dynamic_token_injection,
)
from agent06_gmail_triage_agent.simple_email_triage_agent.tools import gmail_connector_tool

vertexai.init(
    project="your_project_id",
    location="your_location",
    staging_bucket="your_staging_bucket",
)


root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="simple_email_triage_agent",
    description="",  # Add your agent description here
    instruction="",  # Add your agent instruction here
    before_tool_callback=dynamic_token_injection,
    tools=[gmail_connector_tool],
)
