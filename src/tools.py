from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PersonalAssistant")

# In-memory task list
TASKS = []

@mcp.tool()
def add_task(task: str) -> str:
    """Add a task to your personal to-do list."""
    TASKS.append(task)
    return f"Task added: {task}"

@mcp.tool()
def list_tasks() -> str:
    """List all saved tasks."""
    return "\n".join(f"- {t}" for t in TASKS) or "No tasks yet."

@mcp.tool()
def summarize_text(text: str) -> str:
    """Summarize a block of text."""
    if len(text) < 20:
        return "Text is too short to summarize."
    return f"Summary: {text[:80]}..."
