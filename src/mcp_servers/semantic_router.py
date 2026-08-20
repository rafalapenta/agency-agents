from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from src.macro_agents.orchestrator import MacroOrchestrator
from src.router.semantic import RouteAgentResult
from src.router.semantic import route_agent as semantic_route_agent

RouterCallable = Callable[[str, float], RouteAgentResult]


def create_mcp(router: RouterCallable | None = None) -> FastMCP:
    if router is None:
        database_url = os.getenv('AGGENCY_DATABASE_URL', 'sqlite:///agency_agents.db')
        chroma_path = Path(os.getenv('AGGENCY_CHROMA_PATH', 'chroma'))
        source_root = Path(os.getenv('AGGENCY_CATALOG_ROOT', r'C:\Users\RAFAEL\Documents\R!\Obsidian Memory\raw\agency-agents'))

        def configured_router(query: str, threshold: float) -> RouteAgentResult:
            return semantic_route_agent(
                query=query,
                threshold=threshold,
                database_url=database_url,
                chroma_path=chroma_path,
                source_root=source_root,
            )

        selected_router = configured_router
    else:
        selected_router = router

    server = FastMCP('AGgency Semantic Router')

    @server.tool
    def route_agent(query: str, threshold: float = 0.25) -> dict:
        """Route a query to the best-matching domain agent."""
        result = selected_router(query, threshold)
        return result.model_dump(mode='json')

    @server.tool
    def orchestrate(
        title: str,
        query: str,
        body: str = '',
        priority: str = 'medium',
        assignee: str = '',
        source_agent: str = 'system',
    ) -> dict[str, Any]:
        """Run the full macro orchestration loop for a new task.

        Creates a task, routes it to the best domain agent, compresses
        context, performs handoff, and validates quality gates.
        """
        state_dir = Path(os.getenv('AGGENCY_STATE_DIR', 'state_data'))

        orch = MacroOrchestrator(
            state_dir=state_dir,
            database_url=os.getenv('AGGENCY_DATABASE_URL', 'sqlite:///agency_agents.db'),
            chroma_path=Path(os.getenv('AGGENCY_CHROMA_PATH', 'chroma')),
            source_root=Path(os.getenv(
                'AGGENCY_CATALOG_ROOT',
                r'C:\Users\RAFAEL\Documents\R!\Obsidian Memory\raw\agency-agents',
            )),
        )

        result = orch.orchestrate(
            title=title,
            body=body,
            query=query,
            priority=priority,
            assignee=assignee,
            source_agent=source_agent,
        )
        return result.to_dict()

    return server


mcp = create_mcp()

if __name__ == '__main__':
    mcp.run()
