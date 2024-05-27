import pandas as pd

# 1. 데이터 생성
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [30, 25, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 2. 특정 셀 데이터 수정
# 첫 번째 행, 두 번째 열(Age)의 값을 28로 수정
df.iloc[0, 1] = 28

# 두 번째 행, 세 번째 열(City)의 값을 'San Francisco'로 수정
df.at[1, 'City'] = 'San Francisco'

# 3. 특정 행 데이터 수정
# 세 번째 행(Charlie)의 데이터를 수정
df.loc[2] = ['Charlie', 36, 'Boston']

# 4. 특정 열 데이터 수정
# 'Age' 열의 모든 값을 1씩 증가
df['Age'] = df['Age'] + 1

# 'City' 열의 특정 값을 변경
df['City'] = df['City'].replace({'Chicago': 'Seattle'})

# 수정된 데이터프레임 출력
print(df)

# 엑셀 파일로 저장
df.to_excel('xlsx_data/update_file.xlsx', index=False)

# CSV 파일로 저장
df.to_csv('csv_data/update_file.csv', index=False)