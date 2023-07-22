

from collections import defaultdict
from typing import Optional
from pydantic import BaseModel

from solutions.CHK import static_prices

class FreeProductSideEffect(BaseModel):
    product: str

class Offer(BaseModel):
    quantity: int
    price: int
    side_effect: Optional[FreeProductSideEffect] = None

    def apply(self, count: int) -> tuple[int, int]:
        number_of_offer_occurences = int(count / self.quantity)

        offers_price = number_of_offer_occurences * self.price
        count_after_offers = count - (self.quantity * int(count / self.quantity))

        return offers_price, count_after_offers

class Basket(BaseModel):
    skus: str
    prices: dict[str, int]
    offers: list[Offer]

    def calculate_price():
        ...

    def _apply_free_products():

        ...
    
    def _apply_offers():
        ...


def load_offers() -> dict[str, Offer]:
    offers = static_prices.OFFERS
    parsed_offers = defaultdict(list)

    for offer in offers:
        if free_product := offer.get("free_product"):
            side_effect = FreeProductSideEffect(product=free_product)
        else:
            side_effect = None

        parsed_offers[offer["product"]].append(
            Offer(
                quantity=offer["quantity"], 
                price=offer["price"],
                side_effect=side_effect
            )
        )

    return parsed_offers

