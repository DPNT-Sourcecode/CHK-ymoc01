from unittest.mock import patch

import pytest
from solutions.CHK import checkout_solution
from solutions.CHK.models import DiscountOffer, FreeProductOffer


# TODO what happens if the prices change, which reqs say offers do weekly
# fixtures and patching probably quickest way around this, prefer factoryboy
def test_checkout_for_basket_with_item_and_no_offers_returns_item_price():
    sku_string = "A"
    assert checkout_solution.checkout(sku_string) == 50


def test_checkout_for_basket_with_items_valid_for_offers_returns_offer_price():
    sku_string = "AAA"
    assert checkout_solution.checkout(sku_string) == 130


def test_checkout_for_basket_with_offers_and_singles_returns_sum():
    sku_string = "AAAABBBCDD"
    assert checkout_solution.checkout(sku_string) == 180 + 75 + 20 + 30


def test_checkout_for_basket_with_unpriced_items_returns_minus_1():
    sku_string = "@"
    assert checkout_solution.checkout(sku_string) == -1


def test_checkout_for_basket_with_free_product_removes_free_product_cost():
    sku_string = "BEE"
    assert checkout_solution.checkout(sku_string) == 80


def test_checkout_for_basket_with_free_product_which_has_offer_removes_offer():
    sku_string = "BBEE"
    assert checkout_solution.checkout(sku_string) == 110


def test_checkout_for_basket_with_lots_of_products_with_overlapping_rules():
    sku_string = "AAAAABBBBCCDDDDEEEE"
    assert checkout_solution.checkout(sku_string) == 200 + 45 + 40 + 60 + 160


@patch("solutions.CHK.models.load_offers")
@patch("solutions.CHK.static_prices.ITEM_PRICES", {"A": 50})
def test_checkout_for_basket_where_mutliple_offers_for_same_product_prioritises_high_quantity(
    mocked_load_offers,
):
    offer_for_three = DiscountOffer(product="A", quantity=3, price=130)
    offer_for_five = DiscountOffer(product="A", quantity=5, price=200)

    mocked_load_offers.return_value = [offer_for_three, offer_for_five]
    sku_string = "AAAAAA"

    assert checkout_solution.checkout(sku_string) == 200 + 50


@patch("solutions.CHK.models.load_offers")
@patch("solutions.CHK.static_prices.ITEM_PRICES", {"A": 10})
def test_checkout_for_basket_where_offers_remove_the_offered_product(
    mocked_load_offers,
):
    offer_for_self_removal = FreeProductOffer(product="A", quantity=3, free_product="A")

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAA"

    assert checkout_solution.checkout(sku_string) == 20


@patch("solutions.CHK.models.load_offers")
@patch("solutions.CHK.static_prices.ITEM_PRICES", {"A": 10})
def test_checkout_for_basket_where_offers_remove_the_offered_product_and_applies_offer(
    mocked_load_offers,
):
    offer_for_self_removal = FreeProductOffer(product="A", quantity=3, free_product="A")

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAAAA"

    assert checkout_solution.checkout(sku_string) == 40


@patch("solutions.CHK.models.load_offers")
@patch("solutions.CHK.static_prices.ITEM_PRICES", {"A": 10})
def test_checkout_for_basket_where_offers_remove_the_product_when_count_even_has_no_effect(
    mocked_load_offers,
):
    offer_for_self_removal = FreeProductOffer(product="A", quantity=3, free_product="A")

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAAA"

    assert checkout_solution.checkout(sku_string) == 30

def test_order_skus_by_highest_to_lowest_price()

# Explicit rule testing for CHK_R4
def test_checkout_for_basket_A_rule_1():
    sku_string = "AAA"

    assert checkout_solution.checkout(sku_string) == 130


def test_checkout_for_basket_with_A_rule_1():
    sku_string = "AAAAA"

    assert checkout_solution.checkout(sku_string) == 200


def test_checkout_for_basket_with_B_rule():
    sku_string = "BB"

    assert checkout_solution.checkout(sku_string) == 45


def test_checkout_for_basket_with_E_rule():
    sku_string = "BEE"

    assert checkout_solution.checkout(sku_string) == 80


def test_checkout_for_basket_with_F_rule():
    sku_string = "FFF"

    assert checkout_solution.checkout(sku_string) == 20


def test_checkout_for_basket_with_H_rule_1():
    sku_string = "HHHHH"

    assert checkout_solution.checkout(sku_string) == 45


def test_checkout_for_basket_with_H_rule_2():
    sku_string = "HHHHHHHHHH"

    assert checkout_solution.checkout(sku_string) == 80


def test_checkout_for_basket_with_K_rule():
    sku_string = "KK"

    assert checkout_solution.checkout(sku_string) == 120


def test_checkout_for_basket_with_N_rule():
    sku_string = "NNNM"

    assert checkout_solution.checkout(sku_string) == 120


def test_checkout_for_basket_with_P_rule():
    sku_string = "PPPPP"

    assert checkout_solution.checkout(sku_string) == 200


def test_checkout_for_basket_with_Q_rule():
    sku_string = "QQQ"

    assert checkout_solution.checkout(sku_string) == 80


def test_checkout_for_basket_with_R_rule():
    sku_string = "RRRQ"

    assert checkout_solution.checkout(sku_string) == 150


def test_checkout_for_basket_with_U_rule():
    sku_string = "UUUU"

    assert checkout_solution.checkout(sku_string) == 120


def test_checkout_for_basket_with_V_rule_1():
    sku_string = "VV"

    assert checkout_solution.checkout(sku_string) == 90


def test_checkout_for_basket_with_V_rule_2():
    sku_string = "VVV"

    assert checkout_solution.checkout(sku_string) == 130

@pytest.mark.parametrize(
    "sku_string", 
    [
        "STXYZ",
        "TXYZS",
        "XYZST",
        "YZSTX",
        "ZSTXY"
    ]
)
def test_checkout_for_basket_with_group_discount(sku_string):
    # The cheapest pair, plus the price of the offer
    assert checkout_solution.checkout(sku_string) == 37 + 45