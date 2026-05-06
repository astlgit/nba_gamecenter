from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .. import DOMAIN
from ..coordinator.nba_coordinator import NBAGameCenterCoordinator
from .playoff_series_sensor import create_series_sensors
from .live_sensor import create_live_sensors
from .playoff_bracket_sensor import NBAPlayoffBracketSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: NBAGameCenterCoordinator = hass.data[DOMAIN][entry.entry_id]

    series_sensors = create_series_sensors(coordinator)
    live_sensors = create_live_sensors(coordinator)
    bracket_sensor = NBAPlayoffBracketSensor(coordinator)

    async_add_entities(series_sensors + live_sensors + [bracket_sensor])
