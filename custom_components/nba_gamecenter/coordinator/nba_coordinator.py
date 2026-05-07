from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

LIVE_URL = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard.json"
BRACKET_URL = "https://cdn.nba.com/static/json/staticData/playoffBracket.json"
SERIES_URL = "https://cdn.nba.com/static/json/staticData/playoffSeries.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (HomeAssistant NBA GameCenter)",
    "Accept": "application/json",
}


class NBAGameCenterCoordinator(DataUpdateCoordinator):
    """Coordinator for NBA GameCenter."""

    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            _LOGGER,
            name="NBA GameCenter",
            update_interval=timedelta(seconds=30),
        )

        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        """Fetch all NBA data."""
        try:
            live = await self._fetch_json(LIVE_URL)
            bracket = await self._fetch_json(BRACKET_URL)
            series = await self._fetch_json(SERIES_URL)

            return {
                "live": self._parse_live_games(live),
                "bracket": self._parse_bracket(bracket),
                "series": self._parse_series(series),
            }

        except Exception as err:
            raise UpdateFailed(f"NBA update failed: {err}") from err

    async def _fetch_json(self, url: str):
        """Fetch JSON with error handling."""
        try:
            async with self.session.get(url, headers=HEADERS) as resp:
                if resp.status == 403:
                    _LOGGER.error("NBA API 403 Forbidden: %s", url)
                    return None

                resp.raise_for_status()
                return await resp.json()

        except Exception as err:
            _LOGGER.error("NBA API request failed: %s (%s)", url, err)
            return None

    # -----------------------------
    # PARSERS
    # -----------------------------

    def _parse_live_games(self, data):
        if not data or "scoreboard" not in data:
            return []

        games = data["scoreboard"].get("games", [])
        parsed = []

        for g in games:
            parsed.append({
                "gameId": g.get("gameId"),
                "gameStatus": g.get("gameStatus"),
                "gameStatusText": g.get("gameStatusText"),
                "gameClock": g.get("gameClock"),
                "period": g.get("period"),
                "homeTeam": g.get("homeTeam", {}),
                "awayTeam": g.get("awayTeam", {}),
            })

        return parsed

    def _parse_bracket(self, data):
        if not data or "playoffBracket" not in data:
            return None

        bracket = data["playoffBracket"]

        return {
            "seasonYear": bracket.get("seasonYear"),
            "rounds": bracket.get("rounds"),
        }

    def _parse_series(self, data):
        if not data or "series" not in data:
            return []

        parsed = []

        for s in data["series"]:
            parsed.append({
                "seriesId": s.get("seriesId"),
                "seriesName": s.get("seriesName"),
                "roundName": s.get("roundName"),
                "roundNum": s.get("roundNum"),
                "conference": s.get("conference"),
                "homeTeam": s.get("homeTeam"),
                "awayTeam": s.get("awayTeam"),
                "homeWins": s.get("homeWins"),
                "awayWins": s.get("awayWins"),
                "seriesStatus": s.get("seriesStatus"),
                "games": s.get("games"),
            })

        return parsed
