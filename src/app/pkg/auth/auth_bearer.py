from typing import Optional, Tuple

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.internal.auth.models import User
from app.internal.auth.services import UserService
from app.internal.core.db import engine, get_session
from app.pkg.auth.auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, user_service: UserService, auto_error: bool = True) -> None:
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self._user_service = user_service

    async def __call__(self, request: Request) -> Optional[User]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            (verify, user_id) = self.verify_jwt(credentials.credentials)

            if not verify:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

            async with async_session() as session:
                async with session.begin():
                    user = await self._user_service.search_user_by_username(session, user_id)

            if user:
                return user

            raise HTTPException(status_code=403, detail="Forbidden")

        else:
            raise HTTPException(status_code=403, detail="Invalid authorization  code.")

    def verify_jwt(self, jwtoken: str) -> Tuple[bool, str]:

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        return (bool(payload), payload["user_id"] if payload else None)
