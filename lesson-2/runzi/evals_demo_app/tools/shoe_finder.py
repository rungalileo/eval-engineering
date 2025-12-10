import json
from dataclasses import asdict
from typing import Optional

from langchain.tools import tool

from evals_demo_app.models.brands import load_brands
from evals_demo_app.models.shoes import Category, IntendedUse, Width

# Load all the brands with their shoes and clothing
brands = load_brands()


@tool(
    "recommend_shoes",
    description="Find shoes based on category/brand/use/width/price",
)
def recommend_shoes(
    category: Optional[Category] = None,
    brand: Optional[str] = None,
    intended_use: Optional[IntendedUse] = None,
    width: Optional[Width] = None,
    max_price: Optional[int] = None,
) -> str:
    """Recommend shoes based on the provided filters."""
    # Flatten the list of all shoes from all brands
    shoes = (shoe for brand in brands for shoe in brand.shoes)
    results = list(shoes)

    if category is not None:
        results = [s for s in results if s.category == category]

    if brand:
        results = [s for s in results if s.brand_id == brand]

    if intended_use is not None:
        results = [s for s in results if intended_use in s.intended_use]

    if width is not None:
        results = [s for s in results if width in s.fit.widths]

    if max_price is not None:
        results = [s for s in results if s.price_usd <= max_price]

    # Convert to JSON
    response = json.dumps([asdict(shoe) for shoe in results], indent=2)
    return response


@tool(
    "get_shoe_images",
    description="Get images for the shoes",
)
def get_shoe_images(shoe_ids: list[str]) -> str:
    """Get shoe and runner image URLs for the given shoe IDs."""
    # Flatten the list of all shoes from all brands
    shoes = (shoe for brand in brands for shoe in brand.shoes)

    images = {}
    for shoe_id in shoe_ids:
        shoe = next((s for s in shoes if s.shoe_id == shoe_id), None)
        if shoe:
            images[shoe_id] = {
                "shoe_image_url": shoe.shoe_image_url,
                "runner_image_url": shoe.runner_image_url,
            }
        else:
            images[shoe_id] = {
                "shoe_image_url": None,
                "runner_image_url": None,
            }
    return json.dumps(images)
