from abc import ABC, abstractmethod
from typing import List
from domain.entities.shop import Shop


class ShopRepository(ABC):
    @abstractmethod
    def search(self, keyword: str, page: int = 1) -> List[Shop]:
        pass
