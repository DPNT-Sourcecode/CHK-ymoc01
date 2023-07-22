

from collections import defaultdict
from solutions.CHK.static_prices import ITEM_PRICES, OFFERS

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    offers = OFFERS

    # For now, assuming SKUs are structured like AAABCAD
    basket_total = 0
    basket_counts: defaultdict(int) = {}
    for sku in skus:
        basket_counts[sku] += 1
        # try:
        #     basket_total += prices[sku]
        # except KeyError:
        #     return -1
        
    return basket_total




