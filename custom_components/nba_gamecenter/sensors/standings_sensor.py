from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = [
        NBAStandingsSensor(coordinator, "eastern"),
        NBAStandingsSensor(coordinator, "western"),
    ]

    async_add_entities(entities)


class NBAStandingsSensor(CoordinatorEntity, SensorEntity):
    """NBA Standings Sensor (ESPN)."""

    def __init__(self, coordinator, conference: str) -> None:
        super().__init__(coordinator)
        self._conference = conference
        self._attr_unique_id = f"nba_standings_{conference}"
        self._attr_name = f"NBA Standings {conference.title()} Conference"

    @property
    def state(self) -> int | None:
        """Return number of teams in this conference."""
        standings = self._get_conference_standings()
        return len(standings) if standings else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return standings attributes."""
        standings = self._get_conference_standings()
        if not standings:
            return {}

        attrs = {}

        for team in standings:
            tid = team.get("team", {}).get("id")
            if not tid:
                continue

            attrs[tid] = {
                "name": team["team"]["displayName"],
                "abbrev": team["team"]["abbreviation"],
                "rank": team.get("stats", {}).get("rank"),
                "wins": team.get("stats", {}).get("wins"),
                "losses": team.get("stats", {}).get("losses"),
                "win_pct": team.get("stats", {}).get("winPercent"),
                "games_behind": team.get("stats", {}).get("gamesBehind"),
                "streak": team.get("stats", {}).get("streak"),
                "logo": team["team"]["logos"][0]["href"]
                if team["team"].get("logos")
                else None,
            }

        return attrs

    # -----------------------------
    # Helpers
    # -----------------------------
    def _get_conference_standings(self) -> list[dict] | None:
        """Extract standings for the selected conference."""
        data = self.coordinator.data
        if not data:
            return None

        standings = data.get("standings")
        if not standings:
            return None

        groups = standings.get("children", [])
        for group in groups:
            name = group.get("name", "").lower()
            if self._conference in name:
                return group.get("standings", {}).get("entries", [])

        return None
