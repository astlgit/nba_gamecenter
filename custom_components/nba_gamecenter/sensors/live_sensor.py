from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator.nba_coordinator import NBAGameCenterCoordinator
from ..utils.mapping import SERIES_IDS


class NBALiveSeriesSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:scoreboard"

    def __init__(self, coordinator: NBAGameCenterCoordinator, series_id: str) -> None:
        super().__init__(coordinator)
        self._series_id = series_id
        self._attr_unique_id = f"nba_live_{series_id}"
        self._attr_name = f"nba_live_{series_id}"

    @property
    def native_value(self) -> str | None:
        data = self._live_data
        if not data:
            return None
        status = data.get("status")
        period = data.get("period")
        clock = data.get("clock")
        if status != "live":
            return status
        return f"Q{period} {clock}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._live_data or {}

    @property
    def _live_data(self) -> dict[str, Any] | None:
        live = self.coordinator.data.get("live", {})
        return live.get(self._series_id)


def create_live_sensors(
    coordinator: NBAGameCenterCoordinator,
) -> list[NBALiveSeriesSensor]:
    return [NBALiveSeriesSensor(coordinator, sid) for sid in SERIES_IDS]
