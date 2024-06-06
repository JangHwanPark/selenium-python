import pandas as pd
from faker import Faker
import random

# Faker 초기화
fake = Faker()

# 관리자 데이터셋 크기 설정
num_admins = 50  # 50명의 관리자

# 관리자 데이터 생성
admins_data = {
    "admin_id": [fake.uuid4() for _ in range(num_admins)],
    "username": [fake.user_name() for _ in range(num_admins)],
    "password": [fake.password(length=12) for _ in range(num_admins)],  # 암호화된 패스워드 필요
    "email": [fake.email() for _ in range(num_admins)],
    "created_at": [fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_admins)],
    "last_login": [fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_admins)],
    "is_active": [random.choice([True, False]) for _ in range(num_admins)]  # 활성화 여부
}

# 데이터프레임 생성
df_admins = pd.DataFrame(admins_data)

# 생성된 데이터프레임 CSV로 저장
csv_file_path = "csv_data/admins_data.csv"
df_admins.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"CSV 파일이 성공적으로 생성되었습니다: {csv_file_path}")