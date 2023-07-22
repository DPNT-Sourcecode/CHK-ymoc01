
from unittest.mock import patch
from solutions.CHK import checkout_solution
from solutions.CHK.models import PriceOffer, FreeProductOffer

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
    sku_string = "Z"
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

@patch(
    "solutions.CHK.models.load_offers"
)
@patch(
    "solutions.CHK.static_prices.ITEM_PRICES", {
        "A": 50
    }
)
def test_checkout_for_basket_where_mutliple_offers_for_same_product_prioritises_high_quantity(mocked_load_offers):
    offer_for_three = PriceOffer(product="A", quantity=3, price=130)
    offer_for_five = PriceOffer(product="A", quantity=5, price=200)

    mocked_load_offers.return_value = [offer_for_three, offer_for_five]
    sku_string = "AAAAAA"
    
    assert checkout_solution.checkout(sku_string) == 200 + 50


@patch(
    "solutions.CHK.models.load_offers"
)
@patch(
    "solutions.CHK.static_prices.ITEM_PRICES", {
        "A": 10
    }
)
def test_checkout_for_basket_where_offers_remove_the_offered_product(mocked_load_offers):
    offer_for_self_removal = FreeProductOffer(
        product="A",
        quantity=3,
        free_product="A"
    )

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAA"
    
    assert checkout_solution.checkout(sku_string) == 20

@patch(
    "solutions.CHK.models.load_offers"
)
@patch(
    "solutions.CHK.static_prices.ITEM_PRICES", {
        "A": 10
    }
)
def test_checkout_for_basket_where_offers_remove_the_offered_product_and_applies_offer(mocked_load_offers):
    offer_for_self_removal = FreeProductOffer(
        product="A",
        quantity=3,
        free_product="A"
    )

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAAAA"
    
    assert checkout_solution.checkout(sku_string) == 40

@patch(
    "solutions.CHK.models.load_offers"
)
@patch(
    "solutions.CHK.static_prices.ITEM_PRICES", {
        "A": 10
    }
)
def test_checkout_for_basket_where_offers_remove_the_product_when_count_even_has_no_effect(mocked_load_offers):
    offer_for_self_removal = FreeProductOffer(
        product="A",
        quantity=3,
        free_product="A"
    )

    mocked_load_offers.return_value = [offer_for_self_removal]
    sku_string = "AAAA"
    
    assert checkout_solution.checkout(sku_string) == 30

