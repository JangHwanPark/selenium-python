import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy.exc import SQLAlchemyError
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# 제품 코드 딕셔너리 생성
product_code = {
    'food': 194276
}
# , 'household_items': 115573, 'beauty': 176422, 'interior': 184455, 'electronics_digital': 178155,
#     'home_kitchen': 185569, 'maternity_baby': 221834

# 카테고리 리스트화
original_list = [
    "food"
]
# , "household_items", "beauty", "electronics_digital", "home_kitchen", "maternity_baby"

# product_code를 활용해 카테고리별로 url_list 생성
url_list = []
for lis in original_list:
    key = product_code[lis]
    raw_url = f"https://www.coupang.com/np/categories/{key}?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page="
    url_list.append(raw_url)

# 크롬 셀레니움 옵션
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 크롬 설치 경로 설정
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")

df = pd.DataFrame()

while True:
    print("\n" + "=" * 10 + " " + "메뉴" + " " + "=" * 10)
    print("1. 데이터 수집")
    print("2. 데이터 분석")
    print("3. 데이터베이스 저장")
    print("4. 종료")
    print("=" * 30)
    user_input = int(input("원하는 작업을 선택하세요.\nuser >> "))

    # 데이터 수집
    if user_input == 1:
        print("데이터 수집 형식을 선택하세요.")
        print("1. CSV")
        print("2. JSON")
        print("3. XLSX")
        format_choice = int(input("user >> "))

        all_product_data = []

        # Selenium 드라이버 초기화
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for name, main_url in zip(original_list, url_list):
            print("*" * 10 + " " + f"{name} 시작" + " " + "*" * 10)

            for i in range(1, 2):
                temp_url = main_url + f"{i}"
                driver.get(temp_url)
                time.sleep(5)
                print("*" * 10 + " " + str(i) + " Page start! " + "*" * 10)

                try:
                    product_list_element = driver.find_element(By.ID, "productList")
                    lis = product_list_element.find_elements(By.CLASS_NAME, "baby-product")

                    for li in lis:
                        try:
                            product_id = li.get_attribute("data-product-id")
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

        # 데이터프레임으로 변환
        columns = ["Product ID", "Category", "Product Name", "Price", "Delivery", "Product URL"]
        df = pd.DataFrame(all_product_data, columns=columns)

        # 데이터 저장
        save_path = "./data/coupang_products"
        if format_choice == 1:
            df.to_csv(f"{save_path}.csv", index=False)
            print(f"데이터가 {save_path}.csv 에 저장되었습니다.")
        elif format_choice == 2:
            df.to_json(f"{save_path}.json", orient="records", force_ascii=False)
            print(f"데이터가 {save_path}.json 에 저장되었습니다.")
        elif format_choice == 3:
            df.to_excel(f"{save_path}.xlsx", index=False)
            print(f"데이터가 {save_path}.xlsx 에 저장되었습니다.")
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")
        driver.quit()

    # 데이터 분석
    elif user_input == 2:
        if not df.empty:
            # 넘파이 배열로 변환
            np_data = df.to_numpy()
            print("\n데이터 분석 결과")
            print(f"데이터의 전체 개수: {np_data.size}")
            print(f"데이터의 차원: {np_data.shape}")

            # 수치 분석
            if 'Price' in df.columns:
                df['Price'] = df['Price'].str.replace(',', '').str.replace('원', '').astype(float)

                Q1 = df['Price'].quantile(0.25)
                Q3 = df['Price'].quantile(0.75)
                IQR = Q3 - Q1
                df = df[~((df['Price'] < (Q1 - 1.5 * IQR)) | (df['Price'] > (Q3 + 1.5 * IQR)))]

                # 로그 변환
                df['Price'] = np.log1p(df['Price'])

                price_data = df['Price'].to_numpy()
                print(f"평균 가격: {np.mean(price_data)}")
                print(f"최대 가격: {np.max(price_data)}")
                print(f"최소 가격: {np.min(price_data)}")

                # 시각화
                plt.figure(figsize=(10, 6))
                sns.histplot(price_data, kde=True)
                plt.title("Price Distribution")
                plt.xlabel("Price")
                plt.ylabel("Frequency")
                plt.show()

                plt.figure(figsize=(10, 6))
                sns.boxplot(x=price_data)
                plt.title("Price Boxplot")
                plt.xlabel("Price")
                plt.show()
            else:
                print("수치형 데이터가 포함된 컬럼이 없습니다.")
        else:
            print("분석할 데이터가 없습니다. 먼저 데이터를 수집하세요.")

    # 데이터베이스 저장
    elif user_input == 3:
        if df is not None and not df.empty:
            try:
                # 데이터베이스 정보 입력 받기
                db_user = input("데이터베이스 사용자 이름을 입력하세요.\nuser >> ")
                db_password = input("데이터베이스 비밀번호를 입력하세요.\nuser >> ")
                db_host = input("데이터베이스 호스트를 입력하세요.\nuser >> ")
                db_port = input("데이터베이스 포트를 입력하세요.\nuser >> ")
                db_name = input("데이터베이스 이름을 입력하세요.\nuser >> ")

                # 데이터베이스 URL 생성
                db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
                engine = create_engine(db_url)
                df.to_sql('coupang_products', con=engine, if_exists='replace', index=False)
                print("데이터가 데이터베이스에 저장되었습니다.")
            except SQLAlchemyError as e:
                print(f"데이터베이스 저장 중 오류 발생: {e}")
        else:
            print("저장할 데이터가 없습니다. 먼저 데이터를 수집하세요.")

    # 종료
    elif user_input == 4:
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 입력입니다. 다시 선택하세요.")