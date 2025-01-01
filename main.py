from infrastructure.repositories.web_shop_repository import WebShopRepository
from infrastructure.repositories.web_product_repository import WebProductRepository
from infrastructure.exporters.csv_exporter import CsvExporter
from application.use_cases.search_shop import SearchShopUseCase
from application.use_cases.search_products import SearchProductsUseCase


def main():
    try:
        # 創建依賴
        shop_repository = WebShopRepository()
        product_repository = WebProductRepository()
        csv_writer = CsvExporter()

        # 創建用例
        search_shop_use_case = SearchShopUseCase(shop_repository)
        search_products_use_case = SearchProductsUseCase(product_repository)

        # 取得使用者輸入的搜尋關鍵字
        keyword = input("請輸入要搜尋的商品關鍵字：")

        # 執行爬蟲並導出CSV
        print("正在連接到 WebDriver 服務...")
        shops = search_shop_use_case.execute(keyword=keyword, page=8)
        print("已取得商店資料")
        print("正在取得商品資料...")
        products = search_products_use_case.execute(shops)
        csv_writer.write_products(products, "products.csv")
        print("已取得商品資料")

    except ConnectionError:
        print("錯誤：無法連接到 WebDriver 服務。請確保 Selenium 服務器已啟動。")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
    finally:
        print("程式結束")


if __name__ == "__main__":
    main()
