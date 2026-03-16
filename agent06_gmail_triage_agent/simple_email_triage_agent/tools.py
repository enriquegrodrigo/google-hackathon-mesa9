# tools.py
from fastapi.openapi.models import OAuth2, OAuthFlowAuthorizationCode, OAuthFlows
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.tools.application_integration_tool.application_integration_toolset import (
    ApplicationIntegrationToolset,
)

# ... (imports and settings)

gmail_connector_tool = ApplicationIntegrationToolset(
    project=settings.GOOGLE_CLOUD_PROJECT,
    location=settings.GOOGLE_CLOUD_LOCATION,
    connection=settings.GMAIL_CONNECTION_NAME,
    actions=[
        "GET_gmail/v1/users/%7BuserId%7D/messages",
        # ... other actions
    ],
    tool_name_prefix="gmail_tool",
    tool_instructions="Use this tool to read emails.",
)

if settings.IS_ADK_WEB:
    # Local OAuth Configuration
    oauth2_scheme_gmail = OAuth2(
        flows=OAuthFlows(
            authorizationCode=OAuthFlowAuthorizationCode(
                authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",  # Authorization URL for Gmail
                tokenUrl="https://oauth2.googleapis.com/token",  # Token URL for Gmail
                scopes={
                    "https://www.googleapis.com/auth/gmail.readonly": "Read emails",  # Scopes for Gmail access
                },
            )
        )
    )
    oauth2_credential = AuthCredential(
        auth_type=AuthCredentialTypes.OAUTH2,
        oauth2=OAuth2Auth(
            client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
            client_secret=gmail_client_secret,
            redirect_uri=settings.AGENT_REDIRECT_URI,
        ),
    )
    gmail_connector_tool.auth_scheme = oauth2_scheme_gmail
    gmail_connector_tool.auth_credential = oauth2_credential
