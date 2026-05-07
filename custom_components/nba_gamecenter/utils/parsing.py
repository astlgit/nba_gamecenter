from __future__ import annotations
from typing import Any


def extract_live_game_data(game: dict[str, Any]) -> dict[str, Any]:
    """
    Extract live game attributes from ESPN scoreboard structure.
    This is used by the live sensors.
    """
    sb = game["scoreboard"]
    comp = sb.get("competitions", [{}])[0]

    home = comp["competitors"][0]
    away = comp["competitors"][1]

    status = comp.get("status", {}).get("type", {})

    return {
        "game_id": game["game_id"],
        "status": status.get("description"),
        "period": status.get("period"),
        "clock": status.get("displayClock"),

        "home_team": home["team"]["displayName"],
        "away_team": away["team"]["displayName"],
        "home_score": home.get("score"),
        "away_score": away.get("score"),

        "home_id": home["team"]["id"],
        "away_id": away["team"]["id"],

        "summary": game.get("summary"),
        "boxscore": game.get("boxscore"),
        "playbyplay": game.get("playbyplay"),
    }


def extract_series_from_games(games: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Group games by ESPN series ID.
    This powers the playoff bracket + playoff series sensors.
    """
    series_map: dict[str, Any] = {}

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
