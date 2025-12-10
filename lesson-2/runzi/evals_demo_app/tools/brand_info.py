import json
from langchain.tools import tool

from evals_demo_app.models.brands import load_brands

# Load all the brands with their shoes and clothing
brands = load_brands()


@tool(
    "get_brand_info",
    description="Get brand information for a given brand ID",
)
def get_brand_info(brand_id: str) -> str:
    """Get brand information for the given brand ID."""
    brand = next((b for b in brands if b.brand_id == brand_id), None)
    if brand:
        result = {
            "brand_name": brand.brand_name,
            "slogan": brand.slogan,
            "brand_story": brand.brand_story,
            "brand_logo_url": brand.brand_logo_url,
            "brand_full_logo_url": brand.brand_full_logo_url,
        }
        return json.dumps(result, indent=2)
    return json.dumps(None)


@tool(
    "get_brand_images",
    description="Get images for the brands",
)
def get_brand_images(brand_ids: list[str]) -> str:
    """Get shoe and runner image URLs for the given shoe IDs."""
    # Flatten the list of all shoes from all brands
    matching_brands = {b.brand_id: b for b in brands if b.brand_id in brand_ids}

    images = {}
    for brand_id in matching_brands:
        brand = matching_brands[brand_id]
        images[brand_id] = {
            "brand_logo_url": brand.brand_logo_url,
            "brand_full_logo_url": brand.brand_full_logo_url,
        }

    return json.dumps(images, indent=2)
