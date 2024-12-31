from typing import List
from domain.entities.product import Product
from domain.entities.shop import Shop
from application.interfaces.product_repository import ProductRepository


class SearchProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, shop: Shop) -> List[Product]:
        return self.product_repository.search(shop)
