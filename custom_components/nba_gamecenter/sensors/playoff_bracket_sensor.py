from __future__ import annotations

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo

from ..const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up NBA playoff bracket sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    bracket = coordinator.data.get("bracket")
    if bracket:
        async_add_entities([NBABracketSensor(coordinator, bracket)])


class NBABracketSensor(Entity):
    """Sensor representing the full NBA playoff bracket."""

    def __init__(self, coordinator, bracket):
        self.coordinator = coordinator
        self.bracket = bracket
        self._attr_unique_id = "nba_playoff_bracket"
        self._attr_name = "NBA Playoff Bracket"

    @property
    def state(self):
        return self.bracket.get("seasonYear")

    @property
    def extra_state_attributes(self):
        return {
            "season": self.bracket.get("seasonYear"),
            "rounds": self.bracket.get("rounds"),
        }

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "nba_gamecenter")},
            name="NBA GameCenter",
            manufacturer="NBA",
        )
