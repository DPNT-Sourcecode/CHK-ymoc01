from solutions.CHK import checkout_solution
from solutions.CHK.models import FreeProductSideEffect, Offer

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
