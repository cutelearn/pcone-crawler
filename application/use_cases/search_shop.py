from typing import List
from domain.entities.shop import Shop
from application.interfaces.shop_repository import ShopRepository


class SearchShopUseCase:
    def __init__(self, shop_repository: ShopRepository):
        self.shop_repository = shop_repository

    def execute(self, keyword: str, page: int = 1) -> List[Shop]:
        return self.shop_repository.search(keyword, page)
