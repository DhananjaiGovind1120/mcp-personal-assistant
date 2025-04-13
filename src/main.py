from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route
from tools import mcp
from mcp.server.sse import SseServerTransport

# Initialize the app
app = FastAPI(
    title="MCP Assistant",
    description="Minimal FastAPI + MCP personal assistant",
    version="0.1.0",
)

# Mount static frontend at /webapp
app.mount("/webapp", StaticFiles(directory="webapp"), name="webapp")

# Initialize SSE transport
sse = SseServerTransport("/messages/")

# ✅ Define a POST route that wraps sse.handle_post_message
async def messages_endpoint(scope, receive, send):
    await sse.handle_post_message(scope, receive, send)

# ✅ Register the /messages POST endpoint
app.router.routes.append(
    Route("/messages/", endpoint=messages_endpoint, methods=["POST"])
)

# ✅ SSE connection handler
@app.get("/sse")
async def sse_handler(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options()
        )
