"""
TeamFlow EPMS — Shared Pydantic Schemas.

Reusable response schemas used across all API endpoints.
These provide consistent response structure throughout the API.
"""

from typing import Any, Generic, TypeVar

from ninja import Field, Schema

T = TypeVar("T")


class HealthResponse(Schema):
    """Response for the /health endpoint."""

    status: str = Field(description="Service status ('ok' or 'error').")
    version: str = Field(description="API version string.")


class ErrorResponse(Schema):
    """Structured error response returned for all API errors."""

    error: str = Field(description="Human-readable error message.")
    code: str = Field(description="Machine-readable error code.")
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional error context (field errors, etc.).",
    )


class MessageResponse(Schema):
    """Simple message response for operations without data payloads."""

    message: str = Field(description="Human-readable status message.")


class PaginatedResponse(Schema):
    """
    Generic paginated response wrapper.

    Usage in endpoint return type:
        return PaginatedResponse(items=[...], meta={...})
    """

    items: list[Any] = Field(description="List of items on the current page.")
    meta: dict[str, Any] = Field(description="Pagination metadata.")
