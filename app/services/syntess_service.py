import httpx
from app.client.async_http_client import get_http_client
import json

BASE_URL = "https://webapp.syntess.net/Syntess.Atrium.ASP/7.1.0266/"


async def syntess_request(
    endpoint: str, headers: dict, payload: dict, cookies: dict | None
):
    print("cookies", cookies)
    client = await get_http_client()
    
    api_url = f"{BASE_URL}{endpoint}"

    try:
        response = await client.post(
            api_url,
            cookies=cookies,
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        api_response_data = response.json()

        if "d" in api_response_data and isinstance(api_response_data["d"], str):
            actual_data = json.loads(api_response_data["d"])
        else:
            actual_data = api_response_data.get("d")

        return {"success": True, "data": actual_data}

    except httpx.HTTPStatusError as e:
        error_message = str(e)
        status_code = e.response.status_code if e.response is not None else 500

        try:
            error_details = e.response.json() if e.response is not None else None
        except json.JSONDecodeError:
            error_details = e.response.text if e.response is not None else None

        return {
            "success": False,
            "error": error_message,
            "details": error_details,
            "status": status_code,
        }

    except httpx.RequestError as e:
        return {"success": False, "error": str(e), "status": 503}

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON decode error: {str(e)}",
        }

    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}


async def syntess_login_request(endpoint: str, headers: dict, payload: dict, cookies: dict | None):
    
    client = await get_http_client()
    
    api_url = f"{BASE_URL}{endpoint}"

    try:
        response = await client.post(
            api_url,
            cookies=cookies,
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        return response

    except httpx.HTTPStatusError as e:
        error_message = str(e)
        status_code = e.response.status_code if e.response is not None else 500

        try:
            error_details = e.response.json() if e.response is not None else None
        except json.JSONDecodeError:
            error_details = e.response.text if e.response is not None else None

        return {
            "success": False,
            "error": error_message,
            "details": error_details,
            "status": status_code,
        }

    except httpx.RequestError as e:
        return {"success": False, "error": str(e), "status": 503}

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON decode error: {str(e)}",
        }

    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}
