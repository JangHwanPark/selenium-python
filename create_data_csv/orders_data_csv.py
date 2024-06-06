import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Faker 초기화
fake = Faker()

# 주문 데이터셋 크기 설정
num_orders = 1000  # 1000개의 주문 데이터 생성

# 주문 데이터 생성
orders_data = {
    "oid": [fake.uuid4() for _ in range(num_orders)],  # 주문 고유 ID
    "uid": [fake.uuid4() for _ in range(num_orders)],  # 사용자 고유 ID
    "order_date": [fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_orders)],  # 주문 날짜
    "delivery_date": [
        (datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d %H:%M:%S')
        for order_date in [fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_orders)]
    ],  # 배송 날짜 (1-14일 후)
    "quantity": [random.randint(1, 10) for _ in range(num_orders)],  # 수량
    "order_status": [random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled']) for _ in range(num_orders)],  # 주문 상태
    "payment_method": [random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']) for _ in range(num_orders)],  # 결제 방법
    "discount_code": [fake.bothify(text='DISCOUNT-###') if random.choice([True, False]) else '' for _ in range(num_orders)],  # 할인 코드 (있거나 없음)
    "shopping_cost": [round(random.uniform(10.0, 200.0), 2) for _ in range(num_orders)],  # 쇼핑 비용
    "tracking_number": [fake.bothify(text='TRACK-##########') for _ in range(num_orders)],  # 추적 번호
    "customer_note": [fake.sentence(nb_words=10) if random.choice([True, False]) else '' for _ in range(num_orders)]  # 고객 메모 (있거나 없음)
}

# 데이터프레임 생성
df_orders = pd.DataFrame(orders_data)

# 생성된 데이터프레임 CSV로 저장
csv_file_path = "csv_data/orders_data.csv"
df_orders.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"CSV 파일이 성공적으로 생성되었습니다: {csv_file_path}")