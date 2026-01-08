"""
Agentic Browser Backend - Main Application Entry Point.

This module initializes the FastAPI application and registers all API routers.
It serves as the single entry point for the entire backend service.

TODO:
- Add startup/shutdown event handlers for resource management
- Configure CORS middleware for frontend integration
- Add authentication middleware when ready
"""

from fastapi import FastAPI

from app.api.v1 import agent, browser, health, session

app = FastAPI(
    title="Agentic Browser Backend",
    description="A modular agent-based browser automation system",
    version="0.1.0",
)

# ──────────────────────────────────────────────────────────────────────────────
# API Router Registration
# ──────────────────────────────────────────────────────────────────────────────

app.include_router(health.router, tags=["Health"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(browser.router, prefix="/browser", tags=["Browser"])
app.include_router(session.router, prefix="/session", tags=["Session"])


# ──────────────────────────────────────────────────────────────────────────────
# Lifecycle Events
# ──────────────────────────────────────────────────────────────────────────────


@app.on_event("startup")
async def startup_event() -> None:
    """
    Application startup handler.

    TODO:
    - Initialize browser pool
    - Connect to databases/caches
    - Set up observability (tracing, logging)
    """
    pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Application shutdown handler.

    TODO:
    - Close browser connections gracefully
    - Flush pending logs/traces
    - Clean up resources
    """
    pass
