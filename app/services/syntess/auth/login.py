from app.schemas.syntess.auth.login import (
    LoginRequest,
    SyntessLoginCookies,
    SyntessAuthCookie,
    SyntessCookies,
)
from app.services.syntess_service import syntess_request, syntess_login_request
from app.core.constants.headers import LOGIN_HEADERS
import httpx


async def syntess_login(body: LoginRequest) -> SyntessCookies:
    print("syntess_login", body)

    syntess_login_cookies = await get_cookies_with_login(body)
    print("syntess_login_cookies", syntess_login_cookies)

    asp_auth_cookie = await get_asp_auth_cookie(syntess_login_cookies)
    print("asp_auth_cookie", asp_auth_cookie)

    syntess_cookies = SyntessCookies(
        login_cookies=syntess_login_cookies,
        auth_cookie=asp_auth_cookie,
    )

    syntess_cookies_dict = {
        **syntess_cookies.login_cookies.model_dump(by_alias=True),
        **syntess_cookies.auth_cookie.model_dump(by_alias=True),
    }

    return syntess_cookies_dict


async def get_cookies_with_login(body: LoginRequest) -> SyntessLoginCookies:

    endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"

    get_administraties_payload = {
        "parameters": {
            "method": "GetAdministraties",
            "username": body.username,
            "password": body.password,
        }
    }

    get_administraties_response = await syntess_login_request(
        endpoint, LOGIN_HEADERS, get_administraties_payload, None
    )

    if not isinstance(get_administraties_response, httpx.Response):
        raise RuntimeError(f"Login failed: {get_administraties_response}")

    cookies = SyntessLoginCookies(**get_administraties_response.cookies)

    print("cookies", cookies)

    return cookies


async def get_asp_auth_cookie(cookies: SyntessLoginCookies) -> SyntessAuthCookie:

    endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"

    get_asp_auth_cookie_payload = {
        "parameters": {
            "method": "LoginInAdministratie",
            "admincode": "1",
        },
    }

    # Please check SyntessLoginCookies schema, we need to use alias in this call
    cookies = cookies.model_dump(by_alias=True)

    get_asp_auth_cookie_response = await syntess_login_request(
        endpoint, LOGIN_HEADERS, get_asp_auth_cookie_payload, cookies
    )

    if not isinstance(get_asp_auth_cookie_response, httpx.Response):
        raise RuntimeError(
            f"Failed to obtain ASP auth cookie: {get_asp_auth_cookie_response}"
        )

    syntess_auth_cookie = SyntessAuthCookie(**get_asp_auth_cookie_response.cookies)

    return syntess_auth_cookie
