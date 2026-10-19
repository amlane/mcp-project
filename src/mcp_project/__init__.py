from mcp.server.mcpserver import MCPServer, Context
import requests
import os
from dotenv import load_dotenv

# Initialize FastMCP
mcp = MCPServer("Enterprise-Integration-Server")

@mcp.tool()
def fetch_public_issues(owner: str, repo: str) -> str:
    """
    Fetches the latest open issues from a public repository. 
    Use this tool when a user asks about bugs, tasks, or repository health.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?per_page=3"
    headers = {"User-Agent": "MCP-Interview-App"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            issues = response.json()
            if not issues:
                return f"No open issues found in {owner}/{repo}."
            
            summary = []
            for issue in issues:
                summary.append(f"- #{issue['number']}: {issue['title']} (by {issue['user']['login']})")
            return "\n".join(summary)
        else:
            return f"Failed to fetch data. API returned status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@mcp.tool()
def fetch_jira_ticket(ticket_key: str) -> str:
    """
    Fetches a jira ticket by key and returns ticket summary and description as well as a link to the full ticket.
    Use this tool when a user asks for details about a Jira ticket. 
    Ask for the ticket key if they do not provide it up front.
    """
    load_dotenv()
    JIRA_URL = os.getenv("JIRA_URL")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    jira_ticket_url = f"{JIRA_URL}/rest/api/3/issue/{ticket_key}"
    
    try:
        auth = (JIRA_EMAIL, JIRA_API_TOKEN)
        response = requests.get(jira_ticket_url, auth=auth)
        if response.status_code == 200:
            details = response.json()
            if not details or "fields" not in details:
                return f"no content found for {ticket_key}, response: {details}"
            else:
                summary = []
                fields = details["fields"];
                assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
                summary.append(f"- #{details['key']}: {fields['summary']}")
                summary.append(f"    - Assignee: {assignee}")
                summary.append(f"    - Status: {fields['status']['name']}")
                summary.append(f"    - Type: {fields['issuetype']['name']}")
                summary.append(f"    - Last Updated: {fields['updated']}")
                summary.append(f"    - URL: {JIRA_URL}/browse/{ticket_key}")
                return "\n".join(summary)
        else:
            return f"Failed to fetch data. API returned status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    # Run the server using stdin/stdout communication protocol
    mcp.run()
