from unittest.mock import patch

import pytest
from solutions.CHK.models import (
    FreeProductOffer,
    DiscountOffer,
    GroupDiscountOffer,
    load_offers,
)


def test_offer_apply_returns_offer_price_and_empty_sku():
    offer = DiscountOffer(product="A", quantity=3, price=999)
    assert offer.apply("AAA") == (999, "")


def test_offer_apply_no_offer_returns_zero_price_and_unchanged_sku():
    offer = DiscountOffer(product="A", quantity=999, price=999)
    assert offer.apply("A") == (0, "A")


def test_offer_times_offer_can_be_applied_when_offer_can_be_applied_returns_greater_than_zero():
    offer = DiscountOffer(product="A", quantity=3, price=999)
    skus = "AAAAAAA"

    assert offer.times_offer_can_be_applied(skus) == 2


def test_offer_times_offer_can_be_applied_when_offer_cant_be_applied_returns_zero():
    offer = DiscountOffer(product="A", quantity=3, price=999)
    skus = "A"

    assert offer.times_offer_can_be_applied(skus) == 0


@patch(
    "solutions.CHK.static_prices.OFFERS",
    [
        {
            "product": "A",
            "quantity": 25,
            "price": 100,
        },
    ],
)
def test_load_offers_correctly_loads_offer_as_object():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 1

    loaded_offer = loaded_offers[0]
    assert isinstance(loaded_offer, DiscountOffer)
    assert loaded_offer.product == "A"
    assert loaded_offer.quantity == 25
    assert loaded_offer.price == 100


@patch(
    "solutions.CHK.static_prices.OFFERS",
    [
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
    ],
)
def test_load_offers_correctly_loads_multiple_offers_as_objects():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 2

    loaded_offer = loaded_offers[0]
    assert isinstance(loaded_offer, DiscountOffer)
    assert loaded_offer.product == "A"
    assert loaded_offer.quantity == 25
    assert loaded_offer.price == 100

    loaded_offer = loaded_offers[1]
    assert isinstance(loaded_offer, DiscountOffer)
    assert loaded_offer.product == "A"
    assert loaded_offer.quantity == 50
    assert loaded_offer.price == 75


@patch(
    "solutions.CHK.static_prices.OFFERS",
    [
        {"product": "A", "quantity": 25, "free_product": "B"},
    ],
)
def test_load_offers_correctly_loads_offer_with_free_product():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 1

    loaded_offer = loaded_offers[0]
    assert isinstance(loaded_offer, FreeProductOffer)

    assert loaded_offer.product == "A"
    assert loaded_offer.quantity == 25
    assert loaded_offer.free_product == "B"


@patch(
    "solutions.CHK.static_prices.OFFERS",
    [
        {"product": "A", 
         "quantity": 25,
         "price": 100,
         "multibuy_with": ["B", "C"]},
    ],
)
def test_load_offers_correctly_loads_offer_with_multibuy_products():
    loaded_offers = load_offers()
    assert len(loaded_offers) == 1

    loaded_offer = loaded_offers[0]
    assert isinstance(loaded_offer, GroupDiscountOffer)

    assert loaded_offer.product == "A"
    assert loaded_offer.quantity == 25
    assert loaded_offer.price == 100
    assert loaded_offer.mutlibuy_with_products == ["B", "C"]


@pytest.mark.parametrize(
    "skus", 
    [
        "ABCDE",
        "ABC",
        "DEE",
        "ABCFGH"
    ]
)
def test_group_discount_offer_times_offer_can_be_applied_returns_one_for_one_group(
    skus,
):
    discount_offer = GroupDiscountOffer(
        product="A", quantity=3, price=0, mutlibuy_with_products=["B", "C", "D", "E"]
    )

    assert discount_offer.times_offer_can_be_applied(skus) == 1

def test_group_discount_offer_apply_correctly_calculates_discount_and_removes_skus():
    discount_offer = GroupDiscountOffer(
        product="A", quantity=3, price=30, mutlibuy_with_products=["B", "C", "D", "E"]
    )

    skus = "ABCDE"

    assert discount_offer.apply(skus) == (30, "DE")