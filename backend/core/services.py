import logging
from core.exceptions import AuthenticationError, PermissionDeniedError
from core.permissions import has_permission

logger = logging.getLogger(__name__)


class BaseService:

    def __init__(self, user=None):
        self.user = user

    def _check_authenticated(self):
        if not self.user or not self.user.is_authenticated:
            raise AuthenticationError(
                message="You must be logged in to perform this action."
            )

    def _check_permission(self, codename: str):
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
        self._check_authenticated()
        if str(self.user.id) == str(owner_id):
            return
        if not has_permission(self.user, codename):
            raise PermissionDeniedError(
                message="You can only access your own resources or need elevated permissions.",
                details={"required_permission": codename},
            )
