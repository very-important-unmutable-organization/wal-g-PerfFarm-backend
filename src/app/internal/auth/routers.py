from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.internal.auth.models import User, UserBase
from app.internal.auth.services import UserService
from app.internal.core.db import get_session
from app.internal.core.dependencies import get_user_service
from app.internal.core.enums import ServiceEnum
from app.pkg.auth.auth_handler import signJWT
from app.pkg.responses import ErrorInfoResponse, TokenResponse

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post(
    "/registration", status_code=201, responses={201: {"model": TokenResponse}, 400: {"model": ErrorInfoResponse}}
)
async def registration_user_view(
    user_data: UserBase = Body(...),
    session: AsyncSession = Depends(get_session),
    user_data_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    result = await user_data_service.registration_user(session, user_data)

    if result == ServiceEnum.CREATED:
        return JSONResponse(status_code=201, content={"access_token": signJWT(user_data.username)})
    else:
        return JSONResponse(status_code=400, content={"info": result.value})


@auth_router.post(
    "/login", status_code=200, responses={200: {"model": TokenResponse}, 400: {"model": ErrorInfoResponse}}
)
async def login_user_view(
    user_data: UserBase = Body(...),
    session: AsyncSession = Depends(get_session),
    user_data_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    result = await user_data_service.login_user(session, user_data)

    if result == ServiceEnum.LOGIN:
        return JSONResponse(status_code=200, content={"access_token": signJWT(user_data.username)})
    else:
        return JSONResponse(status_code=400, content={"info": result.value})
