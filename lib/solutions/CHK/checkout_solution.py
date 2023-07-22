

from solutions.CHK import models
from solutions.CHK import static_prices

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = static_prices.ITEM_PRICES
    offers = models.load_offers()

    try:
        skus_sorted_by_price = order_skus_by_highest_to_lowest_price(skus, prices)
    except KeyError:
        return -1

    basket = models.Basket(skus=skus_sorted_by_price, prices=prices, offers=offers)

    return basket.calculate_price()

def order_skus_by_highest_to_lowest_price(skus: str, prices: dict[str, int]) -> str:
    skus_and_prices = []

    for sku in skus:
        skus_and_prices.append((sku, prices[sku]))


    ordered_skus_and_prices = sorted(skus_and_prices, key=lambda x: x[1], reverse=True)

    ordered_skus = [sku for sku, _  in ordered_skus_and_prices]
    return "".join(ordered_skus)