from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    name: str
    shop_product_count: int
    shop_star: float
    shop_ship_days: float
    shop_reply_rate: float
    price: float
    discount: float
    star: float
    purchase_count: int
