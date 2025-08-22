from app.services.syntess.auth.login import syntess_login, get_cookies_with_login, get_asp_auth_cookie
from app.core.constants.headers import LOGIN_HEADERS
from app.schemas.syntess.auth.login import LoginRequest
import asyncio

login_request = LoginRequest(username="TH", password="TH")

cookies = asyncio.run(syntess_login(login_request))



login_request = LoginRequest(username="TH", password="TH")

cookies = asyncio.run(get_cookies_with_login(login_request))

print(cookies)

asp_auth_cookie = asyncio.run(get_asp_auth_cookie(cookies))
# async def get_syntess_cookies():
#     endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"
#     get_administraties_payload = {
#         "parameters": {
#             "method": "GetAdministraties",
#             "username": "TH",
#             "password": "TH",
#         }
#     }
#     response = await syntess_login_request(
#         endpoint, LOGIN_HEADERS, get_administraties_payload, None
#     )
#     return response


cookies = asyncio.run(get_syntess_cookies())


# cookies = {'Atrium_ASP.NET_SessionId': 'm5rvntwpym3nfvjkdohln03i', 'Userinfo443': 'Info=zCynxqr5MyRO6KfD1032pKsxwLjvLbKevvkc1DRqgxm0osPqkX83rDovB7OzJlE6GaV57OSAxFAe_-J2ymkDd4JkFzpPGfa_P-BXIMgvbrKDWDapan9_A1ftJNJJJm36tYeMLAfDWTWgT9oJNTcn39cdy8Rge1jvt8VgJSkdpKMh6MUX5_i4_0rc3N6tZSzm_qSaIfaplqqC9Wa9I0Lktzmyo-zFQ2Sog_4q0y4t6RoD-8fJKbqUdh3P1BhkZ7KVzDAXjvHwtn1nKqYB-JFnF1v0BTum4tY9MXVlSO-XefS1kzWJ7-LnGyR8CqP5xr--5PDcpldvN_yBXWgGfXOZbWZnQ9rNF14q_a8f1S7xhl7_TlYEyOc9hlNgNgz9ixf2D8sF7M2RTYkGM3a-4BB6WdZ4a8b89MTf', 'UqZBpD3n3kC5cAQ44Vo_': 'v1KiEzJQ__4tN'}

async def get_asp_auth_cookie(syntess_login_cookies):
    endpoint = "Forms/Public/Login.aspx/ExecuteWebMethod"
    get_asp_auth_cookie_payload = {
        "parameters": {
            "method": "LoginInAdministratie",
            "admincode": "1",
        },
    }
    get_asp_auth_cookie_response = await syntess_request(
        endpoint, LOGIN_HEADERS, get_asp_auth_cookie_payload, syntess_login_cookies
    )
    print("get_asp_auth_cookie_response", get_asp_auth_cookie_response)
    return get_asp_auth_cookie_response


result = asyncio.run(get_asp_auth_cookie(cookies))

import requests

url = "http://localhost:8001/api/files/upload"

file_1_path = "/Users/chriszuidema/projects/github_migration/github_repos/hinfelaar_fastapi/file1.pdf"
file_2_path = "/Users/chriszuidema/projects/github_migration/github_repos/hinfelaar_fastapi/ed.jpg"

files = [
    ("file", ("file1.pdf", open(file_1_path, "rb"), "application/pdf")),
    ("file", ("ed.jpg", open(file_2_path, "rb"), "image/jpg")),
]

data = {
    "sessionId": "123",
    "documentId": "456",
}

response = requests.post(url, data=data, files=files)

print(response.status_code)
print(response.text)


import asyncio
from tortoise import Tortoise
from app.models import TORTOISE_ORM
from app.models.checklist import AnswerType


async def main():
    await Tortoise.init(config=TORTOISE_ORM)
    # Optional if tables aren’t created yet:
    # await Tortoise.generate_schemas()
    rows = await AnswerType.all().values()  # or .all() for model instances
    print(rows)
    await Tortoise.close_connections()


asyncio.run(main())


import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

response = requests.get(
    f"{API_BASE_URL}/checklist/answer-types",
    timeout=30,
)
print("API get answer types status:", response.status_code)
print("API get answer types response:", response.text)

response = requests.post(
    f"{API_BASE_URL}/syntess/login",
    json={"username": "TH", "password": "TH"},
    timeout=30,
)


print("API login status:", response.status_code)
print("API login response:", response.text)

cookie_dict = {
    name: response.cookies.get(name)
    for name in ["syntess_auth", "atrium_session", "userinfo", "uq_token"]
}
print("Cookies:", cookie_dict)


response = requests.post(
    f"{API_BASE_URL}/syntess/get-session-records",
    timeout=30,
    cookies=cookie_dict,
)

print("API get session records status:", response.status_code)
print("API get session records response:", response.text)
