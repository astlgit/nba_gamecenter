from __future__ import annotations

import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

NBA_CDN_BASE = "https://cdn.nba.com/static/json"
NBA_LIVE_BASE = "https://cdn.nba.com/static/json/liveData"


class NBAApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    async def _get_json(self, url: str) -> dict[str, Any] | None:
        try:
            async with self._session.get(url, timeout=15) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("NBA API request failed: %s (%s)", url, err)
            return None

    async def get_playoff_bracket(self) -> dict | None:
        url = f"{NBA_CDN_BASE}/staticData/playoffBracket.json"
        return await self._get_json(url)

    async def get_todays_scoreboard(self) -> dict | None:
        url = f"{NBA_LIVE_BASE}/scoreboard/todaysScoreboard.json"
        return await self._get_json(url)

    async def get_boxscore(self, game_id: str) -> dict | None:
        url = f"{NBA_LIVE_BASE}/boxscore/boxscore_{game_id}.json"
        return await self._get_json(url)

    async def get_playbyplay(self, game_id: str) -> dict | None:
        url = f"{NBA_LIVE_BASE}/playbyplay/playbyplay_{game_id}.json"
        return await self._get_json(url)
