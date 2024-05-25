from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import time

# 크롬 드라이버 경로 지정
driver_path = "../chromedriver/chromedriver.exe"

# selenium 설정 및 웹페이지 로드
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 크롤링할 페이지 URL
url_list = [
    "https://pages.coupang.com/p/84871",
    "https://pages.coupang.com/p/84845"
]

# 모든 제품 정보를 저장할 리스트
all_product_list = []

# 이미지 저장 폴더
img_folder = "coupang/images"
os.makedirs(img_folder, exist_ok=True)

for url in url_list:
    driver.get(url)

    # 페이지가 완전히 로드 될 때 까지 대기
    time.sleep(5)

    # 페이지 소스 가져오기
    page_source = driver.page_source

    # BeautifulSoup을 사용해 웹페이지 파싱
    soup = BeautifulSoup(page_source, "html.parser")

    # 상품 정보 추출
    products = soup.select("div.lazy-container")

    for product in products:
        title_element = product.select_one("span.product-unit-info__title")
        price_element = product.select_one("div.current-price__price")
        image_div = product.select_one("div.container.pre-defined-ratio")
        image_element = image_div.select_one("img") if image_div else None

        # 요소가 존재하는지 확인
        if title_element and price_element and image_element:
            title = title_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            image_url = image_element['src']  # 이미지 URL 추출

            # 스킴(프로토콜) 추가
            if image_url.startswith("//"):
                image_url = "https:" + image_url

            # 이미지 다운로드
            image_response = requests.get(image_url)
            image_name = os.path.join(img_folder, f"{title}.jpg")
            with open(image_name, 'wb') as file:
                file.write(image_response.content)

            all_product_list.append([title, price, image_name])
            print(title, price, image_name)

# 브라우저 종료
driver.quit()

# pandas를 사용해 데이터프레임 생성 및 엑셀 파일로 저장
df = pd.DataFrame(all_product_list, columns=["product_name", "price", "image_path"])
df.to_excel("coupang/coupang_products.xlsx", index=False)
print("파일이 성공적으로 저장되었습니다.")