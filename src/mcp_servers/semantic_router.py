"""FastMCP tool definitions for the AGency router."""

from fastmcp import FastMCP

from ..router import router

mcp = FastMCP("agency-router")


@mcp.tool()
def route_agent(query: str, threshold: float = 0.25) -> dict:
    """
    Route a query to the best-matching agent in the registry.
    Returns lightweight reference — no context bloat.
    """
    return router.route(query=query, threshold=threshold)


@mcp.tool()
def list_agents() -> list[str]:
    """List all registered agents in the registry."""
    return router.list_agents()
