from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.api import APIException
from app.exceptions.upstream import UpstreamServiceError


def register_exception_handlers(app):
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(UpstreamServiceError)
    async def upstream_exception_handler(request: Request, exc: UpstreamServiceError):
        return JSONResponse(
            status_code=503,
            content={
                "error": "Upstream Service Error",
                "message": f"{exc.service} failed.",
                "detail": exc.details,
            },
        )
