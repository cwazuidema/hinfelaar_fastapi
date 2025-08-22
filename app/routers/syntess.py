from fastapi import APIRouter, HTTPException, Response, Request
from datetime import datetime

from app.schemas.syntess.auth.login import LoginRequest
from app.services.syntess.auth.login import syntess_login


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


@router.post("/login")
def login(body: LoginRequest, response: Response) -> dict:
    print("syntess_login", body)

    cookies = syntess_login(body)
    print("cookies", cookies)

    for cookie_name, attr in COOKIE_MAP:
        _set_cookie_if_present(response, cookie_name, getattr(cookies, attr))

    return cookies


@router.post("/get-session-records")
def get_session_records(request: Request):
    print("get_session_records", request.cookies)

    json_payload = {
        "parameters": {
            "method": "GetSessieRecords",
            "zoekWaarde": "",
            "zoekVelden": [],
            "fromIndex": 0,
            "pageSize": 500,
            "datumVandaagClient": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    }
    
    result = work_order_request("GetSessieRecords", json_payload, request.cookies)
    
    if not result.get("success", False):
        raise HTTPException(status_code=result.get("status", 500), detail=result)
    
    return result
