

from typing import Optional
from pydantic import BaseModel

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