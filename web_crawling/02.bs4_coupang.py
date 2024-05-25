# 1. 셀레니움을 사용해 웹페이지 로드
# 2. BeautifulSoup을 사용해 웹페이지 파싱
# 3. 판다스를 사용해 데이터프레임으로 변환

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# 크롬 드라이버 경로 지정
driver_path = "../chromedriver/chromedriver.exe"

# selenium 설정 및 웹페이지 로드
service = Service(driver_path)

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=service)
url = "https://pages.coupang.com/p/84871"
driver.get(url)

# 페이지가 완전히 로드 될 때 까지 대기
time.sleep(5)

# 페이지 소스 가져오기
page_source = driver.page_source
driver.quit()

# BeautifulSoup을 사용해 웹페이지 파싱
soup = BeautifulSoup(page_source, "html.parser")

# 맥북 정보 추출
products = soup.select("div.lazy-container")

product_list = []
for product in products:
    # 상품 제목, 가격 추출
    title_element = product.select_one("span.product-unit-info__title")
    price_element = product.select_one("del.discount-price__base-price")

    # 요소가 존재하는지 확인
    if title_element and price_element:
        title = title_element.get_text(strip=True)
        price = price_element.get_text(strip=True)
        product_list.append([title, price])
        print(title, price)

# pandas를 사용해 데이터프레임 생성 및 엑셀 파일로 저장
df = pd.DataFrame(product_list, columns=["상품명", "가격"])
df.to_excel("coupang/coupang_macbook.xlsx", index=False)
print("파일이 성공적으로 저장되었습니다.")