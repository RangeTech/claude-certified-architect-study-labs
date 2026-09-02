"""D2 sandbox — a minimal stdio MCP server exposing two tools.

Wire it into Claude Code with the sibling `.mcp.json` (project scope). See README.

    pip install "mcp[cli]"
    # quick standalone smoke test (Ctrl-C to exit; it speaks MCP over stdio):
    python mcp_server.py

Exam point: MCP lets you expose tools/resources to Claude over a standard
protocol. In Claude Code, servers are configured at a scope — local (this machine
only), project (committed `.mcp.json`, shared via git), or user (all your projects).
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cca-sandbox")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


@mcp.tool()
def echo(text: str) -> str:
    """Echo the given text back unchanged."""
    return text


if __name__ == "__main__":
    mcp.run()  # stdio transport
