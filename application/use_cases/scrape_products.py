from typing import List
from domain.entities.product import Product
from application.interfaces.product_repository import ProductRepository
from application.interfaces.csv_writer import CsvWriter
import urllib.parse

class ScrapeProductsUseCase:
    def __init__(self, product_repository: ProductRepository, csv_writer: CsvWriter):
        self.product_repository = product_repository
        self.csv_writer = csv_writer

    def execute(self, keyword: str, pages: int = 1, output_file: str = "products.csv") -> None:
        all_products: List[Product] = []
        # URL encode the keyword for proper handling of Chinese characters
        encoded_keyword = urllib.parse.quote(keyword)

        for page in range(1, pages + 1):
            # PCone specific URL format
            products = self.product_repository.get_products(
                encoded_keyword,
                page
            )
            all_products.extend(products)

        self.csv_writer.write_products(all_products, output_file)