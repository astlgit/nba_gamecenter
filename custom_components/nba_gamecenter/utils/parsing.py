from __future__ import annotations

from typing import Any

from .team_data import TEAMS


def parse_bracket_series(
    data: dict[str, Any],
    series_ids: list[str],
) -> dict[str, dict[str, Any]]:
    """Parse playoffBracket.json into per-series structures."""
    result: dict[str, dict[str, Any]] = {}

    # The exact structure may need tweaking once you inspect real JSON.
    # This is a first-pass layout.
    series_list = data.get("playoffBracket", {}).get("series", [])

    for s in series_list:
        sid = _map_raw_series_to_id(s, series_ids)
        if not sid:
            continue

        home = s.get("topRow", {})
        away = s.get("bottomRow", {})

        home_abbr = home.get("teamTricode")
        away_abbr = away.get("teamTricode")

        home_team = TEAMS.get(home_abbr, {})
        away_team = TEAMS.get(away_abbr, {})

        series_status = s.get("seriesSummaryText")
        completed = s.get("isSeriesCompleted", False)
        active = not completed and bool(home_abbr and away_abbr)

        result[sid] = {
            "series_id": sid,
            "round": s.get("roundNumber"),
            "conference": s.get("conferenceName"),
            "home_abbr": home_abbr,
            "away_abbr": away_abbr,
            "home_team": home_team.get("name", home_abbr),
            "away_team": away_team.get("name", away_abbr),
            "home_seed": home.get("seedNum"),
            "away_seed": away.get("seedNum"),
            "home_logo": home_team.get("logo"),
            "away_logo": away_team.get("logo"),
            "home_color": home_team.get("primary_color"),
            "away_color": away_team.get("primary_color"),
            "series_status": series_status,
            "completed": completed,
            "active": active,
            "game_ids": s.get("games", []),
            "next_game": s.get("nextGameId"),
            "last_game": s.get("lastGameId"),
        }

    return result


def _map_raw_series_to_id(raw: dict[str, Any], series_ids: list[str]) -> str | None:
    # Placeholder mapping logic; you’ll refine this once you inspect real data.
    round_num = raw.get("roundNumber")
    conf = raw.get("conferenceName", "").lower()

    if round_num == 1 and conf == "east":
        idx = raw.get("seriesNumber", 1)
        return f"r1_e{idx}"
    if round_num == 1 and conf == "west":
        idx = raw.get("seriesNumber", 1)
        return f"r1_w{idx}"
    if round_num == 2 and conf == "east":
        idx = raw.get("seriesNumber", 1)
        return f"r2_e{idx}"
    if round_num == 2 and conf == "west":
        idx = raw.get("seriesNumber", 1)
        return f"r2_w{idx}"
    if round_num == 3 and conf == "east":
        return "cf_e"
    if round_num == 3 and conf == "west":
        return "cf_w"
    if round_num == 4:
        return "finals"

    return None


def map_series_to_game_ids(
    scoreboard: dict[str, Any],
    series_ids: list[str],
) -> dict[str, str | None]:
    """Map series_id -> current game_id (if any) from todaysScoreboard."""
    result: dict[str, str | None] = {sid: None for sid in series_ids}
    games = scoreboard.get("scoreboard", {}).get("games", [])

    for g in games:
        game_id = g.get("gameId")
        series_text = g.get("seriesText", "")  # e.g., "BOS leads 2-1"
        # You may need a better mapping here; this is a placeholder.
        # For now, we don't know which series_id this belongs to without
        # cross-referencing bracket data, which you can add later.
        # We'll leave everything None until we wire that up.
        _ = series_text
        _ = game_id

    return result


def parse_live_game_for_series(
    series_id: str,
    game_id: str,
    boxscore: dict[str, Any],
) -> dict[str, Any] | None:
    """Parse boxscore_<gameId>.json into live sensor attributes."""
    game = boxscore.get("game", {})
    if not game:
        return None

    home = game.get("homeTeam", {})
    away = game.get("awayTeam", {})

    status = game.get("gameStatusText", "").lower()
    period = game.get("period", {}).get("current")
    clock = game.get("gameClock")

    home_score = int(home.get("score", 0))
    away_score = int(away.get("score", 0))

    home_abbr = home.get("teamTricode")
    away_abbr = away.get("teamTricode")

    home_team = TEAMS.get(home_abbr, {})
    away_team = TEAMS.get(away_abbr, {})

    # Advanced metrics placeholders — refine once you inspect real JSON
    home_wp = game.get("homeWinProbability")
    away_wp = game.get("awayWinProbability")
    momentum = game.get("momentum")
    run_length = game.get("runLength")

    return {
        "series_id": series_id,
        "game_id": game_id,
        "status": status,
        "period": period,
        "clock": clock,
        "arena": game.get("arenaName"),
        "broadcast": game.get("broadcasters", []),

        "home_team": home_team.get("name", home_abbr),
        "away_team": away_team.get("name", away_abbr),
        "home_abbr": home_abbr,
        "away_abbr": away_abbr,
        "home_seed": home.get("seedNum"),
        "away_seed": away.get("seedNum"),
        "home_logo": home_team.get("logo"),
        "away_logo": away_team.get("logo"),
        "home_color": home_team.get("primary_color"),
        "away_color": away_team.get("primary_color"),

        "home_score": home_score,
        "away_score": away_score,
        "possession": game.get("possession"),  # may need refinement
        "home_timeouts_remaining": home.get("timeoutsRemaining"),
        "away_timeouts_remaining": away.get("timeoutsRemaining"),
        "home_in_bonus": home.get("inBonus"),
        "away_in_bonus": away.get("inBonus"),

        "home_win_probability": home_wp,
        "away_win_probability": away_wp,
        "momentum": momentum,
        "run_length": run_length,
    }
