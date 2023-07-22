from solutions.CHK import checkout_solution

# def test_checkout_for_basket_with_item_and_no_offers_returns_item_price():
#     sku_string = "A"
#     assert checkout_solution.checkout(sku_string) == 50

# def test_checkout_for_basket_with_items_valid_for_offers_returns_offer_price():
#     sku_string = "AAA"
#     assert checkout_solution.checkout(sku_string) == 130

def test_calculate_price_of_offers_for_single_offer_returns_offer_price():
    offer = {
        "quantity": 3,
        "offer_price": 999,
    }
    assert checkout_solution.calculate_price_of_offers(offer, 3) == 999