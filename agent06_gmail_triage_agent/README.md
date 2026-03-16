# Hackathon Challenge: Simple Email Triage Agent

The objective of this challenge is to build an AI agent that helps users manage their flooded email inboxes.
The agent should automatically access a user's Gmail, read unread messages, extract tasks in them and classify them using the Eisenhower Matrix (Do, Delegate, Schedule, delete).

A successful solution must be:
- Secure: Safely handle user credentials and access emails.
- Efficient: Quickly process multiple emails without manual intervention.
- Accurate: Correctly classify emails based on their content and context.
- Actionable: Provide clear, organized output that helps the user prioritize their work.

Which involves defining the mechanisms for Gmail connectivity via Application Integration connectors, with a focus on implementing authorization overrides derived from user authentication.

#### Key Features
- **Gmail Integration**: Uses the Gmail API via Google Cloud Application Integration to securely access and retrieve emails.
- **Secure Authentication**: Supports both local OAuth2 for development and deployed dynamic token injection for secure production access via Gemini Enterprise.
- **Intelligent Analysis**: Leverages Gemini’s reasoning capabilities to understand email content, subject lines, and sender information.
- **Eisenhower Matrix Classification**: Automatically categorizes emails based on urgency and importance using a proven productivity framework.

---

## Task
1.  **Setup**: Use the provided starter code or create a new ADK project.
2.  **Implement Tools**: Use the `ApplicationIntegrationToolset` to connect to Gmail ([docs](https://google.github.io/adk-docs/tools/google-cloud-tools/#use-integration-connectors))
3.  **Implement Authentication**: Set up OAuth for local development and dynamic token injection for deployed environments.
4.  **Deploy**: Deploy the agent to Agent Engine and register it with Gemini Enterprise.

### Useful Code Snippets

1. Tool Definition with OAuth
The [tools.py](agent06_gmail_triage_agent/simple_email_triage_agent/tools.py) snippet shows how to configure the Gmail tool with OAuth for local development (ADK Web) and prepare it for deployment.

2. Dynamic Token Injection Callback (Deployed)
[The callbacks.py](agent06_gmail_triage_agent/simple_email_triage_agent/callbacks.py) snippet shows how to inject the user's Gmail token from the Gemini Enterprise session into the tool arguments.

3. Agent Configuration for deployment
Inject the token into the tool via the agent configuration in [agent.py](agent06_gmail_triage_agent/simple_email_triage_agent/agent.py).

### Example Prompts

- "Triage my unread emails."
- "What are the most important emails I received today?"
- "Do I have any emails that need immediate attention?"
- "Classify my latest 5 emails by priority"

### Example Output

- Classification Report:
  - Do (Urgent & Important):
    - Subject: "URGENT: Server Down" | Sender: IT Support
  - Schedule (Important & Not Urgent):
    - Subject: "Quarterly Planning Session" | Sender: Manager
  - Delegate (Urgent & Not Important):
    - Subject: "Meeting Request: Vendor Demo" | Sender: Sales Rep
  - Delete (Not Urgent & Not Important):
    - Subject: "Weekly Newsletter: 50% Off" | Sender: Retailer

### Relevant Materials
- [Configure Gmail Integration Connector (V1)](https://docs.cloud.google.com/integration-connectors/docs/connectors/gsc_gmail/configure)
- [Create OAuth Client for Gmail](https://docs.cloud.google.com/iap/docs/oauth-client-creation#create_an_oauth_client)
- [Gemini Enterprise Agent Registration Guide](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent)
