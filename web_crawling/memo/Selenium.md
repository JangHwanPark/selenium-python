## select_one
- CSS 선택자로 첫번째 일치하는 요소 반환
```html
<h2 class="prod-buy-header__title">Product Title</h2>
```
```python
title_el = product_soup.select_one("h2.prod-buy-header__title")
print(title_el.text)  # 출력: Product Title
```

## find_all
- 태그랑 속성값을 사용해 일치하는 모든 요소를 리스트로 반환
```html
<div class="weblog carousel-contents-grid__product-unit">Product 1</div>
<div class="weblog carousel-contents-grid__product-unit">Product 2</div>
```
```python
products = soup.find_all("div", attrs={"class": re.compile("^weblog carousel-contents-grid__product-unit")})
for product in products:
    print(product.text)  # 출력: Product 1, Product 2
```

결론 = 하나만 찾을때는 select_one, 전부 찾을때는 find_all

<br>

## requests 모듈의 res(response) 객체 속성 및 메서드
주요 속성
status_code: HTTP 응답 상태 코드를 반환합니다. 예: 200, 404, 500 등.
headers: 응답 헤더를 사전 형태로 반환합니다.
text: 응답 본문을 문자열로 반환합니다.
content: 응답 본문을 바이트 형식으로 반환합니다.
json(): JSON 응답을 파싱하여 Python 사전으로 반환합니다.
url: 최종적으로 요청된 URL을 반환합니다. 리다이렉션이 발생한 경우 최종 URL이 반환됩니다.
history: 요청이 리다이렉트된 경우 response 객체들의 목록을 반환합니다.
cookies: 응답에 포함된 쿠키를 반환합니다.
elapsed: 요청과 응답 사이의 경과 시간을 timedelta 객체로 반환합니다.
encoding: 응답 콘텐츠의 인코딩을 반환하거나 설정합니다.
주요 메서드
raise_for_status(): 응답이 성공 상태(상태 코드가 200-299)가 아닌 경우 HTTPError 예외를 발생시킵니다.
iter_content(chunk_size=1, decode_unicode=False): 응답 내용을 지정된 크기만큼의 청크로 반복합니다. 대용량 파일 다운로드에 유용합니다.
iter_lines(chunk_size=512, decode_unicode=None, delimiter=None): 응답 내용을 줄 단위로 반복합니다. 스트리밍 API에 유용합니다.