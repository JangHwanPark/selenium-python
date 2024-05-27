import re
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 가져올거
# 번호, 게시글, 카테고리, 유저이름(user01, 02..), 등록일, 조회수, 추천수

# 페이지 URL
base_url = "https://www.inven.co.kr/board/maple/2304"


def scrape_page(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(page_url, headers=headers)
    data = []

    if response.status_code != 200:
        print(f"문제가 발생했습니다. [에러코드 {response.status_code}]")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("tr", attrs={"class": re.compile("^lgtm")})
    user_count = 1

    for post in posts:
        # 추출할 데이터 정의
        number = post.find("td", class_="num").get_text(strip=True)
        category = post.find("span", class_="category").get_text(strip=True)

        # 제목 추출
        # 제목 추출: <a> 태그에서 카테고리 제외
        title_tag = post.find("a", class_="subject-link")

        # 카테고리 span이 존재하는지 확인
        if title_tag.find("span", class_="category"):
            # 카테고리 제거
            title_tag.find("span", class_="category").decompose()
        title = title_tag.get_text(strip=True)

        # 유저 이름 생성
        user = f"user{user_count:02d}"
        user_count += 1

        date = post.find("td", class_="date").get_text(strip=True)
        views = post.find("td", class_="view").get_text(strip=True)
        recommends = post.find("td", class_="reco").get_text(strip=True)

        # 게시글 링크를 동적으로 생성
        post_link = f"{base_url}/{number}"
        post_response = requests.get(post_link)
        post_soup = BeautifulSoup(post_response.text, "html.parser")

        # 게시글 본문 내용 추출
        post_content = post_soup.find("div", class_="contentBody").get_text(strip=True)  # 본문 클래스 이름은 확인 필요

        print(f"{number}, {category}, {title}, {user}, {date}, {views}, {recommends}, {post_content}")

        # 수집된 데이터를 리스트에 추가
        data.append([number, category, title, user, date, views, recommends, post_content])
    return data


for page in range(1, 2):
    page_url = f"{base_url}?p={page}"
    scrape_page(page_url)

# 모든 페이지에 대한 데이터 수집
all_data = []
for page in range(1, 11):
    page_url = f"{base_url}?p={page}"
    page_data = scrape_page(page_url)
    all_data.extend(page_data)

if all_data:
    df = pd.DataFrame(all_data, columns=['번호', '카테고리', '제목', '사용자', '등록일', '조회수', '추천수', '본문 내용'])
    df.to_excel('scraped_data.xlsx', index=False, engine='openpyxl')
    print("데이터 크롤링 및 엑셀 저장 완료")
else:
    print("수집된 데이터가 없습니다.")