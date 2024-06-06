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
    cities = [
        "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
        "수원시", "성남시", "안양시", "부천시", "광명시", "평택시", "과천시", "오산시", "시흥시", "군포시", "의왕시", "하남시",
        "용인시", "이천시", "안산시", "고양시", "의정부시", "동두천시", "구리시", "남양주시", "파주시", "양주시", "포천시",
        "여주시", "연천군", "가평군", "양평군",
        "천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군",
        "홍성군", "예산군", "태안군",
        "청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군",
        "전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군",
        "고창군", "부안군",
        "목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군",
        "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군",
        "포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군",
        "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군",
        "창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군",
        "남해군", "하동군", "산청군", "함양군", "거창군", "합천군",
        "제주시", "서귀포시"
    ]

    genders = ["남성", "여성"]
    occupations = [
        "엔지니어", "디자이너", "마케터", "교사", "의사", "간호사", "개발자", "매니저", "교수",
        "변호사", "판사", "회계사", "건축가", "약사", "연구원", "기자", "작가", "번역가", "통역사",
        "영업사원", "기획자", "경영자", "비서", "사무직", "은행원", "투자분석가", "경찰관", "소방관",
        "군인", "운전기사", "배달원", "요리사", "바리스타", "웨이터", "미용사", "네일아티스트", "피부관리사",
        "운동선수", "코치", "트레이너", "연예인", "가수", "배우", "방송인", "작곡가", "음악가", "화가",
        "조각가", "사진작가", "영화감독", "프로듀서", "무용가", "디제이", "아나운서", "강사", "교육컨설턴트",
        "심리상담사", "사회복지사", "환경운동가", "인권운동가", "프로그래머", "데이터사이언티스트", "AI전문가",
        "네트워크엔지니어", "보안전문가", "시스템엔지니어", "프로젝트매니저", "제품관리자", "품질관리자",
        "공장노동자", "현장감독", "건설노동자", "인테리어디자이너", "패션디자이너", "뷰티블로거", "유튜버",
        "게임개발자", "애니메이터", "카피라이터", "광고기획자", "여행가이드", "항공기조종사", "승무원", "선장",
        "선원", "농부", "어부", "축산업자", "환경과학자", "식물학자", "동물학자", "지질학자", "천문학자",
        "생물학자", "화학자", "물리학자", "수학자", "통계학자", "경제학자", "정치학자", "사회학자",
        "철학자", "역사학자", "언어학자", "심리학자", "고고학자", "인류학자", "민속학자", "종교학자",
        "문헌학자", "문학평론가"
    ]


    users = []
    for i in range(1, num_users + 1):
        uid = str(uuid.uuid4())
        name = f"user{i}"
        password = f"welcome2ansan12!!"
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
            "password": password,
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

    return users


def generate_order_data(num_orders, user_numbers):
    # 주문 상태, 결제 방법, 할인 코드 목록
    order_statuses = ["처리 중", "배송 중", "배송 완료"]
    payment_methods = ["신용카드", "페이팔", "계좌이체", "카카오 페이"]
    discount_codes = ["DISC10", "SAVE15", "FREESHIP", None]

    orders = []
    print('=' * 10 + 'generate_order_data' + '=' * 10)
    for i in range(0, num_orders):
        order_id = str(uuid.uuid4())
        user_id = user_numbers[i]['uid']
        order_date = generate_random_date(
            datetime(2023, 1, 1),
            datetime(2024, 5, 27)).strftime("%Y-%m-%d")
        delivery_date = (datetime.strptime(
            order_date, "%Y-%m-%d") + timedelta(
            days=random.randint(1, 10))).strftime("%Y-%m-%d")
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
            'oid': order_id,
            'uid': user_id,
            'order_date': order_date,
            'delivery_date': delivery_date,
            "quantity": quantity,
            # "product_id": product_id,
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

        print(f'order_data: {order_data}')
        orders.append(order_data)

    return orders


def save_user_data_to_csv(users, filename):
    df = pd.DataFrame(users)
    df.to_csv(filename, index=False)


# 사용자 번호 저장용 리스트
uid_list = []

# 사용자 데이터 생성 및 CSV 파일로 저장
user_list = generate_user_data(20000, uid_list)
save_user_data_to_csv(user_list, 'csv_data/users.csv')

print(user_list[:2])
print('\n')
print(user_list[0]['uid'])
print(user_list[1]['uid'])
print('\n')
for i in range(0, 5):
    print(user_list[i]['uid'])
print('\n')

# 주문 데이터 생성 및 CSV 파일로 저장
# order_list = generate_order_data(10, user_list)
# save_user_data_to_csv(order_list, 'csv_data/orders.csv')