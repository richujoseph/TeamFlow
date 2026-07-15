"""
TeamFlow EPMS — Custom Exception Hierarchy.

All TeamFlow exceptions inherit from TeamFlowException and carry:
- message: Human-readable error description
- error_code: Machine-readable error code (e.g., "VALIDATION_ERROR")
- status_code: HTTP status code to return

The teamflow_exception_handler registers with Django Ninja to convert
these exceptions into structured JSON error responses.
"""

from http import HTTPStatus


class TeamFlowException(Exception):
    """Base exception for all TeamFlow application errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        details: dict | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(TeamFlowException):
    """Raised when input data fails validation."""

    def __init__(
        self,
        message: str = "Validation failed.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )


class NotFoundError(TeamFlowException):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
            details=details,
        )


class PermissionDeniedError(TeamFlowException):
    """Raised when a user lacks the required permission."""

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            error_code="PERMISSION_DENIED",
            status_code=HTTPStatus.FORBIDDEN,
            details=details,
        )


class AuthenticationError(TeamFlowException):
    """Raised when authentication fails or credentials are invalid."""

    def __init__(
        self,
        message: str = "Authentication required.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=HTTPStatus.UNAUTHORIZED,
            details=details,
        )


class ConflictError(TeamFlowException):
    """Raised when an operation conflicts with existing state."""

    def __init__(
        self,
        message: str = "Operation conflicts with existing data.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=HTTPStatus.CONFLICT,
            details=details,
        )
