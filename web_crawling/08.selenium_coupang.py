import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 크롬 드라이버 경로 지정
driver_path = "../chromedriver/chromedriver.exe"

# Selenium 설정
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# 웹 드라이버 서비스 설정
service = Service(driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

# 크롤링할 페이지 URL
url = "https://www.coupang.com/np/campaigns/82/components/194176"

# 웹페이지 열기
driver.get(url)

# 페이지가 완전히 로드될 때까지 대기
time.sleep(5)

# 페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup을 사용해 웹페이지 파싱
soup = BeautifulSoup(page_source, "html.parser")

# 예시로 웹페이지 제목 출력
print(soup.title.string)

# 드라이버 종료
driver.quit()