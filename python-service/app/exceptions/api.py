from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(
        self, status_code: int, code: str, message: str, details: dict | None = None
    ) -> None:
        self.code = code
        self.details = details or {}
        super().__init__(
            status_code=status_code,
            detail={"error": code, "message": message, "details": self.details},
        )


class GatewayError(APIException):
    def __init__(self, details: dict | None = None) -> None:
        super().__init__(
            status_code=500,
            code="Internal Server Error",
            message="The server could not complete your request.",
            details=details,
        )


class ResourceNotFound(APIException):
    def __init__(self, resource: str, details: dict | None = None) -> None:
        super().__init__(
            status_code=404,
            code="Resource Not Found Error",
            message=f"{resource} not found.",
            details=details,
        )
