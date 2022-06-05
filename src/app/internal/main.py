from fastapi import FastAPI

from app.internal.auth.routers import auth_router
from app.internal.runs.routers import runs_router

app = FastAPI()


app.include_router(auth_router, prefix="/api")
app.include_router(runs_router, prefix="/api")
