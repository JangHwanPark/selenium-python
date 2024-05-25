from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
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
urls = [
    "https://pages.coupang.com/p/81915",
    "https://pages.coupang.com/p/84845",
    "https://pages.coupang.com/p/84871",
    "https://pages.coupang.com/p/84872",
    "https://pages.coupang.com/p/84873",
    "https://pages.coupang.com/p/84874",
    "https://pages.coupang.com/p/84883",
    "https://pages.coupang.com/p/84875"
]

# 모든 제품 정보를 저장할 리스트
all_product_list = []

# 이미지 저장 폴더
img_folder = "coupang/images"
os.makedirs(img_folder, exist_ok=True)

# 페이지별로 크롤링
for url in urls:
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 대기
    time.sleep(5)

    # 페이지 소스 가져오기
    page_source = driver.page_source

    # BeautifulSoup을 사용해 웹페이지 파싱
    soup = BeautifulSoup(page_source, "html.parser")

    # 상품별 상세 페이지 크롤링
    product_containers = soup.select("div.weblog")
    for container in product_containers:
        # 일시품절 텍스트 확인
        sold_out = container.find("span", string="일시품절")
        if sold_out:
            print("Skipping sold-out product")
            continue

        # 상품 링크 수집
        link = container.find("a", href=True)
        if link and 'href' in link.attrs:
            product_url = link['href']
            if not product_url.startswith("http"):
                product_url = "https://www.coupang.com" + product_url  # 상대 URL을 절대 URL로 변환
            print(f"Accessing product URL: {product_url}")

            try:
                driver.get(product_url)

                # 페이지가 완전히 로드될 때까지 대기
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h2.prod-buy-header__title"))
                )

                product_page_source = driver.page_source
                product_soup = BeautifulSoup(product_page_source, "html.parser")

                # 상품 상세 페이지에서 데이터 추출 (Ex. 상품명, 가격, 이미지)
                title_el = product_soup.select_one("h2.prod-buy-header__title")
                price_el = product_soup.select_one("span.total-price > strong")
                img_el = product_soup.select_one("img.prod-image__detail")

                # Null Check
                if title_el and price_el and img_el:
                    title = title_el.get_text(strip=True)
                    price = price_el.get_text(strip=True)
                    img_url = img_el['src']

                    # 스킴(프로토콜) 추가
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url

                    # 이미지 다운로드
                    img_data = requests.get(img_url).content
                    with open(f"{img_folder}/{title}.jpg", "wb") as f:
                        f.write(img_data)

                    all_product_list.append([title, price, img_url])
                    print(f"data: {title}, {price}, {img_url}")
                else:
                    print(f"Product information is missing, returning to the previous page: {product_url}")
                    driver.back()  # 이전 페이지로 돌아감
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.weblog.carousel-contents-grid__product-unit"))
                    )
                    time.sleep(2)  # 페이지 로드 대기
            except TimeoutException:
                print(f"Failed to load the product page: {product_url}")
                driver.back()  # 이전 페이지로 돌아감
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.weblog.carousel-contents-grid__product-unit"))
                )
                time.sleep(2)  # 페이지 로드 대기
            except WebDriverException as e:
                print(f"WebDriverException occurred: {e}")
                driver.back()  # 이전 페이지로 돌아감
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.weblog.carousel-contents-grid__product-unit"))
                )
                time.sleep(2)  # 페이지 로드 대기

# 브라우저 종료
driver.quit()

# pandas를 사용해 데이터프레임 생성 및 엑셀 파일로 저장
df = pd.DataFrame(all_product_list, columns=["product_name", "price", "image_path"])
df.to_excel("coupang/coupang_apple.xlsx", index=False)
print("파일이 성공적으로 저장되었습니다.")