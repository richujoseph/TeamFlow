import functools
import logging
from core.exceptions import AuthenticationError, PermissionDeniedError

logger = logging.getLogger(__name__)


def has_role(user, role_slug: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    if not user.role:
        return False
    return user.role.slug == role_slug


def has_permission(user, codename: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not user.role:
        return False
    return user.role.has_permission(codename)


def require_permission(codename: str):

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

    def decorator(func):

        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise AuthenticationError()
            if not any((has_role(request.user, slug) for slug in role_slugs)):
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
