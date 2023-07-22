

from collections import defaultdict
from solutions.CHK.models import Offer, load_offers
from solutions.CHK.static_prices import ITEM_PRICES

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    all_offers = load_offers()

    # For now, assuming SKUs are structured like AAABCAD
    product_counts = defaultdict(int)
    for sku in skus:
        product_counts[sku] += 1

    basket_total = 0
    for product, count in product_counts.items():
        offer_adjusted_count = count

        offers_for_product = all_offers.get(product)
        if offers_for_product:
            offer_price, offer_adjusted_count, products_to_remove = calculate_price_of_offers(offers_for_product, count)
            for product in products_to_remove:
                if product in skus:
                    basket_total -= prices[product]
            basket_total += offer_price

        try:
            product_price = prices[product]
        except KeyError:
            return -1
        
        basket_total += offer_adjusted_count * product_price

    return basket_total

# This signature is becoming absolutely grim, refactor into something which knows about
# the overarching list of products, perhaps Basket model
def calculate_price_of_offers(offers: list[Offer], count: int) -> tuple[int, int, list[str]]:
    total_offer_price = 0
    count_after_offers = count
    free_products = []

    # At the moment, highest quantity offers benefit customer more, so prioritise those
    sorted_offers = sorted(offers, key=lambda x: x.quantity, reverse=True)
    for offer in sorted_offers:
        offer_price, count_after_offers = offer.apply(count_after_offers)
        total_offer_price += offer_price

        if offer_price != 0 and offer.side_effect is not None:
            free_products.append(offer.side_effect.product)


    return total_offer_price, count_after_offers, free_products


