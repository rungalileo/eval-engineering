from evals_demo_app.models.clothing import load_clothing


def test_load_clothing_returns_list_of_clothing_items():
    """Test that load_clothing returns a list of ClothingItem models."""
    clothing = load_clothing()
    assert isinstance(clothing, list)
    assert len(clothing) == 25

    assert all(hasattr(item, "type") for item in clothing)
    assert all(hasattr(item, "name") for item in clothing)
    assert all(hasattr(item, "description") for item in clothing)
    assert all(hasattr(item, "sizes") for item in clothing)
    assert all(hasattr(item, "color_options") for item in clothing)
    assert all(hasattr(item, "inseam_options") for item in clothing)
    assert all(hasattr(item, "fit_options") for item in clothing)
    assert all(hasattr(item, "length_options") for item in clothing)
    assert all(hasattr(item, "height_options") for item in clothing)
    assert all(hasattr(item, "support_level") for item in clothing)
    assert all(hasattr(item, "features") for item in clothing)
    assert all(hasattr(item, "modes") for item in clothing)
    assert all(hasattr(item, "product_image_urls") for item in clothing)
    assert all(hasattr(item, "runner_image_urls") for item in clothing)
    assert all(hasattr(item, "product_image_urls") for item in clothing)
    assert all(hasattr(item, "runner_image_urls") for item in clothing)

    assert [c for c in clothing if c.name == "Velocity Sprint Shorts"][
        0
    ].description == (
        "Lightweight 5-inch running shorts engineered with moisture-wicking fabric and reflective electric blue accents. Features an internal drawcord, zippered pocket, and seamless construction for chafe-free performance."
    )

    assert (
        [c for c in clothing if c.name == "TouchPoint Running Gloves"][
            0
        ].product_image_urls["Black/Signal Orange"]
        == "./public/images/clothing/adizone/touchpoint-running-gloves-black-signal-orange-clothing.png"
    )
    assert (
        [c for c in clothing if c.name == "TouchPoint Running Gloves"][
            0
        ].runner_image_urls["Black/Signal Orange"]
        == "./public/images/clothing/adizone/touchpoint-running-gloves-black-signal-orange-runner.png"
    )
