import requests

# 1번 get 요청 테스트
res = requests.get("https://www.google.com")
# res = requests.get("https://www.google.com/error")
print(f"응답코드: {res.status_code}")

if res.status_code == requests.codes.ok:
    print("정상입니다.")
else:
    print(f"문제가 생겼습니다. [에러코드 {res.status_code}]")

# 1. 올바른 html 문서인지 확인 (잘못된 문서면 에러발생)
res.raise_for_status()
print("웹 스크래핑을 진행합니다.")

# 2. 텍스트 출력
print(len(res.text))

# 3. 어떤 내용을 가져오는지 출력
print(res.text)

# 4. 파일로 저장 (쓰기모드 = w, 인코딩 = utf8)
with open("mygoogle.html", "w", encoding="utf8") as f:
    f.write(res.text)