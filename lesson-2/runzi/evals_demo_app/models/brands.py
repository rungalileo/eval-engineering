from __future__ import annotations
from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any

from evals_demo_app.models.clothing import ClothingItem, load_clothing
from evals_demo_app.models.shoes import Shoe, load_shoes


@dataclass(frozen=True)
class Brand:
    """Represents a athletics wear brand."""

    brand_id: str
    brand_name: str
    slogan: str
    brand_story: str
    brand_logo_url: str
    brand_full_logo_url: str

    shoes: list[Shoe]
    apparel: list[ClothingItem]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Brand":
        """Create a Brand object from a dictionary."""
        return Brand(
            brand_id=data["brand_id"],
            brand_name=data["brand_name"],
            slogan=data["slogan"],
            brand_story=data["brand_story"],
            brand_logo_url=f"./public/images/brands/{data['brand_id']}-logo-only.png",
            brand_full_logo_url=f"./public/images/brands/{data['brand_id']}-full.png",
            shoes=[],
            apparel=[],
        )


def load_brands() -> list[Brand]:
    """
    Load and return the list of Brand objects from the brands.json file.
    """
    path = Path(os.path.abspath(__file__)).parent / "brands.json"

    data = json.loads(path.read_text(encoding="utf-8"))
    brands = [Brand.from_dict(item) for item in data.get("brands", [])]

    # Load shoes and clothing for each brand
    shoes = load_shoes()
    clothing = load_clothing()

    for brand in brands:
        brand.shoes.extend([shoe for shoe in shoes if shoe.brand_id == brand.brand_id])
        brand.apparel.extend(
            [item for item in clothing if item.brand_id == brand.brand_id]
        )

    return brands
