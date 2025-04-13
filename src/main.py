from fastapi import FastAPI, Request
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from tools import mcp

app = FastAPI(
    title="MCP Assistant",
    description="Minimal FastAPI + MCP personal assistant",
    version="0.1.0",
)

# Set up SSE server
sse = SseServerTransport("/messages/")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))


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
