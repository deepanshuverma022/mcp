import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from tools.generated_tools import register_tools
from tools.api_client import api_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("Website Security Auditor")

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
# and we mount the streamable HTTP app so the agent builder can access it.
try:
    mcp_app = mcp.streamable_http_app()
    app.mount("/", mcp_app)  # Mounting at root exposes the /mcp endpoint
except Exception as e:
    logger.error(f"Failed to mount streamable HTTP app: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await api_client.close()

if __name__ == "__main__":
    # Start the server locally as explicitly requested:
    # mcp.run(transport="streamable-http")
    try:
        mcp.run(transport="streamable-http")
    except ValueError as e:
        logger.error("streamable-http transport not found, falling back to 'sse'")
        mcp.run(transport="sse")
