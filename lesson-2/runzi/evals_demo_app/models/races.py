from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import json
import os
from pathlib import Path
from typing import Any, Optional, Union


class RaceType(StrEnum):
    """Race type enumeration."""

    FUN_RUN = "fun_run"
    ROAD_RACE = "road_race"
    TRAIL_RACE = "trail_race"
    BEACH_RACE = "beach_race"
    MIXED_TERRAIN = "mixed_terrain"
    ULTRA_RACE = "ultra_race"


class Terrain(StrEnum):
    """Terrain type enumeration."""

    ROAD = "road"
    TRAIL = "trail"
    BEACH = "beach"


class Distance(StrEnum):
    """Race distance enumeration."""

    FIVE_K = "5K"
    TEN_K = "10K"
    HALF_MARATHON = "half_marathon"
    MARATHON = "marathon"
    HUNDRED_MILE = "100_mile"


class Difficulty(StrEnum):
    """Race difficulty enumeration."""

    EASY = "easy"
    MODERATE = "moderate"
    CHALLENGING = "challenging"
    HARD = "hard"
    EXTREME = "extreme"


@dataclass
class Location:
    """Race location information."""

    city: str
    state: str
    venue: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Location:
        """Create a Location from a dictionary."""
        return cls(
            city=data["city"],
            state=data["state"],
            venue=data["venue"],
        )


@dataclass
class ElevationGain:
    """Elevation gain information for different race distances."""

    five_k: Optional[int] = None
    ten_k: Optional[int] = None
    half_marathon: Optional[int] = None
    marathon: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ElevationGain:
        """Create an ElevationGain from a dictionary."""
        return cls(
            five_k=data.get("5K"),
            ten_k=data.get("10K"),
            half_marathon=data.get("half_marathon"),
            marathon=data.get("marathon"),
        )


@dataclass
class Altitude:
    """Altitude information for race course."""

    start: int
    max: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Altitude:
        """Create an Altitude from a dictionary."""
        return cls(
            start=data["start"],
            max=data["max"],
        )


@dataclass
class RegistrationFee:
    """Registration fee information for different race distances."""

    five_k: Optional[int] = None
    ten_k: Optional[int] = None
    half_marathon: Optional[int] = None
    marathon: Optional[int] = None
    flat_fee: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Union[dict[str, Any], int]) -> RegistrationFee:
        """Create a RegistrationFee from a dictionary or integer."""
        if isinstance(data, int):
            return cls(flat_fee=data)
        return cls(
            five_k=data.get("5K"),
            ten_k=data.get("10K"),
            half_marathon=data.get("half_marathon"),
            marathon=data.get("marathon"),
        )

    def get_fee(self, distance: str) -> Optional[int]:
        """Get the fee for a specific distance."""
        if self.flat_fee is not None:
            return self.flat_fee

        distance_map = {
            "5K": self.five_k,
            "10K": self.ten_k,
            "half_marathon": self.half_marathon,
            "marathon": self.marathon,
        }
        return distance_map.get(distance)


@dataclass
class Race:
    """Running race information."""

    id: str
    name: str
    type: RaceType
    distances: list[Distance]
    location: Location
    date: str
    time: str
    terrain: list[Terrain]
    description: str
    expected_attendance: int
    registration_fee: RegistrationFee
    features: list[str]
    elevation_gain: Optional[Union[ElevationGain, int]] = None
    cutoff_time: Optional[str] = None
    aid_stations: Optional[int] = None
    difficulty: Optional[Difficulty] = None
    altitude: Optional[Altitude] = None
    qualifier_required: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Race:
        """Create a Race from a dictionary."""
        # Parse location
        location = Location.from_dict(data["location"])

        # Parse registration fee
        registration_fee = RegistrationFee.from_dict(data["registration_fee"])

        # Parse optional elevation gain
        elevation_gain = None
        if "elevation_gain" in data:
            if isinstance(data["elevation_gain"], dict):
                elevation_gain = ElevationGain.from_dict(data["elevation_gain"])
            else:
                elevation_gain = data["elevation_gain"]

        # Parse optional altitude
        altitude = None
        if "altitude" in data:
            altitude = Altitude.from_dict(data["altitude"])

        # Convert distances to enum
        distances = [Distance(d) for d in data["distances"]]

        # Convert terrain to enum list
        terrain = [Terrain(t) for t in data["terrain"]]

        return cls(
            id=data["id"],
            name=data["name"],
            type=RaceType(data["type"]),
            distances=distances,
            location=location,
            date=data["date"],
            time=data["time"],
            terrain=terrain,
            description=data["description"],
            expected_attendance=data["expected_attendance"],
            registration_fee=registration_fee,
            features=data["features"],
            elevation_gain=elevation_gain,
            cutoff_time=data.get("cutoff_time"),
            aid_stations=data.get("aid_stations"),
            difficulty=Difficulty(data["difficulty"]) if "difficulty" in data else None,
            altitude=altitude,
            qualifier_required=data.get("qualifier_required"),
        )

    def has_distance(self, distance: Distance) -> bool:
        """Check if the race offers a specific distance."""
        return distance in self.distances

    def has_terrain(self, terrain: Terrain) -> bool:
        """Check if the race includes a specific terrain type."""
        return terrain in self.terrain

    def get_registration_fee_for_distance(self, distance: str) -> Optional[int]:
        """Get the registration fee for a specific distance."""
        return self.registration_fee.get_fee(distance)


def load_races() -> list[Race]:
    """Load all races from the JSON file."""
    json_path = Path(__file__).parent / "races.json"

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Races file not found: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f)

    races = []
    for race_data in data["races"]:
        try:
            race = Race.from_dict(race_data)
            races.append(race)
        except (KeyError, ValueError) as e:
            print(f"Error loading race {race_data.get('id', 'unknown')}: {e}")
            continue

    return races
