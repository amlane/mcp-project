from mcp.server.mcpserver import MCPServer, Context
import requests

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

if __name__ == "__main__":
    # Run the server using stdin/stdout communication protocol
    mcp.run()
