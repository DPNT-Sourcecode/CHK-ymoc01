

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
        offer_adjusted_count = count

        offer = offers.get(product)
        if offer:
            offer_price, offer_adjusted_count = calculate_price_of_offers(offer, count)
            basket_total += offer_price

        try:
            product_price = prices[product]
        except KeyError:
            return -1
        
        basket_total += offer_adjusted_count * product_price

    return basket_total

def calculate_price_of_offers(offer: dict[str, int], count: int) -> tuple[int, int]:
    offer_quantity = offer["quantity"]

    # Dividing and then rounding down, thereby dropping any remainder
    number_of_offer_occurences = int(count / offer_quantity)

    offers_price = number_of_offer_occurences * offer["price"]
    count_after_offers = count - (offer_quantity * int(count / offer_quantity))

    return offers_price, count_after_offers