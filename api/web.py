from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .routes import *


app = FastAPI(
    title="Auto Line Feeding", 
    docs_url="/auth-doc",
    description="Backend API's for Auto Line Feeding System"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


app.include_router(users_router, prefix="/auth", tags=["users"])
