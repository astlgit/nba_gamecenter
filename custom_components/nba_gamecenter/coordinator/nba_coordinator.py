from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..api.client import ESPNApiClient
from ..utils.parsing import extract_live_game_data, extract_series_from_games

_LOGGER = logging.getLogger(__name__)


class NBAGameCenterCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for ESPN NBA GameCenter."""

    def __init__(self, hass, session) -> None:
        self.hass = hass
        self.client = ESPNApiClient(session)

        super().__init__(
            hass,
            _LOGGER,
            name="nba_gamecenter",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch all NBA data from ESPN."""

        # -----------------------------
        # 1. Scoreboard (today)
        # -----------------------------
        scoreboard = await self.client.get_scoreboard()
        if scoreboard is None:
            raise UpdateFailed("Failed to fetch ESPN NBA scoreboard")

        events = scoreboard.get("events", [])

        # -----------------------------
        # 2. Teams + Standings
        # -----------------------------
        teams = await self.client.get_teams()
        standings = await self.client.get_standings()

        # -----------------------------
        # 3. Expand each game with details
        # -----------------------------
        games: list[dict[str, Any]] = []

        for event in events:
            game_id = event.get("id")
            if not game_id:
                continue

            summary = await self.client.get_game_summary(game_id)
            boxscore = await self.client.get_boxscore(game_id)
            pbp = await self.client.get_playbyplay(game_id)

            games.append(
                {
                    "game_id": game_id,
                    "scoreboard": event,
                    "summary": summary,
                    "boxscore": boxscore,
                    "playbyplay": pbp,
                }
            )

        # -----------------------------
        # 4. Normalize live + series data
        # -----------------------------
        live_data = {
            g["game_id"]: extract_live_game_data(g)
            for g in games
        }

        series_data = extract_series_from_games(games)

        # -----------------------------
        # Final coordinator structure
        # -----------------------------
        return {
            "games": games,
            "live": live_data,
            "series": series_data,
            "teams": teams,
            "standings": standings,
            "raw_scoreboard": scoreboard,
        }
