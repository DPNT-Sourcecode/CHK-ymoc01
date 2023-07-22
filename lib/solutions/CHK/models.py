

from collections import defaultdict
from typing import Optional
from pydantic import BaseModel

from solutions.CHK import static_prices

class FreeProductSideEffect(BaseModel):
    product: str

class Offer(BaseModel):
    product: str
    quantity: int
    price: int
    side_effect: Optional[FreeProductSideEffect] = None

    def apply(self, count: int) -> tuple[int, int]:
        number_of_offer_occurences = int(count / self.quantity)

        offers_price = number_of_offer_occurences * self.price
        count_after_offers = count - (self.quantity * int(count / self.quantity))

        return offers_price, count_after_offers
    
    def times_offer_can_be_applied(self, skus: str) -> int:
        count = skus.count(self.product)
        if count >= self.quantity:
            return int(count / self.quantity)
        return 0

class Basket(BaseModel):
    skus: str
    prices: dict[str, int]
    offers: list[Offer]

    def calculate_price(self):
        skus_to_process = self.skus

        skus_to_process = self._apply_free_products(skus_to_process)

        # product_counts = defaultdict(int)
        # for sku in self.skus:
        #     product_counts[sku] += 1

        # basket_total = 0
        # for product, count in product_counts.items():
        #     offer_adjusted_count = count

        #     offers_for_product = self.offers.get(product)
        #     if offers_for_product:
        #         offer_price, offer_adjusted_count, products_to_remove = self._apply_offers(offers_for_product, count)
        #         for product in products_to_remove:
        #             if product in self.skus:
        #                 basket_total -= self.prices[product]
        #         basket_total += offer_price

        #     try:
        #         product_price = self.prices[product]
        #     except KeyError:
        #         return -1
            
        #     basket_total += offer_adjusted_count * product_price

        # return basket_total


    def _apply_free_products(self, skus: str):
        offers_with_free_product = [offer for offer in self.offers if offer.side_effect is not None]

        products_to_remove = []
        for offer_with_free_product in offers_with_free_product:
            for _ in range(offer_with_free_product.times_offer_can_be_applied(skus)):
                products_to_remove.append(offer_with_free_product.side_effect.product)

        skus_after_processing = skus
        for product in products_to_remove:
            skus_after_processing = skus_after_processing.replace(product, "", 1)
        
        return skus_after_processing

    def _apply_offers(self, offers: list[Offer], count: int) -> tuple[int, int, list[str]]:
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


def load_offers() -> dict[str, Offer]:
    offers = static_prices.OFFERS
    parsed_offers = []

    for offer in offers:
        if free_product := offer.get("free_product"):
            side_effect = FreeProductSideEffect(product=free_product)
        else:
            side_effect = None

        parsed_offers.append(
            Offer(
                product=offer["product"],
                quantity=offer["quantity"], 
                price=offer["price"],
                side_effect=side_effect
            )
        )

    return parsed_offers




