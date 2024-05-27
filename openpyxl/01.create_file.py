from openpyxl import Workbook

# 1. 파일 생성
# 워크북 생성
wb = Workbook()

# 활성화된 시트 선택
ws = wb.active

# 시트 이름 변경 (옵션)
ws.title = "시트 이름 변경"

# 2. 데이터 삽입
# 셀에 직접 삽입
ws['A1'] = "Open"
ws['B1'] = "Py"
ws['C1'] = "Xl"

# 반복문으로 삽입
data = [
    ['Name', 'Age', 'City', 'Birth'],
    ['Alice', 30, 'New York', 2000],
    ['Bob', 25, 'Los Angeles', 2001],
    ['Charlie', 35, 'Chicago']
]

for row in data:
    ws.append(row)

# 3. 엑셀 파일 저장
wb.save('xlsx_data/exam01.xlsx')