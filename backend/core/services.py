"""
TeamFlow EPMS — Base Service Class.

Establishes the service-layer pattern used across all TeamFlow apps.
All domain services inherit from BaseService to get:
- User context (the authenticated user making the request)
- Permission checking helpers
- Consistent interface

Architecture rule: API endpoints delegate ALL business logic to service classes.
Services are the only layer that interacts with models/ORM directly.

Usage:
    class ProjectService(BaseService):
        def create_project(self, data: ProjectCreateSchema) -> Project:
            self._check_permission("project.create")
            project = Project.objects.create(**data.dict(), owner=self.user)
            return project
"""

import logging

from core.exceptions import AuthenticationError, PermissionDeniedError
from core.permissions import has_permission

logger = logging.getLogger(__name__)


class BaseService:
    """
    Base class for all TeamFlow service classes.

    Provides user context and permission-checking helpers.
    Subclasses implement domain-specific business logic.
    """

    def __init__(self, user=None):
        """
        Initialize the service with user context.

        Args:
            user: The authenticated Django User instance. May be None
                  for public/anonymous operations.
        """
        self.user = user

    def _check_authenticated(self):
        """
        Ensure the user is authenticated.

        Raises:
            AuthenticationError: If user is None or not authenticated.
        """
        if not self.user or not self.user.is_authenticated:
            raise AuthenticationError(
                message="You must be logged in to perform this action."
            )

    def _check_permission(self, codename: str):
        """
        Verify the user has the required permission.

        This delegates to the RBAC system (Role → Permission M2M).
        Superusers bypass all permission checks.

        Args:
            codename: Permission codename to check (e.g., "project.create").

        Raises:
            AuthenticationError: If user is not authenticated.
            PermissionDeniedError: If user lacks the required permission.
        """
        self._check_authenticated()
        if not has_permission(self.user, codename):
            logger.warning(
                "Service permission denied: user=%s, permission=%s, service=%s",
                self.user.email,
                codename,
                self.__class__.__name__,
            )
            raise PermissionDeniedError(
                message=f"Missing required permission: {codename}",
                details={"required_permission": codename},
            )

    def _check_owner_or_permission(self, owner_id, codename: str):
        """
        Allow access if the user is the owner OR has the given permission.

        Useful for endpoints where users can manage their own resources
        but admins/managers can manage anyone's resources.

        Args:
            owner_id: UUID of the resource owner.
            codename: Permission codename for non-owner access.

        Raises:
            AuthenticationError: If user is not authenticated.
            PermissionDeniedError: If user is not the owner and lacks permission.
        """
        self._check_authenticated()
        if str(self.user.id) == str(owner_id):
            return
        if not has_permission(self.user, codename):
            raise PermissionDeniedError(
                message="You can only access your own resources or need elevated permissions.",
                details={"required_permission": codename},
            )
