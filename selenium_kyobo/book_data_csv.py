import requests
import os
import os.path
import time
import pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# 이미지 다운로드 함수
def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)


product_code = {
    'Computer Science': 3301,
    'Software Engineering': 330113,
    'Information Communication Engineering': 330115,
    'Computer Architecture': 330117,
    'Operating System Theory': 330123,
    'Data and Algorithm': 330127,
    'AI': 330143
}

category_list = [
    'Computer Science', 'Software Engineering',
    'Information Communication Engineering', 'Computer Architecture',
    'Operating System Theory', 'Data and Algorithm', 'AI'
]

url_list = []

books_data = []

for category in category_list:
    key = product_code[category]
    # print(f'key: {key}')

    for page in range(1, 51):
        raw_url = f"https://product.kyobobook.co.kr/category/KOR/{key}#?page={page}&type=all&sort=new"
        url_list.append(raw_url)
        # print(f'raw_url: {raw_url}')

# print(f'url_list: {url_list}')

options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("authority=" + "www.kyobobook.co.kr")
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
# https://product.kyobobook.co.kr/category/KOR/3301#?page=1&type=all&sort=new1

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 이미지 처리
image_save_path = 'kyobo_img'
if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)

img_cnt = 1

for page_title, main_url in zip(category_list, url_list):
    print("*" * 10 + " " + f"{page_title} 시작" + " " + "*" * 10)
    # print(f'main url = {main_url}')

    for i in range(1, 6):
        # temp_url = main_url + f"{i}"
        driver.get(main_url)
        time.sleep(10)
        print("*" * 10 + " " + str(i) + " Page start! " + "*" * 10)

        book_list_element = driver.find_elements(By.CLASS_NAME, 'prod_item')
        for li in book_list_element:
            try:
                # 이미지 url, 제목, 출판사, 출판일, 가격, 적립 포인트, 소개, 별점, 출고 날짜
                book_name = li.find_element(By.CLASS_NAME, "prod_name").text

                # 책 저자 추출
                author_element = li.find_element(By.CSS_SELECTOR, '.prod_author a')
                book_author = author_element.text.strip() if author_element else '저자 정보 없음'

                # 출판사 이름 추출 (CSS_SELECTOR)
                author_info = li.find_element(By.CSS_SELECTOR, '.prod_author').text
                book_publisher = author_info.split(' ')[-1] if author_info else '출판사 정보 없음'

                book_date = li.find_element(By.CLASS_NAME, "date").text

                # 할인 정보
                book_discount_elements = li.find_elements(By.CLASS_NAME, 'percent')
                if book_discount_elements:
                    book_discount = book_discount_elements[0].text.strip()
                else:
                    book_discount = '할인 정보 없음'

                book_price = li.find_element(By.CLASS_NAME, 'price').text
                book_price_normal = li.find_element(By.CLASS_NAME, 'price_normal').text
                book_point = li.find_element(By.CLASS_NAME, 'point').text
                book_description = li.find_element(By.CLASS_NAME, 'prod_introduction').text

                book_review = li.find_element(By.CLASS_NAME, 'review_klover_text').text

                # 이미지 처리
                book_img_url = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
                formatted_number = f"{img_cnt:03d}"
                image_filename = f"book_img_{formatted_number}.jpg"
                image_path = os.path.join(image_save_path, image_filename)
                download_image(book_img_url, image_path)

                books_data.append([
                    img_cnt,
                    book_name,
                    page_title,
                    book_author,
                    book_publisher,
                    book_discount,
                    book_price,
                    book_price_normal,
                    book_point,
                    book_description,
                    book_review,
                    f'kyobo/{image_filename}'
                ])

                print(books_data)
                img_cnt += 1
                time.sleep(1)
            except NoSuchElementException:
                book_discount = '할인 정보 없음'

    time.sleep(5)

# Save Data
df = pandas.DataFrame(books_data, columns=[
    'book_id',
    'name',
    'category',
    'author',
    'publisher',
    'discount',
    'price',
    'price_normal',
    'point',
    'description',
    'review',
    'img'
])
df.to_csv('csv_data/books.csv', index=False)