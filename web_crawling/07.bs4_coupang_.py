import requests
import re
from bs4 import BeautifulSoup

url = "https://www.coupang.com/np/campaigns/82/components/194176"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
print(f"Get URL: {url}")

res = requests.get(url, headers=headers)
res.raise_for_status()
print(f"Response Status Code: {res.status_code}")

soup = BeautifulSoup(res.text, "html.parser")
products = soup.find_all("li", attrs={"class": re.compile("^baby-product renew-badge")})
# print(products[0].find("div", attrs={"class": "prod_main_info"}).get_text())\

products_list = []
for product in products:
    data = product.find("dl", attrs={"class": "baby-product-wrap adjust-spacing"}).get_text()
    data = re.sub(r'\s+', ' ', data).strip()
    products_list.append(data)
    print(data)

with open("danawa.html", "w", encoding="utf=8") as file:
    for product in products_list:
        file.write(product + "\n\n")