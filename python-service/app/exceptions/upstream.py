from typing import Annotated, Any, Optional


class UpstreamServiceError(Exception):
    def __init__(self, service: str, message: str, details: dict | None = None) -> None:
        self.service = service
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NBAAPIError(UpstreamServiceError):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(service="nba_api", message=message, details=details)
