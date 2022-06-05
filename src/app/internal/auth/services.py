from typing import Optional

from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.internal.auth.models import User, UserBase
from app.internal.core.enums import ServiceEnum


class UserService:
    @staticmethod
    async def search_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
        query = await session.execute(select(User).where(User.username == username))
        user = query.scalars().first()

        return user

    async def registration_user(self, session: AsyncSession, user_data: UserBase):
        user = await self.search_user_by_username(session, user_data.username)
        if user:
            return ServiceEnum.USER_IS_EXIST

        user_data.password = pbkdf2_sha256.hash(user_data.password)
        user = User(username=user_data.username, password=user_data.password)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        if user:
            return ServiceEnum.CREATED
        else:
            return ServiceEnum.NOT_CREATED

    async def login_user(self, session: AsyncSession, user_data: UserBase):
        user = await self.search_user_by_username(session, user_data.username)
        if not user:
            return ServiceEnum.USER_NOT_EXIST

        if pbkdf2_sha256.verify(user_data.password, user.password):
            return ServiceEnum.LOGIN
        else:
            return ServiceEnum.USER_NOT_EXIST
