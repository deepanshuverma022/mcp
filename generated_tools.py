import json
from mcp.server.fastmcp import FastMCP
from .api_client import api_client

def register_tools(mcp: FastMCP):
    
    @mcp.tool()
    async def scan_website(url: str) -> str:
        """
        Scan a website for security vulnerabilities.
        
        Args:
            url: The full URL to audit, e.g., 'https://example.com'
        """
        try:
            result = await api_client.scan_website(url)
            # Return JSON string as the standard output format for MCP tools
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error scanning website: {str(e)}"
