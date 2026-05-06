from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator.nba_coordinator import NBAGameCenterCoordinator
from ..utils.mapping import SERIES_IDS


class NBAPlayoffSeriesSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:trophy"

    def __init__(self, coordinator: NBAGameCenterCoordinator, series_id: str) -> None:
        super().__init__(coordinator)
        self._series_id = series_id
        self._attr_unique_id = f"nba_series_{series_id}"
        self._attr_name = f"nba_series_{series_id}"

    @property
    def native_value(self) -> str | None:
        data = self._series_data
        if not data:
            return None
        return data.get("series_status")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._series_data or {}

    @property
    def _series_data(self) -> dict[str, Any] | None:
        series = self.coordinator.data.get("series", {})
        return series.get(self._series_id)


def create_series_sensors(
    coordinator: NBAGameCenterCoordinator,
) -> list[NBAPlayoffSeriesSensor]:
    return [NBAPlayoffSeriesSensor(coordinator, sid) for sid in SERIES_IDS]
