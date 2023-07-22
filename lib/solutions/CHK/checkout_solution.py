

from solutions.CHK import models
from solutions.CHK import static_prices

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = static_prices.ITEM_PRICES
    offers = models.load_offers()

    basket = models.Basket(skus=skus, prices=prices, offers=offers)

    return basket.calculate_price()

def order_skus_by_highest_to_lowest_price(skus: str, prices: dict[str, int]):
    ...