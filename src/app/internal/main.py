from fastapi import FastAPI

from app.internal.auth.routers import auth_router
from app.internal.runs.routers import runs_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api")
app.include_router(runs_router, prefix="/api")
