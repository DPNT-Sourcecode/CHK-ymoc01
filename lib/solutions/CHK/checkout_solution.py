

from solutions.CHK.models import Basket, load_offers
from solutions.CHK.static_prices import ITEM_PRICES

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: str) -> int:
    prices = ITEM_PRICES
    offers = load_offers()

    basket = Basket(skus=skus, prices=prices, offers=offers)

    return basket.calculate_price()
