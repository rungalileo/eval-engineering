from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import json
import os
from pathlib import Path
from typing import Any, Optional


class ClothingType(StrEnum):
    """Clothing type enumeration."""

    RUNNING_SHORTS = "running_shorts"
    RUNNING_SHIRT_SHORT_SLEEVE = "running_shirt_short_sleeve"
    RUNNING_SHIRT_LONG_SLEEVE = "running_shirt_long_sleeve"
    RUNNING_TIGHTS = "running_tights"
    SOCKS = "socks"
    JACKET = "jacket"
    SPORTS_BRA = "sports_bra"
    HAT = "hat"
    GLOVES = "gloves"
    RUNNING_LIGHTS = "running_lights"


@dataclass(frozen=True)
class ColorOption:
    """Represents a color option for a clothing item."""

    name: str
    primary: str
    accent: Optional[str] = None
    light_color: Optional[str] = None


@dataclass(frozen=True)
class ClothingItem:
    """Represents a clothing item with various attributes."""

    brand_id: str
    type: ClothingType
    name: str
    id: str
    description: str
    sizes: list[str]
    color_options: list[ColorOption]
    product_image_urls: dict[str, str]
    runner_image_urls: dict[str, str]

    # Optional fields that vary by clothing type
    price: Optional[float] = None
    inseam_options: Optional[list[str]] = None
    fit_options: Optional[list[str]] = None
    length_options: Optional[list[str]] = None
    height_options: Optional[list[str]] = None
    support_level: Optional[list[str]] = None
    features: Optional[list[str]] = None
    modes: Optional[list[str]] = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ClothingItem":
        """Create a ClothingItem object from a dictionary."""
        color_options = [
            ColorOption(
                name=color["name"],
                primary=color["primary"],
                accent=color.get("accent"),
                light_color=color.get("light_color"),
            )
            for color in data["color_options"]
        ]
        # Compute a stable id from the provided `id` or the name
        id_value = data.get("id")
        if not id_value:
            id_value = data["name"].lower().replace(" ", "-").replace("/", "-")

        clothing_item = ClothingItem(
            brand_id=data["brand_id"],
            type=ClothingType(data["type"]),
            name=data["name"],
            id=id_value,
            price=(float(data["price"]) if data.get("price") is not None else None),
            description=data["description"],
            sizes=data["sizes"],
            color_options=color_options,
            inseam_options=data.get("inseam_options"),
            fit_options=data.get("fit_options"),
            length_options=data.get("length_options"),
            height_options=data.get("height_options"),
            support_level=data.get("support_level"),
            features=data.get("features"),
            modes=data.get("modes"),
            product_image_urls={},
            runner_image_urls={},
        )

        for color in data.get("color_options", []):
            slug = clothing_item.id
            if "accent" in color:
                clothing_item.product_image_urls[color["name"]] = (
                    f"./public/images/clothing/{clothing_item.brand_id}/{slug}-{color['primary'].replace(' ', '-')}-{color['accent'].replace(' ', '-')}-clothing.png"
                )
                clothing_item.runner_image_urls[color["name"]] = (
                    f"./public/images/clothing/{clothing_item.brand_id}/{slug}-{color['primary'].replace(' ', '-')}-{color['accent'].replace(' ', '-')}-runner.png"
                )
            elif "light_color" in color:
                clothing_item.product_image_urls[color["name"]] = (
                    f"./public/images/clothing/{clothing_item.brand_id}/{slug}-{color['primary'].replace(' ', '-')}-{color['light_color'].replace(' ', '-')}-clothing.png"
                )
                clothing_item.runner_image_urls[color["name"]] = (
                    f"./public/images/clothing/{clothing_item.brand_id}/{slug}-{color['primary'].replace(' ', '-')}-{color['light_color'].replace(' ', '-')}-runner.png"
                )
            else:
                raise ValueError(
                    "Color option must have either 'accent' or 'light_color'."
                )

        return clothing_item


def load_clothing() -> list[ClothingItem]:
    """
    Load and return the list of ClothingItem objects from the clothing.json file.
    """
    path = Path(os.path.abspath(__file__)).parent / "clothing.json"

    data = json.loads(path.read_text(encoding="utf-8"))
    return [ClothingItem.from_dict(item) for item in data.get("clothing", [])]
