import pandas as pd
from faker import Faker
import random

# Faker 초기화
fake = Faker()

# 데이터셋 크기 설정
num_posts = 1000  # 1000개의 게시물
num_authors = 100  # 100명의 작성자

# 작성자 ID 생성
author_ids = [fake.uuid4() for _ in range(num_authors)]

# 게시물 데이터 생성
posts_data = {
    "post_id": [fake.uuid4() for _ in range(num_posts)],
    "author_id": [random.choice(author_ids) for _ in range(num_posts)],
    "title": [fake.sentence(nb_words=6) for _ in range(num_posts)],
    "content": [fake.text(max_nb_chars=200) for _ in range(num_posts)],
    "created_at": [fake.date_time_between(start_date='-1y', end_date='now') for _ in range(num_posts)],
    "updated_at": [fake.date_time_between(start_date='-1y', end_date='now') for _ in range(num_posts)],
    "views": [random.randint(0, 10000) for _ in range(num_posts)],
    "likes": [random.randint(0, 1000) for _ in range(num_posts)],
    "comments": [random.randint(0, 500) for _ in range(num_posts)],
    "tags": [','.join(fake.words(nb=random.randint(1, 5))) for _ in range(num_posts)]
}

# 데이터프레임 생성
df_posts = pd.DataFrame(posts_data)

# 생성된 데이터프레임 출력
print(df_posts.head())
csv_file_path = "csv_data/posts_data.csv"
df_posts.to_csv(csv_file_path, index=False, encoding='utf-8-sig')