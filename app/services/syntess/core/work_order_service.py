import requests
import json

# TODO: Chris: do we need to make version a variable? "Syntess.Atrium.ASP/7.1.0162/Forms"


def work_order_request(xwebmethod: str, payload: dict, cookies: dict) -> dict:
    """
    Make a request to the Syntess external API for work order operations.

    Args:
        xwebmethod: The web method to call on the external API
        payload: JSON payload to send with the request
        cookies: Authentication/session cookies required for API access

    Returns:
        dict: { "success": True, "data": any } on success, otherwise
              { "success": False, "error": str, "details"?: any, "status"?: int }
    """

    # Cookies required for API authentication and session management
    COOKIES = {
        "UqZBpD3n3kC5cAQ44Vo_": cookies.get("uq_token"),
        "Atrium_ASP.NET_SessionId": cookies.get("atrium_session"),
        "Userinfo443": cookies.get("userinfo"),
        ".ASPXFORMSAUTH": cookies.get("syntess_auth"),
    }

    # HTTP headers required by the Syntess API
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://webapp.syntess.net",
        "Referer": "https://webapp.syntess.net/Syntess.Atrium.ASP/7.1.0266/Forms/Werkbonnen/Werkbonnen_Pagina.aspx",
        "X-WebMethod": xwebmethod,  # Specifies which API method to call
    }

    # Prepare the JSON payload for the request
    json_payload = payload

    # Syntess API endpoint for work order operations
    api_url = "https://webapp.syntess.net/Syntess.Atrium.ASP/7.1.0266/Forms/Werkbonnen/Werkbonnen_Pagina.aspx/ExecuteWebMethod"

    try:
        # Make the POST request to the external API
        response = requests.post(
            api_url,
            cookies=COOKIES,
            headers=HEADERS,
            json=json_payload,
            timeout=10,  # 10 second timeout to prevent hanging requests
        )
        # Raise an exception for HTTP error status codes (4xx, 5xx)
        response.raise_for_status()

        # Parse the JSON response from the API
        api_response_data = response.json()

        # Extract the actual data from the nested response structure
        # The Syntess API wraps response data in a 'd' property, sometimes as a JSON string
        if "d" in api_response_data and isinstance(api_response_data["d"], str):
            # If 'd' contains a JSON string, parse it to get the actual data
            actual_data = json.loads(api_response_data["d"])
        else:
            # If 'd' is already an object, use it directly
            actual_data = api_response_data.get("d")

        # Return successful response with the extracted data
        return {"success": True, "data": actual_data}

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 401 Unauthorized, 404 Not Found, 500 Internal Server Error)
        error_message = str(e)
        status_code = e.response.status_code if e.response is not None else 500

        # Try to extract error details from the API response
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

    except requests.exceptions.RequestException as e:
        # Handle other request-related errors (connection errors, timeouts, etc.)
        return {"success": False, "error": str(e), "status": 503}

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors when the response isn't valid JSON
        return {
            "success": False,
            "error": f"JSON decode error: {str(e)}",
            "raw_response": (
                response.text if "response" in locals() else "No response"
            ),
            "status": 500,
        }

    except Exception as e:
        # Handle any other unexpected errors
        return {
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}",
            "status": 500,
        }
