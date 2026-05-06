from __future__ import annotations

# Hardcoded series IDs (playoff structure)
SERIES_IDS: list[str] = [
    "r1_e1",
    "r1_e2",
    "r1_e3",
    "r1_e4",
    "r1_w1",
    "r1_w2",
    "r1_w3",
    "r1_w4",
    "r2_e1",
    "r2_e2",
    "r2_w1",
    "r2_w2",
    "cf_e",
    "cf_w",
    "finals",
]

BRACKET_STRUCTURE = {
    "round1_east": ["r1_e1", "r1_e2", "r1_e3", "r1_e4"],
    "round1_west": ["r1_w1", "r1_w2", "r1_w3", "r1_w4"],
    "round2_east": ["r2_e1", "r2_e2"],
    "round2_west": ["r2_w1", "r2_w2"],
    "conference_finals": ["cf_e", "cf_w"],
    "finals": ["finals"],
}
