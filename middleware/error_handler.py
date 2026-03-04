from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from common.logger import logger


log = logger("error_handler")


async def global_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


def setup_error_handlers(app: FastAPI):
    app.add_exception_handler(Exception, global_exception_handler)