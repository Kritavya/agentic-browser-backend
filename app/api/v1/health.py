"""
Health Check Endpoint.

Provides a simple health check endpoint for monitoring and load balancer probes.
This endpoint should always return immediately without any heavy processing.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: A simple status object indicating the service is running.

    TODO:
    - Add dependency health checks (database, browser pool, etc.)
    - Return detailed health info for debugging
    """
    return {"status": "ok"}
