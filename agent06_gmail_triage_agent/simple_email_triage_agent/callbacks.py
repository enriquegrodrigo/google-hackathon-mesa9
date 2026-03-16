import json
import logging
import os
import re
import warnings
from typing import Any, Dict, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from simple_email_triage_agent.config import settings

# Ignore all warnings
warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GMAIL_AUTH_ID = settings.AUTH_ID

DYNAMIC_AUTH_PARAM_NAME = "dynamic_auth_config"  # Name of the parameter to inject
DYNAMIC_AUTH_INTERNAL_KEY = (
    "oauth2_auth_code_flow.access_token"  # Internal key for the token
)


def dynamic_token_injection(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    token_key = None
    pattern = re.compile(
        r"^(temp:)?" + GMAIL_AUTH_ID + ".*"
    )  # Pattern to match the token key

    state_dict = tool_context.state.to_dict()

    # Try matching with the pattern
    matched_auth = {
        key: value for key, value in state_dict.items() if pattern.match(key)
    }

    if len(matched_auth) > 0:
        token_key = list(matched_auth.keys())[0]
    else:
        # Fallback: look for ANY key that looks like a token if the pattern fails
        # This is a safety net to see if we can find it anyway
        potential_tokens = [
            k for k in state_dict.keys() if "temp:" in k or "auth" in k.lower()
        ]
        if potential_tokens:
            token_key = potential_tokens[0]
        else:
            return None
    access_token = tool_context.state[token_key]
    dynamic_auth_config = {DYNAMIC_AUTH_INTERNAL_KEY: access_token}
    args[DYNAMIC_AUTH_PARAM_NAME] = json.dumps(dynamic_auth_config)
    return None
