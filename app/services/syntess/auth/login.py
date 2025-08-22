from app.schemas.syntess.auth.login import LoginRequest
from app.services.syntess_service import syntess_request
from app.core.constants.headers import LOGIN_HEADERS

async def syntess_login(body: LoginRequest) -> dict:
    syntess_login_cookies = await get_cookies_with_login(body)
    asp_auth_cookie = await get_asp_auth_cookie(syntess_login_cookies)
    credentials = {
        "syntess_login_cookies": syntess_login_cookies,
        "asp_auth_cookie": asp_auth_cookie,
    }
    return credentials


async def get_cookies_with_login(body: LoginRequest) -> dict:

    endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"

    get_administraties_payload = {
        "parameters": {
            "method": "GetAdministraties",
            "username": body.username,
            "password": body.password,
        }
    }

    get_administraties_response = await syntess_request(endpoint,LOGIN_HEADERS, get_administraties_payload, None)

    return get_administraties_response.cookies


async def get_asp_auth_cookie(syntess_login_cookies: dict) -> dict:
    
    endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"

    get_asp_auth_cookie_payload = {
        "parameters": {
            "method": "LoginInAdministratie",
            "admincode": "1",
        },
    }

    get_asp_auth_cookie_response = await syntess_request(endpoint,LOGIN_HEADERS, get_asp_auth_cookie_payload, syntess_login_cookies)
    print("get_asp_auth_cookie_response", get_asp_auth_cookie_response)
    print(get_asp_auth_cookie_response.json())
    print(get_asp_auth_cookie_response.cookies)
    

    asp_auth_cookie = AspxAuthCookie(aspx_auth_cookie=get_asp_auth_cookie_response.get("aspx_auth_cookie"))

    return asp_auth_cookie
