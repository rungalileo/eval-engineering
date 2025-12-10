from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import json
import os
from pathlib import Path
from typing import Any, Optional


class Category(StrEnum):
    """Shoe category enumeration."""

    DAILY_TRAINER = "daily_trainer"
    TEMPO_TRAINER = "tempo_trainer"
    CARBON_RACER = "carbon_racer"
    TRAIL = "trail"
    MAX_CUSHION = "max_cushion"
    STABILITY_TRAINER = "stability_trainer"


class IntendedUse(StrEnum):
    """Shoe intended use enumeration."""

    # Common road uses
    EASY_RUNS = "easy_runs"
    DAILY_MILES = "daily_miles"
    RECOVERY = "recovery"
    LONG_RUNS = "long_runs"
    WALKING = "walking"
    LONG_EASY = "long_easy"
    ALL_DAY_STANDING = "all_day_standing"
    WALK_COMMUTE = "walk_commute"
    RECOVERY_RUNS = "recovery_runs"

    # Speed/tempo/racing
    TEMPO_RUNS = "tempo_runs"
    INTERVALS = "intervals"
    LONG_PROGRESSIONS = "long_progressions"
    SPEEDWORK = "speedwork"
    LONG_TEMPOS = "long_tempos"
    SHORT_RACES = "short_races"
    RACE_DAY_5K_TO_MARATHON = "race_day_5k_to_marathon"
    RACE_DAY_10K_TO_MARATHON = "race_day_10k_to_marathon"
    RACE_DAY_HALF_TO_MARATHON = "race_day_half_to_marathon"

    # Trail
    TRAIL_RUNS = "trail_runs"
    TECHNICAL_TERRAIN = "technical_terrain"
    LIGHT_HIKING = "light_hiking"
    MOUNTAIN_TRAILS = "mountain_trails"
    ULTRAS = "ultras"
    FIRE_ROADS = "fire_roads"
    ALL_TRAIL = "all_trail"
    DOOR_TO_TRAIL = "door_to_trail"
    RAINY_DAYS = "rainy_days"
    MUDDY_TRACKS = "muddy_tracks"
    ROCKY_PATHS = "rocky_paths"

    # Support
    MILD_PRONATION_SUPPORT = "mild_pronation_support"


@dataclass(frozen=True)
class Materials:
    """Represents the materials used in different parts of a shoe."""

    upper: str
    midsole: str
    outsole: str
    plate: Optional[str] = None


@dataclass(frozen=True)
class Tech:
    """Represents the technologies used in different parts of a shoe."""

    rocker: str
    compound_names: list[str]
    insole: Optional[str] = None


@dataclass(frozen=True)
class Specs:
    """Shoe physical specifications."""

    weight_mens_9_usa_oz: float
    drop_mm: int
    stack_forefoot_mm: int
    stack_heel_mm: int


class Width(StrEnum):
    """Shoe width enumeration."""

    NARROW = "narrow"
    STANDARD = "standard"
    WIDE = "wide"


@dataclass(frozen=True)
class Fit:
    """Represents the available fit characteristics of a shoe."""

    widths: list[Width]
    notes: str


@dataclass(frozen=True)
class Shoe:
    """Represents a shoe with various attributes."""

    brand_id: str
    shoe_id: str
    model_name: str
    category: Category
    intended_use: list[IntendedUse]
    marketing_copy: str
    materials: Materials
    tech: Tech
    specs: Specs
    fit: Fit
    colors: list[str]
    price_usd: int
    release_year: int
    shoe_image_url: Optional[str] = None
    runner_image_url: Optional[str] = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Shoe":
        """Create a Shoe object from a dictionary."""
        return Shoe(
            brand_id=data["brand_id"],
            shoe_id=data["shoe_id"],
            model_name=data["model_name"],
            category=Category(data["category"]),
            intended_use=[IntendedUse(i) for i in data["intended_use"]],
            marketing_copy=data["marketing_copy"],
            materials=Materials(**data["materials"]),
            tech=Tech(**data["tech"]),
            specs=Specs(**data["specs"]),
            fit=Fit(**data["fit"]),
            colors=data["colors"],
            price_usd=data["price_usd"],
            release_year=data["release_year"],
            shoe_image_url=f"./public/images/shoes/{data['brand_id']}/{data['shoe_id']}-shoes.png",
            runner_image_url=f"./public/images/shoes/{data['brand_id']}/{data['shoe_id']}-runner.png",
        )


def load_shoes() -> list[Shoe]:
    """
    Load and return the list of Shoe objects from the shoes.json file.
    """
    path = Path(os.path.abspath(__file__)).parent / "shoes.json"

    data = json.loads(path.read_text(encoding="utf-8"))
    return [Shoe.from_dict(item) for item in data.get("shoes", [])]
