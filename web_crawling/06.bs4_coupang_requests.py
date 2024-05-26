import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# 탐색할 url
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

for url in urls:
    print(url)

    # url 에 get 요청 보내고 응답 코드 반환
    response = requests.get(url, headers)

    # 상태 코드
    print(f"Response Status Code: {response.status_code}")

    # 응답 헤더
    print(f"Response Header: {response.headers}")

    # 응답 본문 - 처음 10자를 출력하여 확인
    print(f"Response Body(String): {response.text[:10]}")

    # 응답 본문 - 처음 10바이트를 출력하여 확인
    print(f"Response Body(Byte): {response.content[:10]}")

    # JSON 응답
    if response.headers.get('Content-Type') == 'application/json; charset=utf-8':
        print(f"JSON: {response.json()}")

    # 최종 URL (리다이렉션된 경우)
    print(f"Final URL: {response.url}")

    # 리다이렉션 이력
    print(f"History: {response.history}")

    # 쿠키
    print(f"Cookies: {response.cookies}")

    # 경과 시간
    print(f"Elapsed Time: {response.elapsed}")

    # 인코딩
    print(f"Encoding: {response.encoding}")

# 응답이 성공 상태인지 확인
try:
    response.raise_for_status()
    print("Request was successful.")
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")