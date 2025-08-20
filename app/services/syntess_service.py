import requests

from app.schemas.syntess import LoginRequest, SyntessLoginCookies


SYNTESS_URL = "https://webapp.syntess.net/Syntess.Atrium.ASP/7.1.0266/Forms/Public/Login.aspx/ExecuteWebMethod"

SYNTESS_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://webapp.syntess.net",
    "Referer": "https://webapp.syntess.net/Syntess.Atrium.ASP/7.1.0266/Forms/Public/Login.aspx?installateur=qA8muMF8Ivk&db=xVSHhXqiNC4&epu=cyks_5AiBFj3VqW13UoqsmbI970p0vNI4mCwSa2WY1JprdyqJXR-0dfNkqAQ5TpDemfuI8_U200&iepu=K477o5IVBBs4eYAtJs052Q&bd=Z5PukDKGmblaPunC7pccWXruNKRgvWLI&rm=Z3sUzwZZebg",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest',
    'X-WebMethod': 'GetAdministraties',
}

def perform_syntess_login(body: LoginRequest) -> SyntessLoginCookies:
    print("perform_syntess_login", body)
    get_administraties_payload = {
        "parameters": {
            "method": "GetAdministraties",
            "username": body.username,
            "password": body.password,
        }
    }

    get_administraties_response = requests.post(
        SYNTESS_URL,
        headers=SYNTESS_HEADERS,
        json=get_administraties_payload,
    )
    administratie_cookies = get_administraties_response.cookies
    print("administratie_cookies", administratie_cookies)

    login_payload = {
        "parameters": {
            "method": "LoginInAdministratie",
            "admincode": "1",
        }
    }

    login_response = requests.post(
        SYNTESS_URL,
        headers=SYNTESS_HEADERS,
        json=login_payload,
        cookies=administratie_cookies,
    )
    print("login_response", login_response.status_code)
    print("login_response.text", login_response.text)

    auth_cookie = login_response.cookies.get(".ASPXFORMSAUTH")

    return SyntessLoginCookies(
        aspx_auth_cookie=auth_cookie,
        atrium_session=administratie_cookies.get("Atrium_ASP.NET_SessionId"),
        userinfo=administratie_cookies.get("Userinfo443"),
        uq_token=administratie_cookies.get("UqZBpD3n3kC5cAQ44Vo_"),
    )