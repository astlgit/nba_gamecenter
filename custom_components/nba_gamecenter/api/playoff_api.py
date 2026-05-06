from __future__ import annotations

from typing import Any

from .client import NBAApiClient
from ..utils.mapping import SERIES_IDS
from ..utils.parsing import parse_bracket_series


class NBAPLAYOFFAPI:
    def __init__(self, client: NBAApiClient) -> None:
        self._client = client

    async def get_series_data(self) -> dict[str, dict[str, Any]]:
        """Return dict keyed by series_id (r1_e1, cf_w, finals, etc.)."""
        data = await self._client.get_playoff_bracket()
        if not data:
            return {}

        return parse_bracket_series(data, SERIES_IDS)
