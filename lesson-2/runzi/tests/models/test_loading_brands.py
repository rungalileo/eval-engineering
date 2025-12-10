from evals_demo_app.models.brands import load_brands


def test_load_brands_returns_list_of_brand_models():
    """Test that load_brands returns a list of Brand models."""
    brands = load_brands()
    assert isinstance(brands, list)
    assert len(brands) == 5

    assert all(hasattr(brand, "shoes") for brand in brands)
    assert all(hasattr(brand, "apparel") for brand in brands)
    assert all(hasattr(brand, "brand_id") for brand in brands)
    assert all(hasattr(brand, "brand_name") for brand in brands)
    assert all(hasattr(brand, "slogan") for brand in brands)
    assert all(hasattr(brand, "brand_story") for brand in brands)
    assert all(hasattr(brand, "brand_logo_url") for brand in brands)
    assert all(hasattr(brand, "brand_full_logo_url") for brand in brands)

    assert [b for b in brands if b.brand_id == "adizone"][0].brand_story == (
        "Adizone focuses on featherweight constructions and propulsion systems to turn training cycles into PRs."
    )

    assert len([b for b in brands if b.brand_id == "adizone"][0].shoes) == 4
    assert len([b for b in brands if b.brand_id == "adizone"][0].apparel) == 5

    assert [b for b in brands if b.brand_id == "brukes"][
        0
    ].brand_logo_url == "./public/images/brands/brukes-logo-only.png"
    assert [b for b in brands if b.brand_id == "brukes"][
        0
    ].brand_full_logo_url == "./public/images/brands/brukes-full.png"
