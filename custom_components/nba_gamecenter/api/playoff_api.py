from __future__ import annotations

from typing import Any


class NBAPLAYOFFAPI:
    """Extract playoff bracket + series data from ESPN scoreboard."""

    def __init__(self, coordinator) -> None:
        self._coordinator = coordinator

    async def get_series_data(self) -> dict[str, dict[str, Any]]:
        """Return dict keyed by ESPN series ID."""
        games = self._coordinator.data.get("games", [])
        if not games:
            return {}

        series_map: dict[str, dict[str, Any]] = {}

        for g in games:
            sb = g["scoreboard"]
            comp = sb.get("competitions", [{}])[0]

            series = comp.get("series", {})
            sid = series.get("id")
            if not sid:
                continue

            home = comp["competitors"][0]
            away = comp["competitors"][1]

            if sid not in series_map:
                series_map[sid] = {
                    "series_id": sid,
                    "round": series.get("round"),
                    "home_team": home["team"]["displayName"],
                    "away_team": away["team"]["displayName"],
                    "games": [],
                }

            series_map[sid]["games"].append(
                {
                    "game_id": g["game_id"],
                    "home_score": home.get("score"),
                    "away_score": away.get("score"),
                    "status": comp.get("status", {}).get("type", {}).get("description"),
                    "game_number": series.get("gameNumber"),
                }
            )

        return series_map
