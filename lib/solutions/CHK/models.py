
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

class DiscountOffer(Offer):
    price: int

    def apply(self, skus: str) -> tuple[int, str]:
        number_of_offer_occurences = self.times_offer_can_be_applied(skus)

        offers_price = number_of_offer_occurences * self.price
        count_to_remove = (self.quantity * number_of_offer_occurences)

        skus_after_processing = skus.replace(self.product, "", count_to_remove)
        return offers_price, skus_after_processing

class FreeProductOffer(Offer):
    free_product: str

    def apply(self, skus: str) -> tuple[int, str]:
        skus_after_processing = skus

        return 0, skus_after_processing.replace(
            self.free_product, "", self.times_offer_can_be_applied(skus)
        )

class GroupDiscountOffer(Offer):
    price: int
    mutlibuy_with_products: list[str]

    @property
    def multibuy_group(self) -> list[str]:
        return self.mutlibuy_with_products + [self.product]

    def times_offer_can_be_applied(self, skus: str) -> int:
        match_count = 0
        for sku in skus:
            if sku in self.multibuy_group:
                match_count += 1

        return int(match_count / self.quantity)

    def apply(self, skus: str) -> tuple[int, str]:
        times_to_apply = self.times_offer_can_be_applied(skus)
        quantity_to_remove = self.times_offer_can_be_applied(skus) * self.quantity

        skus_after_processing = ""
        for index, sku in enumerate(skus):
            if quantity_to_remove <= 0:
                skus_after_processing += skus[index:]
                break

            if sku not in self.multibuy_group:
                skus_after_processing += sku
                continue

            quantity_to_remove -= 1

        
        return self.price * times_to_apply, skus_after_processing

class Basket(BaseModel):
    skus: str
    prices: dict[str, int]
    offers: list[Offer]

    def calculate_price(self):
        skus_to_process = self.skus

        skus_to_process = self._apply_free_products(skus_to_process)

        basket_total = 0

        offer_price, skus_to_process = self._apply_discounts_offers(skus_to_process)
        basket_total += offer_price

        offer_price, skus_to_process = self._apply_group_discount_offers(skus_to_process)
        basket_total += offer_price

        for sku in skus_to_process:
            try:
                basket_total += self.prices[sku]
            except KeyError:
                return -1

        return basket_total

    def _apply_group_discounts(self, skus: str) -> tuple[int, str]:
        return 0, skus

    def _apply_free_products(self, skus: str) -> str:
        offers_with_free_product = [
            offer for offer in self.offers 
            if isinstance(offer, FreeProductOffer)
        ]
        skus_after_processing = skus

        for offer_with_free_product in offers_with_free_product:
            _, skus_after_processing = offer_with_free_product.apply(skus_after_processing)

        
        return skus_after_processing

    def _apply_discounts_offers(self, skus: str) -> tuple[int, str]:
        offers_with_discount = [
            offer for offer in self.offers 
            if isinstance(offer, DiscountOffer)
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
            offer_price, skus_after_processing = offer.apply(skus_after_processing)
            total_offer_price += offer_price

        return total_offer_price, skus_after_processing

    def _apply_group_discount_offers(self, skus: str) -> tuple[int, str]:
        offers_with_group_discount = [
            offer for offer in self.offers 
            if isinstance(offer, GroupDiscountOffer)
        ]
        total_offer_price = 0
        skus_after_processing = skus

        for offer in offers_with_group_discount:
            offer_price, skus_after_processing = offer.apply(skus_after_processing)
            total_offer_price += offer_price
        
        return total_offer_price, skus_after_processing


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
        elif multibuy_with := offer.get("multibuy_with"):
            parsed_offer = GroupDiscountOffer(
                product=offer["product"],
                quantity=offer["quantity"],
                price=offer["price"],
                mutlibuy_with_products=multibuy_with
            )
        else:
            parsed_offer = DiscountOffer(
                product=offer["product"],
                quantity=offer["quantity"], 
                price=offer["price"],
            )

        parsed_offers.append(parsed_offer)

    return parsed_offers