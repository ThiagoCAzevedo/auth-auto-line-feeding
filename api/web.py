from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .routes import *


app = FastAPI(
    title="Auth Auto Line Feeding", 
    docs_url="/auth-doc",
    description="Auth microservice for Auto Line Feeding System"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


app.include_router(register_router, prefix="/users/register", tags=["register"])
app.include_router(list_router, prefix="/users/list", tags=["list"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(update_router, prefix="/update", tags=["update"])
app.include_router(delete_router, prefix="/users", tags=["users"])