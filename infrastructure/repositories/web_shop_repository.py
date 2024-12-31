from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List
from domain.entities.shop import Shop
from application.interfaces.shop_repository import ShopRepository
from utils.dely import random_delay


class WebShopRepository(ShopRepository):
    BASE_URL = "https://www.pcone.com.tw/search"

    def search(self, keyword: str, page: int = 1) -> List[Shop]:
        shops = []
        current_page = 1
        max_page = page

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
            while current_page <= max_page:
                # 構建 URL
                url = f"{self.BASE_URL}?page={current_page}&q={keyword}"
                driver.get(url)
                print(f"正在訪問第 {current_page} 頁")
                random_delay()
                # 使用 BeautifulSoup 解析頁面
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # 解析商店資訊
                shop_items = soup.find_all('div', class_='search-item')

                # 如果沒有找到商品，表示已經到最後一頁
                if not shop_items:
                    break

                for item in shop_items:
                    product_info = item.find('div', class_='product-info')
                    if product_info:
                        name = product_info.find(
                            'div', class_='product-name').text.strip()
                        url = item.find('a').get('href')
                        shop = Shop(
                            name=name,
                            url=url
                        )
                        shops.append(shop)

                current_page += 1

        except Exception as e:
            print(f"發生錯誤: {str(e)}")
            raise

        finally:
            driver.quit()

        return shops
