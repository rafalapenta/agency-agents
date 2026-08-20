from fastapi import FastAPI

app = FastAPI(
    title="AGgency Router",
    version="0.1.0",
    description="Semantic registry and ephemeral execution hub for agency-agents.",
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Report process readiness without touching external dependencies."""
    return {"status": "ok", "service": "aggency-router"}
