import json
import os
from datetime import datetime

# 가계부 데이터 파일
expenses_file = 'expenses.json'

# 1. 일일 지출 한도 설정 기능
def set_daily_limit():
    try:
        limit = float(input("일일 지출 한도를 설정하세요 (원): "))
        with open('daily_limit.json', 'w') as file:
            json.dump({"limit": limit}, file)
        print(f"일일 지출 한도가 {limit}원으로 설정되었습니다.")
    except ValueError:
        print("유효한 금액을 입력하세요.")

def get_daily_limit():
    if os.path.exists('daily_limit.json'):
        with open('daily_limit.json', 'r') as file:
            data = json.load(file)
        return data.get("limit", None)
    return None

def check_daily_limit():
    limit = get_daily_limit()
    if limit is None:
        print("설정된 일일 지출 한도가 없습니다.")
        return
    
    total_spent_today = 0
    today = datetime.today().strftime('%Y-%m-%d')
    with open(expenses_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for expense in data:
            if expense['date'] == today:
                total_spent_today += float(expense['amount'])
    
    print(f"오늘 지출: {total_spent_today}원")
    if total_spent_today > limit:
        print(f"경고: 오늘의 지출이 한도를 초과했습니다! ({limit}원 초과)")
    else:
        print(f"남은 한도: {limit - total_spent_today}원")

# 2. 특정 기간 내 지출 분석 기능
def analyze_expenses_in_period():
    start_date = input("시작 날짜를 입력하세요 (예: 2024-05-01): ")
    end_date = input("종료 날짜를 입력하세요 (예: 2024-05-31): ")

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("올바른 날짜 형식을 입력하세요 (YYYY-MM-DD).")
        return

    total_expense = 0
    category_totals = {}
    with open(expenses_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for expense in data:
            expense_date_obj = datetime.strptime(expense['date'], "%Y-%m-%d")
            if start_date_obj <= expense_date_obj <= end_date_obj:
                amount = float(expense['amount'])
                total_expense += amount
                category = expense['item']
                if category not in category_totals:
                    category_totals[category] = 0
                category_totals[category] += amount

    print(f"{start_date}부터 {end_date}까지의 총 지출: {total_expense} 원")
    print("카테고리별 지출 내역:")
    for category, total in category_totals.items():
        print(f"{category}: {total} 원")

# 3. 지출 패턴 예측 기능
def predict_future_expenses():
    days = int(input("몇 일 후까지의 지출을 예측하시겠습니까? (예: 30): "))
    total_expense = 0
    days_count = 0

    with open(expenses_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for expense in data:
            total_expense += float(expense['amount'])
            days_count += 1

    if days_count == 0:
        print("지출 내역이 없습니다.")
        return

    daily_average_expense = total_expense / days_count
    future_expense = daily_average_expense * days
    print(f"예상 일일 평균 지출: {daily_average_expense:.2f} 원")
    print(f"{days}일 후 예상 총 지출: {future_expense:.2f} 원")