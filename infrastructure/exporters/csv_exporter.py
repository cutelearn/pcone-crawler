import csv
from typing import List
from domain.entities.product import Product
from domain.entities.shop import Shop
from application.interfaces.csv_writer import CsvWriter


class CsvExporter(CsvWriter):
    def write_products(self, products: List[Product], filename: str) -> None:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['商品名稱', '店家商品數量', '店家評價', '店家出貨天數',
                            '店家回覆率', '特價', '折數', '商品評分'])

            for product in products:
                writer.writerow([
                    product.name,
                    product.shop_product_count,
                    product.shop_star,
                    product.shop_ship_days,
                    product.shop_reply_rate,
                    product.price,
                    product.discount,
                    product.star
                ])

    def write_shops(self, shops: List[Shop], filename: str) -> None:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['商店名稱', '商店URL'])

            for shop in shops:
                writer.writerow([shop.name, shop.url])
