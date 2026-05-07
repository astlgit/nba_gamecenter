from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Forward to your organized sensors module
from .sensors.live_sensor import async_setup_entry as setup_live_sensors
from .sensors.playoff_series_sensor import async_setup_entry as setup_series_sensors
from .sensors.playoff_bracket_sensor import async_setup_entry as setup_bracket_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Forward sensor setup to the organized sensor modules."""
    await setup_live_sensors(hass, entry, async_add_entities)
    await setup_series_sensors(hass, entry, async_add_entities)
    await setup_bracket_sensors(hass, entry, async_add_entities)
