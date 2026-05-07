from __future__ import annotations

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo

from ..const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up NBA live game sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    live_games = coordinator.data.get("live", [])
    for game in live_games:
        sensors.append(NBALiveGameSensor(coordinator, game))

    async_add_entities(sensors)


class NBALiveGameSensor(Entity):
    """Sensor representing a single live NBA game."""

    def __init__(self, coordinator, game):
        self.coordinator = coordinator
        self.game = game
        self._attr_unique_id = f"nba_live_{game['gameId']}"
        self._attr_name = f"{game['awayTeam']['teamTricode']} @ {game['homeTeam']['teamTricode']}"

    @property
    def state(self):
        return self.game.get("gameStatusText")

    @property
    def extra_state_attributes(self):
        return {
            "game_id": self.game.get("gameId"),
            "home_team": self.game["homeTeam"]["teamName"],
            "away_team": self.game["awayTeam"]["teamName"],
            "home_score": self.game["homeTeam"].get("score"),
            "away_score": self.game["awayTeam"].get("score"),
            "period": self.game.get("period"),
            "clock": self.game.get("gameClock"),
            "status": self.game.get("gameStatus"),
        }

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, "nba_gamecenter")},
            name="NBA GameCenter",
            manufacturer="NBA",
        )
