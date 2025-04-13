from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Assistant")

TASKS = []

@mcp.tool()
def add_task(task: str) -> str:
    TASKS.append(task)
    return f"Task added: {task}"

@mcp.tool()
def list_tasks() -> str:
    return "\n".join(f"- {t}" for t in TASKS) or "No tasks yet."

@mcp.tool()
def summarize_text(text: str) -> str:
    if len(text) < 20:
        return "Text is too short to summarize."
    return f"Summary: {text[:80]}..."
