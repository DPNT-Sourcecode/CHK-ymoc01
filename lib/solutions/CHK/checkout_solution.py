

from solutions.CHK.models import Basket, load_offers
from solutions.CHK import static_prices

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = static_prices.ITEM_PRICES
    offers = load_offers()

    breakpoint()
    basket = Basket(skus=skus, prices=prices, offers=offers)

    return basket.calculate_price()