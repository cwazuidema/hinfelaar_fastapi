from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool


class SyntessLoginCookies(BaseModel):
    aspx_auth_cookie: str | None
    atrium_session: str | None
    userinfo: str | None
    uq_token: str | None
