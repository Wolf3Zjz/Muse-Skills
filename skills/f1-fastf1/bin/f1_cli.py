#!/usr/bin/env python3
"""F1 data CLI bootstrap.

Thin wrapper over the ``sports-skills`` package CLI (machina-sports/sports-skills,
``f1`` module). Enables a persistent FastF1 HTTP cache inside the skill directory
before delegating to the upstream CLI, so repeated queries don't re-download
session data and the cache survives VM restarts.

Usage:
    f1 f1 <command> [--key=value ...]
"""

import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CACHE = os.path.join(SKILL_DIR, ".cache", "fastf1")
CACHE_DIR = os.environ.get("F1_FASTF1_CACHE_DIR", DEFAULT_CACHE)


def main() -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)

    import fastf1

    # Explicit cache dir inside the skill; overrides fastf1's default ~/.cache.
    fastf1.Cache.enable_cache(CACHE_DIR)
    fastf1.set_log_level("WARNING")

    from sports_skills.cli import main as upstream_main

    # Upstream CLI expects argv like: ["sports-skills", "f1", "get_race_schedule", ...]
    sys.argv = ["sports-skills"] + sys.argv[1:]
    upstream_main()


if __name__ == "__main__":
    main()
