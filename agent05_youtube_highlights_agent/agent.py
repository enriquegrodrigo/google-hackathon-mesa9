import json
import os
from typing import Any, Dict, Optional

import google.auth
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from pydantic import BaseModel, HttpUrl

from .prompt import (
    multimodal_agent_prompt,
    rank_agent_prompt,
    youtube_search_agent_prompt,
)
from .tools import youtube_search


class RankedVideo(BaseModel):
    """Represents the video selected by the ranking agent."""


def search_tool_output_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    # Store for later resue the user query and the youtube search result
    return None


def rank_output_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    # Store in the context the selected video by the rank agent
    pass


def build_llm_parts(video):
    # Create parts for the llm call
    parts = []
    parts.append(types.Part(text=f'Video: {video["title"]}'))
    parts.append(types.Part(text=f'url: {video["url"]}'))
    parts.append(
        types.Part(file_data=types.FileData(file_uri=video["url"], mime_type="video/*"))
    )
    return parts


def vision_callback_builds_video_parts(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Build the llmrequest for the the multimodal video analysis by providing the original user query, the url and video title to analyze
    pass


# Load environment variables from .env file
load_dotenv()

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


# TODO: Define the YouTube Search Agent
# This agent should be an LlmAgent that uses the `youtube_search` tool to find videos.
# - Give it a name, a model, and a description.
# - Use the `youtube_search_agent_prompt` as the instruction.
# - Use the `search_tool_output_callback` as the `after_tool_callback`.
# - Pass the `youtube_search` tool in the `tools` list.
youtube_search_agent = None  # Replace with your LlmAgent definition

# TODO: Define the Rank Agent
# This agent should be an LlmAgent that ranks the videos found by the search agent.
# - Give it a name, a model, and a description.
# - Use the `rank_agent_prompt` as the instruction.
# - Use the `rank_output_callback` as the `after_model_callback`.
# - Use the `RankedVideo` as the `output_schema`.
rank_agent = None  # Replace with your LlmAgent definition

# TODO: Define the Multimodal Agent
# This agent should be an LlmAgent that analyzes the video to find the key moment.
# - Give it a name, a model, and a description.
# - Use the `multimodal_agent_prompt` as the instruction.
# - Use the `vision_callback_builds_video_parts` as the `before_model_callback`.
multimodal_agent = None  # Replace with your LlmAgent definition

# TODO: Define the Root Agent
# This should be a SequentialAgent that runs the three agents in order.
# - Give it a name and a description.
# - Add the `youtube_search_agent`, `rank_agent`, and `multimodal_agent` to the `sub_agents` list.
root_agent = None  # Replace with your SequentialAgent definition
