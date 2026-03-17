from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import httpx


class WazuhCollector:
    def __init__(self, base_url: str, username: str, password: str, timeout: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout

    async def _get_token(self) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/security/user/authenticate",
                auth=(self.username, self.password),
            )
            response.raise_for_status()
            return response.json()["data"]["token"]

    async def fetch_recent_alerts(self, minutes: int = 10) -> list[dict[str, Any]]:
        since = (datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)).isoformat()
        token = await self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": f"timestamp>{since}",
            "limit": 200,
            "sort": "-timestamp",
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/alerts",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json().get("data", {}).get("affected_items", [])
