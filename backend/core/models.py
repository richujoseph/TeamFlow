import uuid
from django.db import models


class BaseModel(models.Model):
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
        auto_now=True, help_text="Timestamp when this record was last updated."
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
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self):
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when this record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when this record was last updated."
    )

    class Meta:
        abstract = True
