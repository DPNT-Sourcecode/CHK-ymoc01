

from typing import Optional
from pydantic import BaseModel

from solutions.CHK.static_prices import OFFERS

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
    
def load_offers() -> dict[str, Offer]:
    offers = OFFERS
    parsed_offers = []

    for product, offer in offers.items():
        parsed_offers[product] = Offer(
            quantity=offer["quantity"], 
            price=offer["price"]
        )