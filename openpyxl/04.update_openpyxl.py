from openpyxl import Workbook

# 워크북 생성
wb = Workbook()

# 활성화된 시트 선택
ws = wb.active

# 데이터 삽입
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles'],
    ['Charlie', 35, 'Chicago'],
    ['JPark', 38, 'Seoul']
]

for row in data:
    ws.append(row)

# 특정 셀 데이터 수정
ws['B2'] = 28  # 첫 번째 행, 두 번째 열(Age)의 값을 28로 수정
ws['C3'] = 'San Francisco'  # 두 번째 행, 세 번째 열(City)의 값을 'San Francisco'로 수정

# 특정 행 데이터 수정
ws['A4'] = 'Charlie'
ws['B4'] = 36
ws['C4'] = 'Boston'
ws['D4'] = 22

# 특정 열 데이터 수정
for cell in ws['B']:
    if cell.row != 1:  # 첫 번째 행(헤더 행)은 제외
        cell.value += 1

# 특정 값을 가진 셀 수정
for cell in ws['C']:
    if cell.value == 'Chicago':
        cell.value = 'Seattle'

# 수정된 데이터프레임 출력
for row in ws.iter_rows(values_only=True):
    print(row)

# 엑셀 파일 저장
wb.save('xlsx_data/update_file.xlsx')