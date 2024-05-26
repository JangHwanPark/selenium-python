import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

urls = [
    "https://pages.coupang.com/p/81915",
    "https://pages.coupang.com/p/84845",
    "https://pages.coupang.com/p/84871",
    "https://pages.coupang.com/p/84872",
    "https://pages.coupang.com/p/84873",
    "https://pages.coupang.com/p/84874",
    "https://pages.coupang.com/p/84875",
]

# user-agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

brand_mapping = {
    "Apple": "Apple",
    "삼성": "Samsung"
}

category_mapping = {
    "아이폰 15": "iPhone 15",
    "아이폰 14": "iPhone 14",
    "아이패드": "iPad",
    "맥북": "MacBook",
}

# 제품 정보를 메모리에 저장하기 위한 리스트
product_list = []

for url in urls:
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    # lxml 파서를 사용해 BeautifulSoup 객체 생성
    soup = BeautifulSoup(res.text, "html.parser")

    # 클래스가 weblog, tab 인 div, li 태그를 모두 찾아옴
    products = soup.find_all("div", attrs={"class": re.compile("^weblog carousel-contents-grid__product-unit")})

    # 제품 정보를 리스트에 저장
    for product in products:
        product_text = product.text.strip()
        brand_name = "OtherBrand"  # 기본 브랜드 설정
        category_name = "OtherCategory"  # 기본 카테고리 설정

        # 브랜드를 식별
        for brand, brand_label in brand_mapping.items():
            if brand in product_text:
                brand_name = brand_label
                break

        # 카테고리를 식별
        for keyword, category in category_mapping.items():
            if keyword in product_text:
                category_name = category
                break

        # 정규 표현식을 사용하여 필요한 정보를 추출
        name_match = re.search(r'아이폰 \d+ (?:Pro )?Max?', product_text)
        color_match = re.search(r'(블랙|화이트|핑크|옐로|블루|그린|레드|퍼플|스타라이트|미드나이트|네츄럴티타늄|블루티타늄|블랙티타늄)', product_text)
        storage_match = re.search(r'\d+GB', product_text)
        discount_match = re.search(r'\d+%', product_text)
        price_match = re.findall(r'\d{1,3}(?:,\d{3})*원', product_text)
        availability_match = re.search(r'(일시품절|내일\(월\) 도착 보장)', product_text)
        reviews_match = re.search(r'\((\d+,?\d*)\)', product_text)

        # 각 요소를 추출하여 변수에 저장, 해당 요소가 없으면 "Unknown" 또는 기본값 설정
        # 제품 이름 추출
        name = name_match.group(0) if name_match else "Unknown"

        # 색상 추출
        color = color_match.group(0) if color_match else "Unknown"

        # 저장 용량 추출
        storage = storage_match.group(0) if storage_match else "0"

        # 할인율 추출
        discount = discount_match.group(0) if discount_match else "0"

        # 가격 추출
        price = price_match[0] if price_match else "Unknown"

        # 최종 가격 추출
        final_price = price_match[1] if len(price_match) > 1 else "Unknown"

        # 재고 상태 추출
        availability = availability_match.group(0) if availability_match else "100"

        # 리뷰 수 추출
        reviews = reviews_match.group(1) if reviews_match else "Unknown"

        # 리스트에 (brand_name, category_name, name, color, storage, discount, price, final_price, availability, reviews) 형태로 저장
        product_list.append([
            brand_name, category_name, name, color, storage, discount, price, final_price, availability, reviews
        ])

# DataFrame 생성
df = pd.DataFrame(
    product_list,
    columns=[
        "brand", "category", "name", "color", "storage", "discount", "price", "final_price","availability", "reviews"
    ]
)

df.to_excel("coupang/coupang_apple.xlsx", index=False)
print("저장 완료")