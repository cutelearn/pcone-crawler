from abc import ABC, abstractmethod
from typing import List
from domain.entities.product import Product

class CsvWriter(ABC):
    @abstractmethod
    def write_products(self, products: List[Product], filename: str) -> None:
        pass