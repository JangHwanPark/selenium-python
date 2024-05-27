import random
import uuid
import pandas as pd
from datetime import datetime, timedelta


def generate_phone_number():
    first_part = "010"
    second_part = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    third_part = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return f"{first_part}-{second_part}-{third_part}"


def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))


def generate_user_data(num_users, user_numbers):
    cities = ["서울시", "평택시", "부천시", "시흥시", "인천시", "부산시", "대구시", "천안시", "안양시", "안산시"]
    genders = ["남성", "여성"]
    occupations = ["엔지니어", "디자이너", "마케터", "교사", "의사", "간호사", "개발자", "매니저", "교수"]

    users = []
    for i in range(1, num_users + 1):
        uid = str(uuid.uuid4())
        name = f"user{i}"
        age = random.randint(20, 60)
        city = random.choice(cities)
        email = f"user{i}@gmail.com"
        phone = generate_phone_number()
        gender = random.choice(genders)
        occupation = random.choice(occupations)
        join_date = generate_random_date(datetime(2010, 1, 1), datetime(2024, 5, 27)).strftime("%Y-%m-%d")
        address = f"{city} {random.randint(1, 100)}-{random.randint(1, 100)}번지"

        user_data = {
            "uid": uid,
            "name": name,
            "age": age,
            "city": city,
            "email": email,
            "phone": phone,
            "gender": gender,
            "occupation": occupation,
            "join_date": join_date,
            "address": address
        }
        users.append(user_data)
        user_numbers.append(user_data["uid"])

    return users, user_numbers


def save_user_data_to_csv(users, filename):
    df = pd.DataFrame(users)
    df.to_csv(filename, index=False)


def generate_order_data(num_orders, users):
    # 주문 상태, 결제 방법, 할인 코드 목록
    order_statuses = ["처리 중", "배송 중", "배송 완료"]
    payment_methods = ["신용카드", "페이팔", "계좌이체", "카카오 페이"]
    discount_codes = ["DISC10", "SAVE15", "FREESHIP", None]

    orders = []
    for _ in range(num_orders):
        order_id = str(uuid.uuid4())
        user = random.choice(users)
        user_id = random.choice(users)

        # product = random.choice(products)
        # product_id = product["product_id"]

        order_date = generate_random_date(datetime(2023, 1, 1), datetime(2024, 5, 27)).strftime("%Y-%m-%d")
        delivery_date = (datetime.strptime(order_date, "%Y-%m-%d") + timedelta(days=random.randint(1, 10))).strftime(
            "%Y-%m-%d")
        quantity = random.randint(1, 5)

        # price = product["price"]
        # total_price = quantity * price
        # shipping_address = user["address"]
        order_status = random.choice(order_statuses)
        payment_method = random.choice(payment_methods)
        discount_code = random.choice(discount_codes)
        shipping_cost = random.uniform(0, 20) if discount_code != "FREESHIP" else 0
        tracking_number = str(uuid.uuid4())[:12]
        customer_note = random.choice([None, "Please deliver after 5 PM", "Leave at the front door", None])

        order_data = {
            "order_id": order_id,
            "user_id": user_id,
            # "product_id": product_id,
            "order_date": order_date,
            "delivery_date": delivery_date,
            "quantity": quantity,
            # "price": price,
            # "total_price": total_price,
            # "shipping_address": shipping_address,
            "order_status": order_status,
            "payment_method": payment_method,
            "discount_code": discount_code,
            "shipping_cost": round(shipping_cost, 2),
            "tracking_number": tracking_number,
            "customer_note": customer_note
        }
        orders.append(order_data)

    return orders


def iterator_list(item_list):
    for item in item_list:
        return item


# 사용자 번호 저장용 리스트
uid_list = []

# 사용자 데이터, 주문 데이터 생성
iterator_data = 10000
user_list = generate_user_data(iterator_data, uid_list)
order_list = generate_order_data(iterator_data, user_list)

# 터미널 출력 (테스트)
print_item = iterator_list(user_list)
print(print_item)

# 사용자 아이디 얻는 함수
# print_uid = get_user_uid(user_list, uid_list)
# print(print_uid)

for i in uid_list:
    print(i)

# CSV 파일로 저장
save_user_data_to_csv(user_list, 'csv_data/users.csv')