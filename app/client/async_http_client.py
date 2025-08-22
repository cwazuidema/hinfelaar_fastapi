import httpx
from typing import Optional


_async_client: Optional[httpx.AsyncClient] = None


async def initialize_http_client() -> None:
    global _async_client
    if _async_client is None:
        _async_client = httpx.AsyncClient(
            timeout=10.0,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        )


async def get_http_client() -> httpx.AsyncClient:
    global _async_client
    if _async_client is None:
        await initialize_http_client()
    assert _async_client is not None
    return _async_client


async def close_http_client() -> None:
    global _async_client
    if _async_client is not None:
        await _async_client.aclose()
        _async_client = None
