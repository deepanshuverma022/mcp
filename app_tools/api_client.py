import httpx
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

BASE_URL = "https://website-pddf.onrender.com"

class APIClient:
    def __init__(self):
        # We set a generous timeout for security scanning which might take time
        self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=60.0)

    async def close(self):
        await self.client.aclose()

    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        try:
            logger.info(f"Making {method} request to {endpoint}")
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exception(f"API HTTP Error: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise Exception(f"API Request Error: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Unexpected API Error: {str(e)}") from e

    async def scan_website(self, url: str) -> Dict[str, Any]:
        """
        Scan a website for security vulnerabilities.
        """
        payload = {"url": url}
        return await self.request("POST", "/scan", json=payload)

api_client = APIClient()
