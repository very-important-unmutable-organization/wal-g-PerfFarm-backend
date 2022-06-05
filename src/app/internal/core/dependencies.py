from sqlmodel import Session

from app.internal.auth.services import UserService
from app.pkg.auth.auth_bearer import JWTBearer


def get_jwt_bearer():
    return JWTBearer(UserService())


def get_user_service():
    return UserService()
