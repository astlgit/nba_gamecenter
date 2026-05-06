NBA GameCenter
==============

NBA GameCenter is a Home Assistant custom integration that provides:

Playoff series sensors

Live game sensors with advanced metrics

A full playoff bracket sensor

Team metadata (logos, colors, seeds)

Real‑time scoreboard and boxscore data

This integration is designed for dashboard builders who want clean, predictable, high‑quality NBA playoff data.

Features

Playoff Series Sensors
Each playoff series has a static sensor:

sensor.nba_series_r1_e1
sensor.nba_series_r1_e2
…
sensor.nba_series_finals

These sensors include:

Team names

Seeds

Logos

Colors

Series status

Next game

Last game

Game IDs

Live Game Sensors
Each series also has a live sensor:

sensor.nba_live_r1_e1
sensor.nba_live_r1_e2
…
sensor.nba_live_finals

Live sensors include:

Scores

Period + clock

Possession

Bonus status

Timeouts

Win probability

Momentum

Run length

Arena

Broadcast info

Playoff Bracket Sensor
sensor.nba_bracket

Includes:

Round structure

Active series

Completed series

Installation

Place the folder:

custom_components/nba_gamecenter

into your Home Assistant configuration directory.

Restart Home Assistant and add the integration through:

Settings → Devices & Services → Add Integration → NBA GameCenter

Status

This is an early development version and will evolve as the NBA playoff data structure is refined.