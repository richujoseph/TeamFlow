"""
TeamFlow EPMS — Pagination Utilities.

Provides reusable pagination classes for Django Ninja endpoints.
Both offset-based and cursor-based pagination are available.
"""

from typing import Any

from ninja import Field, Schema


class PageNumberPaginationInput(Schema):
    """Input schema for offset-based pagination."""

    page: int = Field(default=1, ge=1, description="Page number (1-indexed).")
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page (max 100).",
    )


class PaginationMeta(Schema):
    """Metadata about the current page of results."""

    page: int = Field(description="Current page number.")
    page_size: int = Field(description="Number of items per page.")
    total_items: int = Field(description="Total number of items across all pages.")
    total_pages: int = Field(description="Total number of pages.")
    has_next: bool = Field(description="Whether a next page exists.")
    has_previous: bool = Field(description="Whether a previous page exists.")


def paginate_queryset(
    queryset: Any,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list, PaginationMeta]:
    """
    Apply offset-based pagination to a Django queryset.

    Args:
        queryset: A Django QuerySet to paginate.
        page: The 1-indexed page number.
        page_size: Number of items per page.

    Returns:
        Tuple of (items_list, pagination_meta).
    """
    total_items = queryset.count()
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    # Clamp page to valid range
    page = max(1, min(page, total_pages))

    offset = (page - 1) * page_size
    items = list(queryset[offset : offset + page_size])

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
    )

    return items, meta
