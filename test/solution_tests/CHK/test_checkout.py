from solutions.CHK import checkout_solution
from solutions.CHK.models import Offer

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

def test_calculate_price_of_offers_for_single_offer_returns_offer_price_and_adjusted_count():
    offer = Offer(quantity=3, price=999)
    offers = [offer]
    assert checkout_solution.calculate_price_of_offers(offers, 3) == (999, 0)

def test_calculate_price_of_offers_for_no_offer_returns_zero_price_and_unchanged_count():
    offer = Offer(quantity=999, price=999)
    offers = [offer]
    assert checkout_solution.calculate_price_of_offers(offers, 1) == (0, 1)

def test_calculate_price_of_offers_for_multiple_offers_prioritises_high_quantity():
    offer_for_three = Offer(quantity=3, price=130)
    offer_for_five = Offer(quantity=5, price=200)

    offers = [offer_for_three, offer_for_five]
    count = 6

    total_offer_price, count_after_offers = checkout_solution.calculate_price_of_offers(offers, count)

    assert total_offer_price == 200
    assert count_after_offers == 1

def test_calculate_price_of_offers_for_multiple_offers_calculates_applies_both_offers():
    offer_for_three = Offer(quantity=3, price=130)
    offer_for_five = Offer(quantity=5, price=200)

    offers = [offer_for_three, offer_for_five]
    count = 9

    total_offer_price, count_after_offers = checkout_solution.calculate_price_of_offers(offers, count)

    assert total_offer_price == 330
    assert count_after_offers == 1






