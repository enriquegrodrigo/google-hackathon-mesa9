import os
import time
from typing import Optional

import google.auth
import google.genai as genai
from dotenv import load_dotenv
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.types import Image

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

client = genai.Client(vertexai=True, project=project_id, location="global")


async def create_frame(
    tool_context: ToolContext, prompt: str, is_image_edit: bool
) -> dict:
    """
    Use this tool to create an image or to modify a previously generated image based on a user request.
    Args:
    prompt: the prompt to create or edit an image based on the user requests.
    is_image_edit: Set this to True if the user wants edit a previous generated image, False otherwise (create a brand new image)
    """
    # TODO: Implement this function
    # The implementation should:
    # 1. Define the model to use (e.g., "gemini-2.5-flash-image-preview").
    # 2. Create an enhanced prompt for better image quality.
    # 3. If `is_image_edit` is True, load the previous image artifact.
    # 4. Call the model to generate the image.
    # 5. Save the newly generated image as an artifact.
    # 6. Return a dictionary with the status and filename.
    return {"status": "error", "message": "Not implemented."}


async def animate_frame(prompt: str, tool_context: ToolContext) -> dict:
    """
    Use this tool to animate a previously generated image. Never call this tool if an image has never been generated or if the user asks to generate a new image and the image still need to be generated.
    Args:
    prompt: the prompt to generate the video tailored on the user request
    """
    # TODO: Implement this function
    # The implementation should:
    # 1. Define the video model to use (e.g., "veo-3.0-generate-preview").
    # 2. Load the latest image artifact that was created.
    # 3. Call the model to generate the video.
    # 4. Wait for the video generation operation to complete.
    # 5. Save the generated video as an artifact.
    # 6. Return a dictionary with the status and filename.
    return {"status": "error", "message": "Not implemented."}
