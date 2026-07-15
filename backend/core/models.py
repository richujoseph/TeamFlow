"""
TeamFlow EPMS — Abstract Base Models.

Provides two abstract model bases that all TeamFlow models should inherit from:

- BaseModel: Full-featured base with UUID primary key, timestamps, and soft-delete.
  Use for all domain entities (User, Project, Task, etc.)

- TimeStampedModel: Lightweight base with only created_at/updated_at.
  Use for through tables and auxiliary records (RolePermission, etc.)
"""

import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model for all TeamFlow domain entities.

    Provides:
    - UUID primary key (avoids sequential ID enumeration)
    - created_at / updated_at timestamps (auto-managed)
    - is_active flag (soft-delete support)
    - Default ordering by newest first
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier (UUID v4).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when this record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated.",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Soft-delete flag. Inactive records are excluded from default queries.",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        """Mark this record as inactive instead of hard-deleting."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])


class TimeStampedModel(models.Model):
    """
    Lightweight abstract base with only timestamps.

    Use for through tables (e.g., RolePermission) and auxiliary records
    that don't need UUID primary keys or soft-delete.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated.",
    )

    class Meta:
        abstract = True
