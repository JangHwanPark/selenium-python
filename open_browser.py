from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# 크롬 드라이버 경로 지정
driver_path = "chromedriver/chromedriver.exe"

# 서비스 객체 생성 (chromedriver 실행 경로 지정)
service = Service(driver_path)

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=service)

# 구글 웹사이트 열기
url = "https://www.google.com"
driver.get(url)

# 브라우저가 바로 종료되는 문제 해결을 위한 대기시간 추가
time.sleep(5)

# 크롬 드라이버 종료
driver.quit()