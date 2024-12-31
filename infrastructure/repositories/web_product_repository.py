from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List
from domain.entities.product import Product
from application.interfaces.product_repository import ProductRepository


class WebProductRepository(ProductRepository):
    BASE_URL = "https://www.pcone.com.tw/search"

    def get_products(self, keyword: str, page: int = 1) -> List[Product]:
        products = []

        # 設定 Chrome 選項
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # 連接到遠端 Selenium Server
        driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444',
            options=chrome_options
        )
        try:
            # 構建 URL
            url = f"{self.BASE_URL}?page={page}&q={keyword}"
            driver.get(url)

            # 使用 BeautifulSoup 解析頁面
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # 解析產品資訊
            product_items = soup.find_all('div', class_='search-item')

            for item in product_items:
                product = Product(
                    name=item.find('div', class_='product-name').text.strip(),
                    star=item.find('span', class_='review-avg').text.strip(
                    ) if item.find('span', class_='review-avg') else "0",
                    price=item.find('span', class_='price').text.strip()
                )
                products.append(product)

        except Exception as e:
            print(f"發生錯誤: {str(e)}")
            raise

        finally:
            driver.quit()

        return products
