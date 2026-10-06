# f1-fastf1 — API Reference

Adapted from machina-sports/sports-skills `skills/fastf1` (MIT). CLI form: `bin/f1 f1 <command> [--key=value]`.

## Commands

| Command | Required | Optional | Description |
|---|---|---|---|
| `get_race_schedule` | | year | Full season calendar: event names, dates, circuits, session times |
| `get_race_results` | year, event | | Final classification: positions, times, points, fastest lap |
| `get_session_data` | session_year, session_name | session_type (default `Q`) | Raw session info for Q / R / FP1 / FP2 / FP3 / S |
| `get_driver_info` | year | driver | Grid details: number, code, team, nationality |
| `get_team_info` | year | team | Team info with driver lineup |
| `get_lap_data` | year, event | session_type (default `R`), driver | Lap-by-lap: lap/sector times, compound; `is_pit_in_lap`/`is_pit_out_lap` mark pit laps |
| `get_pit_stops` | year | event, driver | Pit-lane durations (entry→exit, NOT stationary), team averages |
| `get_speed_data` | year | event, driver | Speed trap / intermediate / finish-line speeds |
| `get_championship_standings` | year | round | Driver + constructor standings, optionally after round N |
| `get_season_stats` | year | | Season aggregates: fastest laps, top speeds, points/wins/podiums |
| `get_team_comparison` | year, team1, team2 | event | Head-to-head: quali deltas, race pace, sectors, points |
| `get_driver_comparison` | year, driver1, driver2 | event | Head-to-head: quali H2H, race H2H, pace delta, per-race breakdown. `event="last"` = most recent race |
| `get_tire_analysis` | year | event, driver | Compounds, stint lengths, degradation rates |

Driver identifiers: 3-letter codes (`VER`, `NOR`, `PIA`) or names. Team names: e.g. `Red Bull`, `McLaren`, `Ferrari`, `Mercedes`.

## Key return schemas

- **get_race_results** → `data[]`: `position`, `driver` (code), `full_name`, `team`, `grid_position`, `points`, `status`, `time`, `fastest_lap` (bool), `fastest_lap_time` (driver's best lap).
- **get_championship_standings** → `data.driver_standings[]`: `position`, `driver_code`, `full_name`, `team`, `points` (incl. sprint), `sprint_points`, `wins`, `podiums`; `data.constructor_standings[]`: `position`, `team`, `points`, `wins`. With `round`: `data.after_round`, `data.races_counted`.
- **get_lap_data** → `data[]`: `lap_number`, `lap_time`, `sector_1/2/3_time`, `compound`, `is_pit_in_lap`, `is_pit_out_lap`, `is_accurate` (false for pit laps / sector-rebuilt laps).
- **get_pit_stops** → `data.pit_stops[]` (`race`, `team`, `driver`, `lap`, `duration_seconds`, `red_flag`), `data.team_summary[]` (avg/best/total), `data.total_stops`. `duration_type` is always `"pit_lane_time"`. Red-flag tyre changes have `red_flag: true` and huge durations (~whole stoppage) — excluded from team_summary.
- **get_session_data** → metadata: `session` (e.g. `"2026 Season Round 13: Italian Grand Prix - Race"`), `event_name`, `round`, `event_date`, `session_date` (track-local), `session_type`, `track_name`, plus `results[]`.
- **get_tire_analysis** → compound usage, stint lengths, degradation rates, pit strategies.
- **get_driver_comparison / get_team_comparison** → H2H records, pace deltas, per-race breakdowns. Points include sprint points of compared weekends.

## Workflows

**Race weekend analysis**: schedule → `get_race_results` → `get_lap_data --session_type=R` → `get_tire_analysis`.
**Driver/team comparison**: `get_championship_standings` → `get_driver_comparison`/`get_team_comparison` → `get_season_stats`.
**Season overview**: `get_race_schedule` → `get_championship_standings` → `get_season_stats` → `get_driver_info`.

## Do NOT exist

`get_qualifying` / `get_practice` (use `get_session_data`), `get_standings`, `get_results`, `get_calendar`, `get_driver_results`, `get_fastest_laps`, `get_tire_strategy`, `get_circuit_info`. If it's not in the table above, it doesn't exist.

## Troubleshooting

- *Event name not found* → call `get_race_schedule` first, copy `event_name` exactly.
- *Empty session data* → the session hasn't happened yet (no live timing). Say so.
