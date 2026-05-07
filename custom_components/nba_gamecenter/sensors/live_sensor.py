from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []

    # coordinator.data["live"] is keyed by game_id
    for game_id in coordinator.data.get("live", {}):
        entities.append(NBALiveGameSensor(coordinator, game_id))

    async_add_entities(entities)


class NBALiveGameSensor(CoordinatorEntity, SensorEntity):
    """Live NBA game sensor using ESPN normalized data."""

    def __init__(self, coordinator, game_id: str) -> None:
        super().__init__(coordinator)
        self._game_id = game_id
        self._attr_unique_id = f"nba_live_{game_id}"
        self._attr_name = f"NBA Live Game {game_id}"

    @property
    def state(self) -> str | None:
        live = self._get_live()
        if not live:
            return None
        return live.get("status")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        live = self._get_live()
        if not live:
            return {}

        return {
            "game_id": self._game_id,
            "home_team": live.get("home_team"),
            "home_score": live.get("home_score"),
            "away_team": live.get("away_team"),
            "away_score": live.get("away_score"),
            "period": live.get("period"),
            "clock": live.get("clock"),
            "summary": live.get("summary"),
            "boxscore": live.get("boxscore"),
            "playbyplay": live.get("playbyplay"),
        }

    def _get_live(self) -> dict | None:
        """Return normalized live data for this game."""
        return self.coordinator.data.get("live", {}).get(self._game_id)
