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

    # coordinator.data["series"] is already normalized and keyed by series_id
    for series_id in coordinator.data.get("series", {}):
        entities.append(NBASeriesSensor(coordinator, series_id))

    async_add_entities(entities)


class NBASeriesSensor(CoordinatorEntity, SensorEntity):
    """NBA Playoff Series Sensor using normalized ESPN data."""

    def __init__(self, coordinator, series_id: str) -> None:
        super().__init__(coordinator)
        self._series_id = series_id
        self._attr_unique_id = f"nba_series_{series_id}"
        self._attr_name = f"NBA Series {series_id}"

    @property
    def state(self) -> str | None:
        series = self._get_series()
        if not series:
            return None

        home = series.get("home_team")
        away = series.get("away_team")

        if home and away:
            return f"{home} vs {away}"

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the normalized series structure."""
        return self._get_series() or {}

    def _get_series(self) -> dict[str, Any] | None:
        """Return normalized series data from coordinator."""
        return self.coordinator.data.get("series", {}).get(self._series_id)
