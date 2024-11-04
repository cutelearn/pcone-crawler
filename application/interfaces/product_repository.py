from abc import ABC, abstractmethod
from typing import List
from domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_products(self, keyword: str, page: int = 1) -> List[Product]:
        pass