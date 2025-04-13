from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from mcp.server.sse import SseServerTransport
from tools import mcp

app = FastAPI(
    title="MCP Assistant",
    description="Minimal FastAPI + MCP personal assistant",
    version="0.1.0",
)

# ✅ Mount the static frontend directory
app.mount("/webapp", StaticFiles(directory="webapp"), name="webapp")

# ✅ Set up SSE server transport
sse = SseServerTransport("/messages/")

# ✅ Register POST handler for tool calls
app.router.routes.append(sse.as_route())  # ← this is the key fix

# ✅ Handle GET /sse to connect the EventStream
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
