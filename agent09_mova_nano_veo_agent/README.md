# Mova: GenMedia Agent (Nano + Veo)

**PoC**: [Giulio Salierno](mailto:giuliosalierno@google.com) [Lorenzo Spataro](mailto:lspataro@google.com)
**Created**: Oct 24, 2025
**Status**: Completed

Use ADK 1.6

---

## The Challenge

The objective is to create a conversational GenMedia Agent that bridges static images with dynamic motion. Users will describe a frame for Gemini 2.5-flash-image to create, which Veo 3 will then bring to life as video.

Traditional video production presents significant barriers, demanding specialized skills, expensive software, and considerable time for storyboarding, shooting, editing, and post-production. This complexity stifles creativity and limits the ability of marketers, educators, and individuals to quickly produce compelling video content.

The core task involves constructing an agent capable of interpreting a user's creative vision from a straightforward text prompt, generating a keyframe, and subsequently animating it with Veo.

---

## Our Proposed Solution

The Mova-Nano-Veo Agent is a generative AI agent that automates the entire video creation process. It uses Google's state-of-the-art Gemini models to transform text into stunning video sequences.

### Key Features

* **AI-Powered Frame Creation**: Use Gemini 2.5-flash-image Nano banana to generate a high-quality image that serves as the visual anchor for the video.
* **Advanced Video Synthesis**: Use Veo to create dynamic video content by animating a single frame.
* **Iterative Refinement**: Allows users to provide feedback to regenerate specific frames or generate a new video.

### How It Works

The agent operates through a sequential, multi-step workflow:

1.  **Root Agent**: This is the main agent that orchestrates the multi-step workflow. It implements two tools: one that generates an image given a user prompt using Gemini 2.5.-flash-image to construct a visual “storyboard” for the forthcoming video, and a dedicated `veo_tool` to invoke Veo instructing it to generate a video starting from a frame.
2.  **Output & Refinement**: The final generated video is then presented to the user.

---

## System Architecture

The Mova-Nano-Veo Agent functions as a sequential, tool-using AI agent, comprising the following components:

* **User Interface (UI)**: A front-end (CLI or ADK web UI or Gemini Enterprise) designed to accept user prompts and display the resulting video.
* **Root Agent (SequentialAgent)**: The principal agent responsible for orchestrating the multi-step workflow calling the two tools as needed.
* **Tools (FunctionTool)**:
    * **nano_tool**: A dedicated tool for generating images using Gemini Nano.
    * **veo_tool**: A tool specifically designed for generating video from images with Veo.
* **APIs**:
    * **Vertex AI API**: Provides access to both Gemini (Nano) and Veo models.
* **Data Flow**:
    1.  The user describes the images.
    2.  The Agent calls the `nano_tool` to generate an image and stores it as an artifact.
    3.  When the user is satisfied with the images generated, the Agent calls the `veo_tool`, supplying the images as input to the Veo model to generate the video.
    4.  The final video is returned to the user as an artifact.

---

## Assignment

**Starter**: Code repository (the updated version to be shared during the hackathon in a commonly accessible repo).

**High-level instructions**:

* Based on the agent specification above and the provided code, implement an ADK agent.
* Locally test the agent (`uv run adk run agent` or `uv run adk web`).
* Deploy the agent to Agent Engine.
* Validate the deployed version of the agent.
* Register the agent to Gemini Enterprise.
* Ensure full functionality within Gemini Enterprise.

**Example Prompts**:

* "Create a cinematic shot of a futuristic city at night, with flying cars and neon signs."
* "Generate a 15-second timelapse of a flower blooming."
* "Animate this image of a lion to make it look like it's roaring."

### Example Input

A majestic whale breaching the ocean surface in slow motion, with dramatic, cinematic lighting.

### Example Output

Video Generation Report:

 - Status: Success

 - Video Artifact: artifacts/generated_video_12345.mp4

 - Description: A 10-second, high-definition video clip depicting a large humpback whale breaching the water in slow motion. The scene is captured with dramatic, low-key lighting, accentuating the water droplets as they disperse through the air.


 ## Setting Up

To run the Agent Development Kit Application locally, execute the following steps:

1.  **Set up the Python virtual environment and install dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Add all necessary GCP Authentications and setup**:
    ```bash
    gcloud auth application-default login
    gcloud config set project YOUR_PROJECT_ID
    gcloud auth application-default set-quota-project YOUR_PROJECT_ID
    ```
3.  **Ensure an .env file is configured with the following variables**:
    ```env
    GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
    GOOGLE_CLOUD_LOCATION="us-central1" # e.g., us-central1 or europe-west1
    GOOGLE_GENAI_USE_VERTEXAI="TRUE"
    ```

**Note**: To utilize Veo, confirm that the "Vertex AI API" is enabled in your GCP project and that your project has been allowlisted for access to the Veo model.

## High-level instructions

 - Looking at the agent specification above and the provided code snippets, implement an ADK agent
 - Test the agent locally (`uv run adk web`)
 - Deploy the agent to Agent Engine
 - Test the deployed version of the agent
 - Link the agent to a Gemini Enterprise application
 - Make sure it works in Gemini Enterprise as well
