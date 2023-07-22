

from typing import Optional
from pydantic import BaseModel

class FreeProductSideEffect(BaseModel):
    product: str

class Offer(BaseModel):
    quantity: int
    price: int
    side_effect: Optional[FreeProductSideEffect] = None


