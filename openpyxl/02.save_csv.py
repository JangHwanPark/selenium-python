import pandas as pd

# 1. 판다스를 사용하여 엑셀, CSV 저장
# 데이터 생성
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [30, 25, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 2. 엑셀 파일 저장
df.to_excel('xlsx_data/exam02.xlsx', index=False)

# 3. CSV 파일 저장
df.to_csv('csv_data/exam01.csv', index=False)