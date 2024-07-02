import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import pandas as pd
import time

# 크롬 셀레니움 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")

# 위치 정보 관련 설정 추가
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
})

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 알림 처리 함수
def handle_alert():
    try:
        alert = Alert(driver)
        alert.dismiss()
        print("Alert dismissed")
    except:
        print("No alert present")

# 웹사이트로부터 HTML 가져오기
url = 'https://www.redfin.com/houses-near-me'
driver.get(url)

# 페이지 로드 후 잠시 대기
time.sleep(5)

# 알림 처리
handle_alert()

# 데이터 추출 및 저장을 위한 리스트
data = []

# 매물 정보 추출 함수
def extract_listing_info(listing):
    try:
        price = listing.find_element(By.CLASS_NAME, "homecardV2Price").text
        home_state = listing.find_element(By.CLASS_NAME, "HomeStatsV2").text
        address = listing.find_element(By.CLASS_NAME, "addressDisplay").text
        return {'price': price, 'home_state': home_state, 'address': address}
    except NoSuchElementException:
        return None

# 페이지가 로드될 때까지 대기
wait = WebDriverWait(driver, 20)
try:
    # 알림 다시 처리
    handle_alert()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "HomeCardContainer")))
except TimeoutException:
    print("Timeout waiting for page to load")
    driver.quit()
    exit()

# 스크롤 함수
def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 매물 정보 추출
max_scrolls = 5  # 스크롤 횟수 제한
scroll_count = 0

while scroll_count < max_scrolls:
    listings = driver.find_elements(By.CLASS_NAME, "HomeCardContainer")

    for listing in listings:
        info = extract_listing_info(listing)
        if info and info not in data:
            data.append(info)
            print(f"Extracted: {info}")

    scroll_page()
    scroll_count += 1

driver.quit()

# 데이터프레임으로 변환
df = pd.DataFrame(data)

# JSON 파일로 저장
with open('listings.json', 'w') as f:
    json.dump(data, f, indent=4)

# CSV 파일로 저장
df.to_csv('listings.csv', index=False)

print(f"Data saved to listings.json and listings.csv. Total listings: {len(data)}")