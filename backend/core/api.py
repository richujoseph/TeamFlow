from django.http import HttpRequest
from ninja import NinjaAPI
from core.exceptions import TeamFlowException
from core.schemas import ErrorResponse, HealthResponse

api = NinjaAPI(
    title="TeamFlow API",
    version="1.0.0",
    description="TeamFlow EPMS — Enterprise Project Management & Engineering Collaboration Platform API. Provides endpoints for project management, team coordination, task tracking, and engineering report generation.",
    urls_namespace="api-v1",
)


@api.exception_handler(TeamFlowException)
def teamflow_exception_handler(request: HttpRequest, exc: TeamFlowException):
    return api.create_response(
        request,
        {"error": exc.message, "code": exc.error_code, "details": exc.details},
        status=exc.status_code,
    )


@api.get(
    "/health",
    response=HealthResponse,
    tags=["System"],
    summary="Health Check",
    description="Returns the current health status and API version.",
)
def health_check(request: HttpRequest) -> dict:
    return {"status": "ok", "version": "1.0.0"}
