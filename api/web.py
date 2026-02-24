from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .routes import *


app = FastAPI(
    title="Auth Auto Line Feeding", 
    docs_url="/auth-doc",
    description="Auth microservice for Auto Line Feeding System"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# -- DEFAULT ROUTES --
app.include_router(default_routes, prefix="/user", tags=["default"])
app.include_router(register_router, prefix="/user/register", tags=["register"])
app.include_router(login_router, prefix="/user/login", tags=["login"])
app.include_router(logout_router, prefix="/user/logout", tags=["logout"])


# -- ADMIN ROUTES --
app.include_router(list_router, prefix="/admin", tags=["list"])
app.include_router(update_router, prefix="/admin/update", tags=["update"])
app.include_router(delete_router, prefix="/admin/delete", tags=["delete"])