from evals_demo_app.models.shoes import load_shoes


def test_load_shoes_returns_list_of_shoe_models():
    """Test that load_shoes returns a list of Shoe models."""
    shoes = load_shoes()
    assert isinstance(shoes, list)
    assert len(shoes) == 20

    assert all(hasattr(shoe, "shoe_id") for shoe in shoes)
    assert all(hasattr(shoe, "model_name") for shoe in shoes)
    assert all(hasattr(shoe, "category") for shoe in shoes)
    assert all(hasattr(shoe, "intended_use") for shoe in shoes)
    assert all(hasattr(shoe, "marketing_copy") for shoe in shoes)
    assert all(hasattr(shoe, "materials") for shoe in shoes)
    assert all(hasattr(shoe, "tech") for shoe in shoes)
    assert all(hasattr(shoe, "specs") for shoe in shoes)
    assert all(hasattr(shoe, "fit") for shoe in shoes)
    assert all(hasattr(shoe, "colors") for shoe in shoes)
    assert all(hasattr(shoe, "price_usd") for shoe in shoes)
    assert all(hasattr(shoe, "release_year") for shoe in shoes)
    assert all(hasattr(shoe, "shoe_image_url") for shoe in shoes)
    assert all(hasattr(shoe, "runner_image_url") for shoe in shoes)

    assert [s for s in shoes if s.shoe_id == "glyceride-21"][0].marketing_copy == (
        "Luxuriously soft foam tuned with a guidance rail for easy, consistent miles."
    )

    assert [s for s in shoes if s.shoe_id == "endurfin-pro-4"][
        0
    ].shoe_image_url == "./public/images/shoes/saukion/endurfin-pro-4-shoes.png"
    assert [s for s in shoes if s.shoe_id == "endurfin-pro-4"][
        0
    ].runner_image_url == "./public/images/shoes/saukion/endurfin-pro-4-runner.png"
