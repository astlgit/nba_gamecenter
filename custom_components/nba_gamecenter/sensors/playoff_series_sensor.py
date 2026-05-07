from __future__ import annotations

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo

from ..const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up NBA playoff series sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    series_list = coordinator.data.get("series", [])
    for series in series_list:
        sensors.append(NBASeriesSensor(coordinator, series))

    async_add_entities(sensors)


class NBASeriesSensor(Entity):
    """Sensor representing a single NBA playoff series."""

    def __init__(self, coordinator, series):
        self.coordinator = coordinator
        self.series = series
        self._attr_unique_id = f"nba_series_{series['seriesId']}"
        self._attr_name = f"{series['roundName']} - {series['seriesName']}"

    @property
    def state(self):
        return self.series.get("seriesStatus")

    @property
    def extra_state_attributes(self):
        return {
            "series_id": self.series.get("seriesId"),
            "round": self.series.get("roundNum"),
            "conference": self.series.get("conference"),
            "home_team": self.series.get("homeTeam"),
            "away_team": self.series.get("awayTeam"),
            "home_wins": self.series.get("homeWins"),
            "away_wins": self.series.get("awayWins"),
            "games": self.series.get("games"),
        }

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "nba_gamecenter")},
            name="NBA GameCenter",
            manufacturer="NBA",
        )
