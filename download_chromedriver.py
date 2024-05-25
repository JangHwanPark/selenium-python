import requests
import zipfile
import os

# 엔드포인트 주소
endpoint = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

# 엔드포인트에 GET 요청을 보내고 응답 받기
response = requests.get(endpoint)
data = response.json()

# 크롬 드라이버 버전 (상시 업데이트)
desired_version = "125.0.6422.77"

# 필요한 플랫폼에 맞는 URL 추출
platform = "win64"
downloads = data["channels"]["Stable"]["downloads"]["chromedriver"]
url = next(item["url"] for item in downloads if item["url"].endswith(f"{platform}.zip"))

# 크롬 드라이버 다운로드
response = requests.get(url)
zip_path = "chromedriver.zip"

with open(zip_path, "wb") as file:
    file.write(response.content)

# 압출 풀기
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall("chromedriver")

# 압축 파일 삭제
os.remove(zip_path)

print("Chrome드라이버가 성공적으로 다운로드 및 추가되었습니다.")