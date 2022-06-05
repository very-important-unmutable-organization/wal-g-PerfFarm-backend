from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True


class TokenResponse(BaseModel):
    access_token: str


class ErrorInfoResponse(BaseModel):
    info: str
