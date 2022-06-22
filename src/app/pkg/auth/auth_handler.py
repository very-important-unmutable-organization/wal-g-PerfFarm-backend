import os
import time
from typing import Dict

import jwt

from app.pkg.utils import get_int_from_env

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
LIFE_TIME_JWT = get_int_from_env("LIFE_TIME_JWT", 600)


def signJWT(user_id: str) -> str:
    payload = {"user_id": user_id}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decodeJWT(token: str) -> Dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return {}
