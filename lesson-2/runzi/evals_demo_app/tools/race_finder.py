import json
from dataclasses import asdict
from typing import Optional

from langchain.tools import tool

from evals_demo_app.models.races import (
    Difficulty,
    Distance,
    Terrain,
    RaceType,
    load_races,
)

# Load all the races
races = load_races()


@tool(
    "find_races",
    description="Find races based on criteria such as location, distance, difficulty, terrain, and race type.",
)
def find_races(
    distance: Optional[Distance] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    difficulty: Optional[Difficulty] = None,
    terrain: Optional[Terrain] = None,
    race_type: Optional[RaceType] = None,
) -> str:
    """Find and return races based on the provided filters."""
    results = list(races)

    if distance is not None:
        results = [race for race in results if race.has_distance(distance)]

    if city is not None:
        results = [
            race for race in results if race.location.city.lower() == city.lower()
        ]

    if state is not None:
        results = [
            race for race in results if race.location.state.lower() == state.lower()
        ]

    if difficulty is not None:
        results = [race for race in results if race.difficulty == difficulty]

    if terrain is not None:
        results = [race for race in results if race.has_terrain(terrain)]

    if race_type is not None:
        results = [race for race in results if race.type == race_type]

    # Convert to JSON
    return json.dumps([asdict(race) for race in results], indent=2)
