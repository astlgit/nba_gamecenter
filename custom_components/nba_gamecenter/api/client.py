from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"


class ESPNApiClient:
    """Client for ESPN's public NBA API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    # -----------------------------
    # Internal GET helper
    # -----------------------------
    async def _get_json(self, url: str) -> dict[str, Any] | None:
        try:
            async with self._session.get(url, timeout=20) as resp:
                if resp.status != 200:
                    _LOGGER.error("ESPN API error %s: %s", resp.status, url)
                    return None
                return await resp.json()
        except Exception as err:
            _LOGGER.error("ESPN API request failed: %s (%s)", url, err)
            return None

    # -----------------------------
    # Date helper
    # -----------------------------
    def _today_str(self) -> str:
        """Return today's date in ESPN-required YYYYMMDD format."""
        return datetime.now().strftime("%Y%m%d")

    # -----------------------------
    # Scoreboard
    # -----------------------------
    async def get_scoreboard(self, date: str | None = None) -> dict | None:
        """Fetch scoreboard for a given date (YYYYMMDD)."""
        if date is None:
            date = self._today_str()

        url = f"{ESPN_BASE}/scoreboard?dates={date}"
        return await self._get_json(url)

    # -----------------------------
    # Game Summary
    # -----------------------------
    async def get_game_summary(self, game_id: str) -> dict | None:
        url = f"{ESPN_BASE}/summary?event={game_id}"
        return await self._get_json(url)

    # -----------------------------
    # Boxscore
    # -----------------------------
    async def get_boxscore(self, game_id: str) -> dict | None:
        url = f"{ESPN_BASE}/boxscore?event={game_id}"
        return await self._get_json(url)

    # -----------------------------
    # Play-by-Play
    # -----------------------------
    async def get_playbyplay(self, game_id: str) -> dict | None:
        url = f"{ESPN_BASE}/playbyplay?event={game_id}"
        return await self._get_json(url)

    # -----------------------------
    # Standings
    # -----------------------------
    async def get_standings(self) -> dict | None:
        url = f"{ESPN_BASE}/standings"
        return await self._get_json(url)

    # -----------------------------
    # Teams
    # -----------------------------
    async def get_teams(self) -> dict | None:
        url = f"{ESPN_BASE}/teams"
        return await self._get_json(url)
