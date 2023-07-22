

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
    offers: dict[str, list[Offer]]

    def calculate_price(self):
        skus_to_process = self.skus
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


    def _apply_free_products(self):
        ...

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



