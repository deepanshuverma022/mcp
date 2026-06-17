# Website Security Auditor MCP Server

This is an MCP (Model Context Protocol) server that consumes the Website Security Auditor REST API.

## Features
- Provides the `scan_website` tool to analyze a target website for vulnerabilities.
- Uses `FastMCP` from the official Python MCP SDK.
- Exposes a standard `GET /health` endpoint for monitoring.
- Starts with the requested transport mechanism.

## Local Testing
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python server.py`

## Testing with MCP Inspector
1. Ensure the server is running locally.
2. Follow the official [MCP Inspector documentation](https://modelcontextprotocol.io/docs/tools/inspector) to connect to your SSE URL (e.g., `http://localhost:8000/sse` or the specific transport endpoint).

## Render Deployment (Free Tier)
1. Push this `mcp-server` folder to a GitHub repository.
2. Go to your Render Dashboard and click **New +**, then select **Web Service**.
3. Connect your GitHub repository.
4. Fill out the configuration:
   - **Name**: `mcp-security-auditor`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Select the **Free** tier.
5. Expand "Advanced" and click "Add Environment Variable":
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.11`
6. Click **Create Web Service**. It will build and deploy automatically.

## Connecting Clients

### Claude Desktop
Add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "security-auditor": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"]
    }
  }
}
```

### Cursor
Add a new MCP server in Cursor Settings -> Features -> MCP:
- Type: `SSE` (or the equivalent for `streamable-http`)
- URL: `https://your-app-url.onrender.com/sse` (or your local URL)

### ChatGPT Agents
Use the deployed URL (`https://your-app-url.onrender.com`) to provide an MCP integration if they support SSE or raw OpenAPI imports.
