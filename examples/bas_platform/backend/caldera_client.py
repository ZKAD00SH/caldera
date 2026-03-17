from __future__ import annotations

from typing import Any

import httpx


class CalderaClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "KEY": api_key,
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    async def trigger_operation(
        self,
        adversary_id: str,
        group: str = "red",
        planner: str = "atomic",
        source: str = "basic",
    ) -> dict[str, Any]:
        payload = {
            "name": f"op-{adversary_id[:8]}",
            "adversary_id": adversary_id,
            "group": group,
            "planner": planner,
            "source": source,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/v2/operations",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def list_operations(self, limit: int = 20) -> list[dict[str, Any]]:
        params = {"limit": limit}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/api/v2/operations",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else data.get("operations", [])
