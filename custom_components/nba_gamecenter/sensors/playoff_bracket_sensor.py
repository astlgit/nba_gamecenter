from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator.nba_coordinator import NBAGameCenterCoordinator
from ..utils.mapping import BRACKET_STRUCTURE


class NBAPlayoffBracketSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:bracket"

    def __init__(self, coordinator: NBAGameCenterCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = "nba_bracket"
        self._attr_name = "nba_bracket"

    @property
    def native_value(self) -> str:
        return "playoffs"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        series_data = self.coordinator.data.get("series", {})
        active = [sid for sid, s in series_data.items() if s.get("active")]
        completed = [sid for sid, s in series_data.items() if s.get("completed")]

        attrs: dict[str, Any] = {
            "structure": BRACKET_STRUCTURE,
            "active_series": active,
            "completed_series": completed,
        }
        return attrs
