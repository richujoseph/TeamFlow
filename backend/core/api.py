"""
TeamFlow EPMS — Master API Configuration.

Creates the NinjaAPI instance that serves as the single entry point
for all versioned API endpoints. Registers global exception handlers
and the health check endpoint.

Architecture:
- This module creates the `api` instance imported by config/urls.py
- Each Django app registers its own router via api.add_router()
- All endpoints live under /api/v1/
"""

from django.http import HttpRequest
from ninja import NinjaAPI

from core.exceptions import TeamFlowException
from core.schemas import ErrorResponse, HealthResponse

# ---------------------------------------------------------------------------
# API Instance
# ---------------------------------------------------------------------------
api = NinjaAPI(
    title="TeamFlow API",
    version="1.0.0",
    description=(
        "TeamFlow EPMS — Enterprise Project Management & Engineering "
        "Collaboration Platform API. Provides endpoints for project management, "
        "team coordination, task tracking, and engineering report generation."
    ),
    urls_namespace="api-v1",
)


# ---------------------------------------------------------------------------
# Global Exception Handlers
# ---------------------------------------------------------------------------
@api.exception_handler(TeamFlowException)
def teamflow_exception_handler(request: HttpRequest, exc: TeamFlowException):
    """
    Convert TeamFlowException subclasses into structured JSON responses.

    All custom exceptions (ValidationError, NotFoundError, etc.) flow through
    this handler, ensuring consistent error response format across the API.
    """
    return api.create_response(
        request,
        {
            "error": exc.message,
            "code": exc.error_code,
            "details": exc.details,
        },
        status=exc.status_code,
    )


# ---------------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------------
@api.get(
    "/health",
    response=HealthResponse,
    tags=["System"],
    summary="Health Check",
    description="Returns the current health status and API version.",
)
def health_check(request: HttpRequest) -> dict:
    """
    Health check endpoint for monitoring and load balancer probes.

    Returns a simple JSON response indicating the API is operational.
    This endpoint requires no authentication.
    """
    return {"status": "ok", "version": "1.0.0"}
