---
name: "f1-fastf1"
description: |
  Formula 1 data — season calendar, race/qualifying/practice results, lap-by-lap timing with sectors, pit stops, speed traps, tire strategy and degradation, driver/team head-to-head comparison, championship standings, season stats. Powered by the FastF1 library (F1 official livetiming history, 2018 season onward). No API key needed.

  Use when: user asks about F1 race results, qualifying, lap times, sector times, driver stats, team info, the F1 calendar / 赛历, tire strategy / 轮胎策略, pit stops, championship standings / 积分榜, or comparing drivers/teams.
  Don't use when: user asks about other motorsports (MotoGP, NASCAR, IndyCar, WEC, Formula E). Don't use for F1 news — that's a different skill. Don't use for live timing during an ongoing session — this skill only has data after a session ends.
license: MIT
metadata: { "includeInPrompt": true }
---

# f1-fastf1 — Formula 1 Data

## Purpose

Answer F1 questions with real session data: schedules, classifications, lap timing, sectors, tires, pit stops, speed traps, standings, and comparisons. All data comes from FastF1 (F1's official livetiming feed history, 2018+). Read-only; no API key, no signup.

## Tooling

Single entry point — a wrapper script plus a Python CLI, with a persistent FastF1 cache.
First-time setup is required (this repo does not ship `.venv/`): follow `INSTALL.md`
for the one-time venv setup — those steps were verified end-to-end in a fresh venv.

```bash
<skill-dir>/bin/f1 f1 <command> [--key=value ...]
```

Examples:

```bash
# Season calendar
<skill-dir>/bin/f1 f1 get_race_schedule --year=2026

# Race classification
<skill-dir>/bin/f1 f1 get_race_results --year=2026 --event="Azerbaijan Grand Prix"

# Lap-by-lap for one driver (sectors + compounds)
<skill-dir>/bin/f1 f1 get_lap_data --year=2026 --event="Azerbaijan Grand Prix" --driver="VER"

# Tire strategy / stints / degradation
<skill-dir>/bin/f1 f1 get_tire_analysis --year=2026 --event="Azerbaijan Grand Prix"

# Standings (optionally after a given round)
<skill-dir>/bin/f1 f1 get_championship_standings --year=2026 --round=15
```

Output is JSON: `{"status": true, "data": ...}`. FastF1 cache lives in `.cache/fastf1/` inside the skill dir and is reused across calls.

Implementation: `bin/f1` (bash) → `bin/f1_cli.py` (enables the cache, delegates to the upstream `sports-skills` CLI). Python deps live in `.venv/` — create it per `INSTALL.md` (sports-skills 0.35.0, fastf1 3.8.3, Python 3.12). Do not `pip install` into the system Python; use the venv.

## Auth

None. FastF1 pulls public F1 livetiming history; no key required.

## Operating Rules

1. **Year selection.** If the user names a year, use it. Otherwise: the F1 season runs roughly March–December. From March onward use the current year; in January/February use `current_year - 1` (new season hasn't started).
2. **Event names must be exact.** Always call `get_race_schedule --year=<y>` first and copy the `event_name` verbatim (e.g. `"Azerbaijan Grand Prix"`). A wrong name returns "event not found".
3. **No live timing.** Data for a session appears only after it ends. If a session hasn't happened yet, the result is empty — say so, don't invent numbers.
4. **Session types**: `R` (race), `Q` (qualifying), `FP1`/`FP2`/`FP3`, `S` (sprint). `get_lap_data` defaults to `R`.
5. **Commands that DO NOT exist** — never call these: `get_qualifying`, `get_practice`, `get_driver_results`, `get_standings`, `get_results`, `get_calendar`, `get_fastest_laps`, `get_tire_strategy`, `get_circuit_info`. Use the 13 real commands in `references/api-reference.md`.
6. **First load is slow.** The first query touching a session downloads it (~1–2 min); repeats are served from cache. For lap-heavy analysis, pass `--driver` to limit scope.
7. **Pit stop durations are pit-lane time** (entry to exit, ~20–30 s), not stationary time at the box — FastF1 doesn't provide the latter. Don't present them as stationary times.
8. **Personal use only.** Upstream data is third-party public data for non-commercial use.

## References

- `references/api-reference.md` — all 13 commands, parameters, return schemas, workflows.
- `INSTALL.md` — one-time venv setup, verified end-to-end (bilingual / 中英双语).
