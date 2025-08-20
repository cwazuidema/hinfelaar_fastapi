import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")

response = requests.post(
    f"{API_BASE_URL}/syntess/login",
    json={"username": "TH", "password": "TH"},
    timeout=30,
)

print("API login status:", response.status_code)
print("API login response:", response.text)

print("Cookies:")
for name in ["syntess_auth", "atrium_session", "userinfo", "uq_token"]:
    print(f"  {name}: {response.cookies.get(name)}")
