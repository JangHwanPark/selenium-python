import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import os

# product_code 를 dictionary 로 생성 (url 참조)
product_code = {
    'food': 194276, 'household_items': 115673, 'beauty': 176522, 'interior': 184555, 'electronics_digital': 178155,
    'home_kitchen': 185669, 'maternity_baby': 221934, 'pet_supplies': 115674, 'toys': 317779, 'automotive': 183960,
    'stationery_office': 177295, 'sports': 317778, 'books_music_movies': 317777, 'health_supplements': 305798,
    'women_fashion': 186764, 'men_fashion': 187069, 'kids_baby_fashion': 508566, 'unisex_clothing': 502993
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
    print(f"key: {key}")

    raw_url = f"https://www.coupang.com/np/categories/{key}?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page="
    # raw_url = f"https://www.coupang.com/np/categories/{key}"
    url_list.append(raw_url)

# 크롬 셀레니움 옵션
options = webdriver.ChromeOptions()
# options.add_argument("--headless")

# 크롬 실행 파일의 경로를 지정합니다. 이 경로는 크롬 브라우저가 설치된 위치를 가리킵니다.
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# 웹사이트가 자동화된 크롬을 일반 사용자의 브라우저로 인식하지 못하게 합니다.
options.add_argument("--disable-blink-features=AutomationControlled")

# 브라우저 상단에 "자동화된 소프트웨어에 의해 제어됩니다"라는 정보바를 비활성화합니다.
options.add_argument("--disable-infobars")

# 자동화 탐지를 피하기 위한 크롬 드라이버의 일부 기능을 비활성화합니다.
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# HTTP 요청에 사용될 기본 헤더를 설정합니다.
options.add_argument("authority=" + "www.coupang.com")  # 요청을 보낼 권한을 가진 호스트를 지정합니다.
options.add_argument("method=" + "GET")  # 사용할 HTTP 메소드를 GET으로 지정합니다.
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")  # 서버로부터 어떤 타입의 데이터를 받을 수 있는지 지정합니다.
options.add_argument("accept-encoding=" + "gzip, deflate, br")  # 서버로부터 받을 수 있는 인코딩 타입을 지정합니다.
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")  # 브라우저의 유저 에이전트를 지정합니다.
options.add_argument("sec-ch-ua-platform=" + "macOS")  # 사용자의 운영체제 정보를 제공합니다.
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")  # 사이트에 사용할 쿠키를 설정합니다.


# 모든 데이터를 저장할 리스트
all_product_data = []

# Selenium 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 이미지 저장 경로 설정
image_save_path = "coupang_img"
if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)

# 크롤링 메인 로직
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
            # print(f"lis: {lis}")

            for li in lis:
                try:
                    # pid 추출
                    product_link = li.find_element(By.CLASS_NAME, "baby-product-link")
                    product_url = product_link.get_attribute("href")
                    product_id = product_link.get_attribute("data-product-id")

                    # 제품 데이터 추출
                    product_name = li.find_element(By.CLASS_NAME, "name").text
                    discount = li.find_element(By.CLASS_NAME, "discount-percentage").text
                    base_price = li.find_element(By.CLASS_NAME, "base-price").text
                    price = li.find_element(By.CLASS_NAME, "price-value").text
                    unit_price = li.find_element(By.CLASS_NAME, "unit-price").text
                    delivery = li.find_element(By.CLASS_NAME, "delivery").text
                    rating = li.find_element(By.CLASS_NAME, "rating-total-count").text
                    reward = li.find_element(By.CLASS_NAME, "reward-cash-txt").text
                    # product_url = li.find_element(By.CLASS_NAME, "baby-product-link").get_attribute("href")

                    # 이미지 URL 추출 및 다운로드
                    # 이미지 URL 추출 및 다운로드
                    image_element = li.find_element(By.CLASS_NAME, "baby-product-wrap").find_element(By.TAG_NAME, "img")
                    image_url = image_element.get_attribute("src")
                    image_filename = os.path.join(image_save_path, f"{product_id}.jpg")
                    image_response = requests.get(image_url)
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_response.content)
                        
                    # 리스트에 데이터 삽입
                    all_product_data.append([product_id, name, product_name, base_price, price, unit_price, delivery,
                                             rating, reward, image_filename])

                    print(f"product_id: {product_id}")
                    print(f"Category: {name}")
                    print(f"Category: {product_name}")
                    print(f"base_price: {base_price}")
                    print(f"Price: {price}")
                    print(f"unit_price: {unit_price}")
                    print(f"Delivery: {delivery}")
                    print(f"rating: {rating}")
                    print(f"reward: {reward}")
                    print(f"Image: {image_filename}")
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
ws.append(["pid", "category", "name", "base_price", "price", "unit_price", "arrival", "rating", "reward", "url"])

# 모든 데이터를 워크시트에 추가
for product_data in all_product_data:
    ws.append(product_data)

# 데이터 저장
wb.save("coupang_all_products.xlsx")
wb.close()
driver.quit()
print("*" * 5 + " " + "모든 데이터 수집을 마쳤습니다. 감사합니다. " + " " + "*" * 5)