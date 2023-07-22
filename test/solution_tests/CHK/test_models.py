
from unittest.mock import patch
from solutions.CHK.models import Offer, load_offers


def test_offer_apply_returns_offer_price_and_adjusted_count():
    offer = Offer(quantity=3, price=999)
    assert offer.apply(3) == (999, 0)

def test_offer_apply_no_offer_returns_zero_price_and_unchanged_count():
    offer = Offer(quantity=999, price=999)
    assert offer.apply(1) == (0, 1)

@patch(
    "solutions.CHK.static_prices.OFFERS", [
        {
            "product": "A",
            "quantity": 25,
            "price": 100,
        },
    ]
)
def test_load_offers_correctly_loads_offer_as_object():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 1
    assert len(loaded_offers["A"]) == 1
    loaded_offer = loaded_offers["A"][0]
    assert loaded_offer.quantity == 25
    assert loaded_offer.price == 100
    assert loaded_offer.side_effect == None

@patch(
    "solutions.CHK.static_prices.OFFERS", [
        {
            "product": "A",
            "quantity": 25,
            "price": 100,
        },
        {
            "product": "A",
            "quantity": 50,
            "price": 75,
        },
    ]
)
def test_load_offers_correctly_loads_multiple_offers_as_objects():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 1
    assert len(loaded_offers["A"]) == 2

    loaded_offer = loaded_offers["A"][0]
    assert loaded_offer.quantity == 25
    assert loaded_offer.price == 100
    assert loaded_offer.side_effect == None

    loaded_offer = loaded_offers["A"][1]
    assert loaded_offer.quantity == 50
    assert loaded_offer.price == 75
    assert loaded_offer.side_effect == None