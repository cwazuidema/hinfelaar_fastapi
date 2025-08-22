from fastapi import APIRouter

from app.schemas.syntess.auth.login import LoginRequest, SyntessCookies
from app.services.syntess.auth.login import syntess_login

router = APIRouter()


@router.post("/login", response_model=dict)
async def login(body: LoginRequest) -> dict:
    print("syntess_login", body)

    cookies = await syntess_login(body)
    print("cookies", cookies)

    return cookies
