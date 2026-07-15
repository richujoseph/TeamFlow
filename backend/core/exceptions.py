from http import HTTPStatus


class TeamFlowException(Exception):

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

    def __init__(
        self, message: str = "Validation failed.", details: dict | None = None
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )


class NotFoundError(TeamFlowException):

    def __init__(
        self, message: str = "Resource not found.", details: dict | None = None
    ):
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
            details=details,
        )


class PermissionDeniedError(TeamFlowException):

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

    def __init__(
        self, message: str = "Authentication required.", details: dict | None = None
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=HTTPStatus.UNAUTHORIZED,
            details=details,
        )


class ConflictError(TeamFlowException):

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
