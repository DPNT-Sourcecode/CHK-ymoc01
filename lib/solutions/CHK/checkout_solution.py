

from collections import defaultdict
from solutions.CHK.static_prices import ITEM_PRICES, OFFERS

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    offers = OFFERS

    # For now, assuming SKUs are structured like AAABCAD
    product_counts = defaultdict(int)
    for sku in skus:
        product_counts[sku] += 1
 
    basket_total = 0
    for product, count in product_counts.items():
        offer = offers.get(product)
        if offer:
            basket_total = calculate_offer_value(offer, count)
            adjusted_count = count - offer["quantity"]
        else:
            adjusted_count = count
        
        

        

            



    return basket_total

def calculate_offer_value(offer: dict[str, int], count: int) -> int:
    ...