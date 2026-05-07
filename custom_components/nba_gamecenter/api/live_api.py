from __future__ import annotations

from typing import Any


class NBALiveAPI:
    """Live game extraction for ESPN NBA."""

    def __init__(self, coordinator) -> None:
        self._coordinator = coordinator

    async def get_live_series_data(self) -> dict[str, dict[str, Any]]:
        """
        Return live data keyed by game_id.
        (ESPN does NOT provide series-level live data like NHL.)
        """
        games = self._coordinator.data.get("games", [])
        if not games:
            return {}

        live_map: dict[str, dict[str, Any]] = {}

        for g in games:
            game_id = g.get("game_id")
            if not game_id:
                continue

            sb = g["scoreboard"]
            comp = sb.get("competitions", [{}])[0]

            home = comp["competitors"][0]
            away = comp["competitors"][1]

            status = comp.get("status", {}).get("type", {})
            live_map[game_id] = {
                "game_id": game_id,
                "status": status.get("description"),
                "period": status.get("period"),
                "clock": status.get("displayClock"),
                "home_team": home["team"]["displayName"],
                "home_score": home.get("score"),
                "away_team": away["team"]["displayName"],
                "away_score": away.get("score"),
                "possession": comp.get("situation", {}).get("possession"),
                "summary": g.get("summary"),
                "boxscore": g.get("boxscore"),
                "playbyplay": g.get("playbyplay"),
            }

        return live_map
