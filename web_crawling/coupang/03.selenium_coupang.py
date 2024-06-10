import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook

# product_code 를 dictionary 로 생성 (url 참조)
product_code = {
    'food': 194276, 'household_items': 115573, 'beauty': 176422, 'interior': 184455, 'electronics_digital': 178155, 'home_kitchen': 185569, 'maternity_baby': 221834, 'pet_supplies': 115574, 'toys': 317679, 'automotive': 183960, 'stationery_office': 177195, 'sports': 317678, 'books_music_movies': 317677, 'health_supplements': 305698, 'women_fashion': 186664, 'men_fashion': 186969, 'kids_baby_fashion': 213101, 'unisex_clothing': 502893
}

# 카테고리 리스트화 (코드로 수집 가능)
original_list = [
    "food", "household_items", "beauty", "electronics_digital", "home_kitchen",
    "maternity_baby", "pet_supplies", "toys", "automotive", "stationery_office", "sports",
    "books_music_movies", "health_supplements", "women_fashion", "men_fashion",
    "kids_baby_fashion", "unisex_clothing"
]

# product_code 를 활용해 카테고리별로 url_list 생성
url_list = []
for lis in original_list:
    key = product_code[lis]
    raw_url = f"https://www.coupang.com/np/categories/{key}?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page="
    url_list.append(raw_url)

# 크롬 셀레니움 옵션
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 크롬 설치 경로 설정
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("authority=" + "www.coupang.com")
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("accept-encoding=" + "gzip, deflate, br")
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
options.add_argument("sec-ch-ua-platform=" + "macOS")
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

# 모든 데이터를 저장할 리스트
all_product_data = []

# Selenium 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for name, main_url in zip(original_list, url_list):
    print("*" * 10 + " " + f"{name} 시작" + " " + "*" * 10)

    for i in range(1, 6):
        temp_url = main_url + f"{i}"
        driver.get(temp_url)
        time.sleep(20)
        print("*" * 10 + " " + str(i) + " Page start! " + "*" * 10)

        try:
            product_list_element = driver.find_element(By.ID, "productList")
            lis = product_list_element.find_elements(By.CLASS_NAME, "baby-product")

            for li in lis:
                try:
                    product_id = li.find_element(By.ID, "product-id").text
                    product_name = li.find_element(By.CLASS_NAME, "name").text
                    price = li.find_element(By.CLASS_NAME, "price-value").text
                    delivery = li.find_element(By.CLASS_NAME, "delivery").text
                    product_url = li.find_element(By.CLASS_NAME, "baby-product-link").get_attribute("href")
                    all_product_data.append([product_id, name, product_name, price, delivery, product_url])

                    print(f"Category: {name}")
                    print(f"Product: {product_name}")
                    print(f"Price: {price}")
                    print(f"Delivery: {delivery}")
                    print(f"URL: {product_url}")
                except Exception as e:
                    print(f"Error while extracting data: {e}")

        except NoSuchElementException as e:
            print(f"No such element exception: {e}")

        print("*" * 10 + " " + str(i) + " Page end! " + "*" * 10)

        # 각 페이지 사이에 1초 간격을 두기
        time.sleep(1)

    # 각 카테고리 사이에 5초 간격을 두기
    time.sleep(5)

# Workbook과 Worksheet 생성
wb = Workbook()
ws = wb.active
ws.title = "Coupang Products"
ws.append(["pid", "category", "name", "price", "arrival", "url"])

# 모든 데이터를 워크시트에 추가
for product_data in all_product_data:
    ws.append(product_data)

# 데이터 저장
wb.save("coupang_all_products.xlsx")
wb.close()
driver.quit()
print("*" * 5 + " " + "모든 데이터 수집을 마쳤습니다. 감사합니다. " + " " + "*" * 5)