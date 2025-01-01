from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List, Tuple
from domain.entities.product import Product
from domain.entities.shop import Shop
from application.interfaces.product_repository import ProductRepository
from utils.dely import random_delay


class WebProductRepository(ProductRepository):
    def _parse_shop_details(self, soup: BeautifulSoup) -> Tuple[int, float, float, float]:
        """解析商店詳細資訊"""
        details_div = soup.find('div', class_='details')
        if not details_div:
            return 0, 0.0, 0.0, 0.0

        details = details_div.find_all('div', class_='detail')
        shop_product_count = int(details[0].find('div', class_='count').text)
        shop_star = float(details[1].find('div', class_='count').text)
        shop_ship_days = float(details[2].find('div', class_='count').text)
        shop_reply_rate = float(details[3].find(
            'div', class_='count').text.replace('%', '')) / 100

        return shop_product_count, shop_star, shop_ship_days, shop_reply_rate

    def _parse_price_info(self, soup: BeautifulSoup) -> Tuple[float, float]:
        """解析價格和折扣資訊"""
        primary_div = soup.find('div', class_='primary')
        if not primary_div:
            return 1.0, 0

        discount = 1.0
        discount_tag = primary_div.find('div', class_='tag circle')
        if discount_tag:
            discount = float(discount_tag.text.replace('折', '')) / 100

        price = 0
        price_span = primary_div.find('span', class_='display-price')
        if price_span:
            price = float(price_span.text.replace('$', ''))

        return discount, price

    def _parse_review_star(self, soup: BeautifulSoup) -> float:
        """解析評價星數"""
        review_div = soup.find('div', class_='review-info')
        if not review_div:
            return 0.0

        review_element = review_div.find('div', class_='review')
        return float(review_element.contents[0]) if review_element else 0.0

    def _parse_product_name(self, soup: BeautifulSoup) -> str:
        """解析商品名稱"""
        name_element = soup.find('h1', class_='name')
        return name_element.text.strip() if name_element else ""

    def _parse_purchase_count(self, soup: BeautifulSoup) -> int:
        """解析購買人數"""
        review_div = soup.find('div', class_='review-info')
        if not review_div:
            return 0

        # 找到包含購買人數的 div
        purchase_div = review_div.find_all('div')[1]  # 第二個 div 包含購買人數
        if purchase_div:
            # 提取數字部分
            purchase_text = purchase_div.text.strip()
            purchase_count = ''.join(filter(str.isdigit, purchase_text))
            return int(purchase_count) if purchase_count else 0
        return 0

    def search(self, shops: List[Shop]) -> List[Product]:
        products = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444',
            options=chrome_options
        )
        try:
            for shop in shops:
                driver.get(shop.url)
                print(f"正在訪問 {shop.name} 的商品頁面")
                random_delay()

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                product_name = self._parse_product_name(soup)
                shop_product_count, shop_star, shop_ship_days, shop_reply_rate = self._parse_shop_details(
                    soup)
                discount, price = self._parse_price_info(soup)
                star = self._parse_review_star(soup)
                purchase_count = self._parse_purchase_count(soup)

                product = Product(
                    name=product_name,
                    shop_product_count=shop_product_count,
                    shop_star=shop_star,
                    shop_ship_days=shop_ship_days,
                    shop_reply_rate=shop_reply_rate,
                    price=price,
                    discount=discount,
                    star=star,
                    purchase_count=purchase_count
                )
                products.append(product)

        except Exception as e:
            print(f"發生錯誤: {str(e)}")
            print(f"錯誤位置: ", e.__traceback__.tb_lineno)
            raise

        finally:
            driver.quit()

        return products
