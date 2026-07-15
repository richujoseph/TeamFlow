"""
TeamFlow EPMS — RBAC Permission Utilities.

Provides helper functions and decorators for the custom RBAC system.
These work with our Role → Permission M2M (not Django's PermissionsMixin).

Usage in Django Ninja endpoints:
    @router.get("/projects", auth=django_auth)
    @require_permission("project.view")
    def list_projects(request):
        ...

    @router.post("/projects", auth=django_auth)
    @require_role("administrator", "project_manager")
    def create_project(request, payload: ProjectCreateSchema):
        ...
"""

import functools
import logging

from core.exceptions import AuthenticationError, PermissionDeniedError

logger = logging.getLogger(__name__)


def has_role(user, role_slug: str) -> bool:
    """
    Check if the user's assigned role matches the given slug.

    Args:
        user: The Django User instance (must have a `role` FK).
        role_slug: The slug to check against (e.g., "administrator").

    Returns:
        True if the user's role slug matches, False otherwise.
    """
    if not user or not user.is_authenticated:
        return False
    if not user.role:
        return False
    return user.role.slug == role_slug


def has_permission(user, codename: str) -> bool:
    """
    Check if the user has a specific permission via their role.

    Superusers bypass all permission checks.
    Users without a role are denied all permissions.

    Args:
        user: The Django User instance.
        codename: Permission codename (e.g., "project.create").

    Returns:
        True if the user has the permission, False otherwise.
    """
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not user.role:
        return False
    return user.role.has_permission(codename)


def require_permission(codename: str):
    """
    Decorator for Django Ninja endpoints that enforces a specific permission.

    Raises PermissionDeniedError if the user lacks the required permission.

    Usage:
        @router.get("/projects")
        @require_permission("project.view")
        def list_projects(request):
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise AuthenticationError()
            if not has_permission(request.user, codename):
                logger.warning(
                    "Permission denied: user=%s, required=%s",
                    request.user.email,
                    codename,
                )
                raise PermissionDeniedError(
                    message=f"Missing required permission: {codename}",
                    details={"required_permission": codename},
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_role(*role_slugs: str):
    """
    Decorator for Django Ninja endpoints that enforces one of the given roles.

    Raises PermissionDeniedError if the user's role is not in the allowed list.

    Usage:
        @router.post("/admin/settings")
        @require_role("administrator")
        def update_settings(request, payload: SettingsSchema):
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise AuthenticationError()
            if not any(has_role(request.user, slug) for slug in role_slugs):
                logger.warning(
                    "Role denied: user=%s, required_roles=%s, actual_role=%s",
                    request.user.email,
                    role_slugs,
                    getattr(request.user.role, "slug", None),
                )
                raise PermissionDeniedError(
                    message="Your role does not have access to this resource.",
                    details={"required_roles": list(role_slugs)},
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
