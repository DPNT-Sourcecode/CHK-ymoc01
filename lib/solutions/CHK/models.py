
from pydantic import BaseModel

from solutions.CHK import static_prices

class Offer(BaseModel):
    product: str
    quantity: int

    def times_offer_can_be_applied(self, skus: str) -> int:
        count = skus.count(self.product)

        if count < self.quantity:
            return 0
        
        return int(count / self.quantity)

class PriceOffer(Offer):
    price: int

    def apply(self, count: int) -> tuple[int, int]:
        number_of_offer_occurences = int(count / self.quantity)

        offers_price = number_of_offer_occurences * self.price
        count_to_remove = (self.quantity * int(count / self.quantity))

        return offers_price, count_to_remove

class FreeProductOffer(Offer):
    free_product: str

    def apply(self, skus: str) -> str:
        skus_after_processing = skus

        return skus_after_processing.replace(self.free_product, "", self.times_offer_can_be_applied(skus))


class Basket(BaseModel):
    skus: str
    prices: dict[str, int]
    offers: list[Offer]

    def calculate_price(self):
        skus_to_process = self.skus

        skus_to_process = self._apply_free_products(skus_to_process)

        skus_to_process, offer_price = self._apply_offers(skus_to_process)

        basket_total = offer_price
        for sku in skus_to_process:
            try:
                basket_total += self.prices[sku]
            except KeyError:
                return -1

        return basket_total

    def _apply_free_products(self, skus: str):
        offers_with_free_product = [
            offer for offer in self.offers 
            if isinstance(offer, FreeProductOffer)
        ]
        skus_after_processing = skus

        for offer_with_free_product in offers_with_free_product:
            skus_after_processing = offer_with_free_product.apply(skus_after_processing)

        
        return skus_after_processing

    def _apply_offers(self, skus: str) -> tuple[str, int]:
        offers_with_discount = [
            offer for offer in self.offers 
            if isinstance(offer, PriceOffer)
        ]
        total_offer_price = 0
        skus_after_processing = skus

        # Currently highest quantity offers benefit customer more, so prioritise those
        sorted_offers = sorted(
            offers_with_discount, 
            key=lambda x: x.quantity, 
            reverse=True
        )

        for offer in sorted_offers:
            count = skus_after_processing.count(offer.product)
            offer_price, count_to_remove = offer.apply(count)
            total_offer_price += offer_price

            skus_after_processing = skus_after_processing.replace(
                offer.product, "", count_to_remove
            )

        return skus_after_processing, total_offer_price


def load_offers() -> dict[str, Offer]:
    offers = static_prices.OFFERS
    parsed_offers = []

    for offer in offers:
        if free_product := offer.get("free_product"):
            parsed_offer = FreeProductOffer(
                product=offer["product"],
                quantity=offer["quantity"],
                free_product=free_product
            )
        else:
            parsed_offer = PriceOffer(
                product=offer["product"],
                quantity=offer["quantity"], 
                price=offer["price"],
            )

        parsed_offers.append(parsed_offer)

    return parsed_offers


