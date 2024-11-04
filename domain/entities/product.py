from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    star: float
    # review_count: int
    # sales_count: int
    price: int
    # ship_days: int
    # sales_amount: int