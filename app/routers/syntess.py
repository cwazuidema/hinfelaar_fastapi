from fastapi import APIRouter, HTTPException, Response

from app.schemas.syntess import LoginRequest, SyntessLoginCookies
from app.services.syntess_service import perform_syntess_login


router = APIRouter()


def _set_cookie_if_present(response: Response, name: str, value: str | None) -> None:
    if value:
        response.set_cookie(
            name,
            value,
            httponly=True,
            secure=True,
            samesite="Strict",
        )


COOKIE_MAP = [
    ("syntess_auth", "aspx_auth_cookie"),
    ("atrium_session", "atrium_session"),
    ("userinfo", "userinfo"),
    ("uq_token", "uq_token"),
]


@router.post("/login", response_model=SyntessLoginCookies)
def syntess_login(body: LoginRequest, response: Response) -> SyntessLoginCookies:
    print("syntess_login", body)

    cookies = perform_syntess_login(body)
    print("cookies", cookies)

    for cookie_name, attr in COOKIE_MAP:
        _set_cookie_if_present(response, cookie_name, getattr(cookies, attr))

    return cookies
