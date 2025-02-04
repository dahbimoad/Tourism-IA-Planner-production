# app/core/exception_handlers.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions and return properly formatted JSON responses
    """
    # Log the error
    logger.error(f"HTTP Exception: {exc.detail}")

    # Get any additional headers
    headers = getattr(exc, "headers", None)

    # Format the error response
    error_response = {
        "detail": exc.detail if isinstance(exc.detail, dict) else {
            "message": str(exc.detail),
            "code": f"ERROR_{exc.status_code}"
        }
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=headers
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation exceptions from pydantic models
    """
    # Log the error
    logger.error(f"Validation Error: {str(exc)}")

    # Extract error details
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": " -> ".join(str(x) for x in error["loc"]),
            "msg": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": {
                "message": "Validation error",
                "code": "VALIDATION_ERROR",
                "errors": errors
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle any unhandled exceptions
    """
    # Log the error
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "message": "Internal server error",
                "code": "INTERNAL_SERVER_ERROR",
                "error": str(exc)
            }
        }
    )