import csv
from typing import List
from domain.entities.product import Product
from application.interfaces.csv_writer import CsvWriter

class CsvExporter(CsvWriter):
    def write_products(self, products: List[Product], filename: str) -> None:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # # writer.writerow(['商品名稱', '商品星數', '商品評價人數', '銷售數量', '商品價格', '商品出貨天數','銷售金額'])
            writer.writerow(['商品名稱', '商品星數', '商品價格'])

            for product in products:
                writer.writerow([
                    product.name,
                    product.star,
                    # product.review_count,
                    # product.sales_count,
                    product.price,
                    # product.ship_days,
                    # product.sales_amount
                ])