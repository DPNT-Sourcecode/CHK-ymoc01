

from collections import defaultdict
from solutions.CHK.static_prices import ITEM_PRICES, OFFERS

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    offers = OFFERS

    # For now, assuming SKUs are structured like AAABCAD
    product_counts: defaultdict(int) = {}
    for sku in skus:
        product_counts[sku] += 1
 
    basket_total = 0
    for product, count in product_counts.items():
        offer = offers.get("product")
        if offer:
            



    return basket_total




