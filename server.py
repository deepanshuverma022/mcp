import os
import sys
# Ensure the current directory is in the Python path for Render deployment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from app_tools.generated_tools import register_tools
from app_tools.api_client import api_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server bound to all hosts for Render deployment
mcp = FastMCP("Website Security Auditor", host="0.0.0.0")

# Register generated tools
register_tools(mcp)

# --- Health Endpoint & ASGI App Integration ---
# FastMCP abstracts the transport layer. For deployments like Render,
# it is common to mount or wrap the server in an ASGI application like FastAPI.
# Here we expose a standalone ASGI app that provides the GET /health endpoint.
app = FastAPI(title="Website Security Auditor MCP Server")

@app.get("/health")
async def health_check():
    """Health check endpoint for Render."""
    return {"status": "ok"}

# When deployed on Render via uvicorn, the main app entrypoint serves the healthcheck,
# and we mount the standard SSE app so the agent builder can access it.
try:
    mcp_app = mcp.sse_app()
    app.mount("/", mcp_app)  # Exposes /sse and /messages
except Exception as e:
    logger.error(f"Failed to mount SSE app: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await api_client.close()

if __name__ == "__main__":
    mcp.run(transport="sse")
