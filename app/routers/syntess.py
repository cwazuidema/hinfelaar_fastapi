from fastapi import APIRouter, HTTPException, Response, Request
from datetime import datetime

from app.schemas.syntess.auth.login import LoginRequest
from app.services.syntess.auth.login import syntess_login


router = APIRouter()


@router.post("/login")
async def login(body: LoginRequest, response: Response) -> dict:
    print("syntess_login", body)

    cookies = await syntess_login(body)
    print("cookies", cookies)

    # Map Syntess cookie aliases to our app's cookie names and set them on the response
    aspxauth_cookie = cookies.get('syntess_auth')
    atrium_session = cookies.get("atrium_session")
    userinfo = cookies.get("userinfo")
    uq_token = cookies.get("uq_token")

    if aspxauth_cookie:
        response.set_cookie(
            key="syntess_auth",
            value=aspxauth_cookie,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    if atrium_session:
        response.set_cookie(
            key="atrium_session",
            value=atrium_session,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    if userinfo:
        response.set_cookie(
            key="userinfo",
            value=userinfo,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    if uq_token:
        response.set_cookie(
            key="uq_token",
            value=uq_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

    return {"message": "Login successful"}


# @router.post("/get-session-records")
# def get_session_records(request: Request):
#     print("get_session_records", request.cookies)

#     json_payload = {
#         "parameters": {
#             "method": "GetSessieRecords",
#             "zoekWaarde": "",
#             "zoekVelden": [],
#             "fromIndex": 0,
#             "pageSize": 500,
#             "datumVandaagClient": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         },
#     }

#     result = work_order_request("GetSessieRecords", json_payload, request.cookies)

#     if not result.get("success", False):
#         raise HTTPException(status_code=result.get("status", 500), detail=result)

#     return result
