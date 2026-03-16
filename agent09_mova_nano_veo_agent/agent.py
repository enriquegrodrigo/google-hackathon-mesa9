import os

import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent

from .prompts import MOVA_INSTRUCTION
from .tools import animate_frame, create_frame

# Load environment variables from .env file
load_dotenv()

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Root Agent ---
# The root agent which orchestrate the entire generation workflow
root_agent = None
