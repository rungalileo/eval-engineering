import json
from dataclasses import asdict
from typing import Optional

from langchain.tools import tool

from evals_demo_app.models.brands import load_brands
from evals_demo_app.models.clothing import ClothingType
from evals_demo_app.models.shoes import Category, IntendedUse, Width

# Load all the brands with their shoes and clothing
brands = load_brands()


@tool(
    "recommend_apparel",
    description="Find running clothing and accessories based on category/brand/use/size/price",
)
def recommend_apparel(
    type: Optional[ClothingType] = None,
    brand: Optional[str] = None,
    max_price: Optional[float] = None,
) -> str:
    """Recommend shoes based on the provided filters."""
    # Flatten the list of all shoes from all brands
    apparel_items = (apparel for brand in brands for apparel in brand.apparel)
    results = list(apparel_items)

    if type is not None:
        results = [a for a in results if a.type == type]

    if brand is not None:
        results = [a for a in results if a.brand_id.lower() == brand.lower()]

    if max_price is not None:
        results = [a for a in results if a.price is not None and a.price <= max_price]

    # Convert to JSON
    response = json.dumps([asdict(apparel) for apparel in results], indent=2)
    return response


@tool(
    "get_apparel_images",
    description="Get images for the apparel",
)
def get_apparel_images(apparel_ids: list[str]) -> str:
    """Get apparel and runner image URLs for the given apparel IDs."""
    # Flatten the list of all apparel from all brands
    apparel = (item for brand in brands for item in brand.apparel)

    images = {}
    for apparel_id in apparel_ids:
        item = next((a for a in apparel if a.id == apparel_id), None)
        if item:
            for color in item.color_options:
                images[f"{apparel_id}_{color.name}"] = {
                    "apparel_image_url": item.product_image_urls.get(color.name),
                    "runner_image_url": item.runner_image_urls.get(color.name),
                }
    return json.dumps(images)
