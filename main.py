from infrastructure.repositories.web_product_repository import WebProductRepository
from infrastructure.exporters.csv_exporter import CsvExporter
from application.use_cases.scrape_products import ScrapeProductsUseCase

def main():
    # 創建依賴
    product_repository = WebProductRepository()
    csv_writer = CsvExporter()

    # 創建用例
    use_case = ScrapeProductsUseCase(product_repository, csv_writer)

    # 取得使用者輸入的搜尋關鍵字
    keyword = input("請輸入要搜尋的商品關鍵字：")

    # 執行爬蟲並導出CSV
    use_case.execute(keyword=keyword, pages=1, output_file="products.csv")

if __name__ == "__main__":
    main()