from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from common.logger import logger
from modules.access.api.routes import router as access_router
from modules.list.api.routes import router as list_router
from modules.register.api.routes import router as register_router
from modules.update.api.routes import router as update_router
from modules.delete.api.routes import router as delete_router
from middleware.error_handler import setup_error_handlers
from config.settings import settings
import uvicorn


log = logger("main")


def create_app() -> FastAPI:
    log.info("Initializing FastAPI application")

    app = FastAPI(
        title="Auto Line Feeding API",
        description="Auth microservice responsible for powering the authentication to CIAL system",
        docs_url="/auth-docs",
    )

    setup_error_handlers(app)

    log.debug("Adding CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000
    )

    log.debug("Registering register routes")
    app.include_router(register_router, prefix="/user/register", tags=["register"])
    
    log.debug("Registering list routes")
    app.include_router(list_router, prefix="/admin", tags=["list"])

    log.debug("Registering access routes")
    app.include_router(access_router, prefix="/user/access", tags=["access"])

    log.debug("Registering update routes")
    app.include_router(update_router, prefix="/admin/update", tags=["update"])

    log.debug("Registering delete routes")
    app.include_router(delete_router, prefix="/admin/delete", tags=["delete"])

    log.info("FastAPI application initialized successfully")
    return app


app = create_app()


if __name__ == "__main__":
    log.info("Starting Uvicorn server (127.0.0.1:8004, reload=True)")
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8003,
            reload=True
        )
    except Exception as e:
        log.error(f"Uvicorn server failed: {str(e)}", exc_info=True)
        raise


# -- ROUTE FOR HEALTH CHECK --
@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}