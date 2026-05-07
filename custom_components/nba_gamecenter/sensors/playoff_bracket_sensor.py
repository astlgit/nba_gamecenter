from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([NBABracketSensor(coordinator)])


class NBABracketSensor(CoordinatorEntity, SensorEntity):
    """NBA Playoff Bracket Sensor using normalized ESPN data."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = "nba_playoff_bracket"
        self._attr_name = "NBA Playoff Bracket"

    @property
    def state(self) -> int:
        """Return number of active playoff series."""
        series = self.coordinator.data.get("series", {})
        return len(series)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the normalized bracket structure."""
        return self.coordinator.data.get("series", {})
