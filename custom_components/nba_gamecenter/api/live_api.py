from __future__ import annotations

from typing import Any

from .client import NBAApiClient
from ..utils.mapping import SERIES_IDS
from ..utils.parsing import (
    map_series_to_game_ids,
    parse_live_game_for_series,
)


class NBALiveAPI:
    def __init__(self, client: NBAApiClient) -> None:
        self._client = client

    async def get_live_series_data(self) -> dict[str, dict[str, Any]]:
        """Return live data per series_id."""
        scoreboard = await self._client.get_todays_scoreboard()
        if not scoreboard:
            return {}

        series_to_game = map_series_to_game_ids(scoreboard, SERIES_IDS)
        result: dict[str, dict[str, Any]] = {}

        for series_id, game_id in series_to_game.items():
            if not game_id:
                continue

            boxscore = await self._client.get_boxscore(game_id)
            if not boxscore:
                continue

            live = parse_live_game_for_series(series_id, game_id, boxscore)
            if live:
                result[series_id] = live

        return result
