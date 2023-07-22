from solutions.CHK import checkout_solution

def test_checkout_for_basket_with_item_and_no_offers_returns_item_price():
    sku_string = "A"
    assert checkout_solution(sku_string) == 50

