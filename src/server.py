"""
AGency — Minimal FastAPI entrypoint for Registry-as-a-Tool architecture.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .__init__ import __project__, __version__

app = FastAPI(
    title=__project__,
    description="Registry-as-a-Tool · Zero Context Bloat — Multi-agent orchestration platform",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"project": __project__, "version": __version__, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/registry")
async def registry():
    """Return the tool registry (schema-only, no payloads)."""
    return {
        "tools": [
            {"name": "route_agent", "description": "Route a query to the best-matching agent"},
            {"name": "search_memory", "description": "Search persistent memory graph"},
            {"name": "get_state_ref", "description": "Resolve a lightweight state reference"},
        ],
        "paradigm": "Registry-as-a-Tool",
        "bloat_level": "zero",
    }


@app.get("/info")
async def info():
    return {
        "project": __project__,
        "version": __version__,
        "architecture": "DAG-based multi-agent orchestration",
        "paradigm": "Registry-as-a-Tool / Zero Context Bloat",
        "license": "MIT",
    }
