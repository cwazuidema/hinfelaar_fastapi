from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool


class SyntessLoginCookies(BaseModel):
    atrium_session: str = Field(alias="Atrium_ASP.NET_SessionId")
    userinfo: str = Field(alias="Userinfo443")
    uq_token: str = Field(alias="UqZBpD3n3kC5cAQ44Vo_")
    
    
class SyntessAuthCookie(BaseModel):
    syntess_auth: str = Field(alias=".ASPXFORMSAUTH")
    

class SyntessCookies(BaseModel):
    login_cookies: SyntessLoginCookies
    auth_cookie: SyntessAuthCookie
    