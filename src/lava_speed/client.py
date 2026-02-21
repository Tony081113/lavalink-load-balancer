from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import aiohttp
import ujson


@dataclass(slots=True)
class LavaSpeedClient:
    base_url: str
    timeout_seconds: int = 10

    async def get_json(self, path: str) -> dict[str, Any]:
        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
                return ujson.loads(text)