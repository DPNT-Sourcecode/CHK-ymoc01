

from solutions.CHK.static_prices import ITEM_PRICES, OFFERS

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    offers = OFFERS

    # For now, assuming SKUs are structured like AAABCAD
    basket_total = 0
    for sku in skus:
        try:
            basket_total += prices[sku]
        except KeyError:
            return -1
        
    return basket_total



