from fastapi import APIRouter

from app.schemas.syntess import LoginRequest, SyntessLoginCookies
from app.services.syntess.auth.login import syntess_login

router = APIRouter()


@router.post("/login", response_model=SyntessLoginCookies)
def login(body: LoginRequest) -> SyntessLoginCookies:
    print("syntess_login", body)

    cookies = syntess_login(body)
    print("cookies", cookies)

    return 
