from config import (
    GOOGLE_SHEET_TITLE,
    GOOGLE_WORKSHEET_NAME,
    RESERVATION_DATA_HEADERS,
    CREDENTIALS_FILE
)
import gspread
from google.oauth2.service_account import Credentials


def save_to_sheet(data: list[dict]):
    """
    스크랩된 데이터를 구글 시트에 저장합니다.

    Args:
        data: 저장할 예약 정보 딕셔너리 리스트
              각 딕셔너리는 RESERVATION_DATA_HEADERS에 정의된 키를 가져야 합니다.
    """
    # 1. Google Sheets API 인증
    gc = gspread.service_account(filename=CREDENTIALS_FILE)

    # 2. 스프레드시트 열기 (없으면 생성)
    try:
        spreadsheet = gc.open(GOOGLE_SHEET_TITLE)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"스프레드시트 '{GOOGLE_SHEET_TITLE}'를 찾을 수 없습니다. 새로 생성합니다.")
        spreadsheet = gc.create(GOOGLE_SHEET_TITLE)
        print(f"스프레드시트 '{GOOGLE_SHEET_TITLE}' 생성 완료.")

    # 3. 워크시트 열기 (없으면 생성)
    try:
        worksheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        print(f"워크시트 '{GOOGLE_WORKSHEET_NAME}'를 찾을 수 없습니다. 새로 생성합니다.")
        worksheet = spreadsheet.add_worksheet(
            title=GOOGLE_WORKSHEET_NAME,
            rows="1000",
            cols="20"
        )
        print(f"워크시트 '{GOOGLE_WORKSHEET_NAME}' 생성 완료.")

    # 4. 헤더 확인 및 작성
    all_values = worksheet.get_all_values()
    if not all_values or all_values[0] != RESERVATION_DATA_HEADERS:
        # 헤더가 없거나 다르면 시트를 초기화하고 헤더를 작성
        worksheet.clear()
        worksheet.append_row(RESERVATION_DATA_HEADERS)
        print("헤더 작성 완료.")

    # 5. 데이터 행 추가
    for reservation in data:
        row = [
            reservation.get("이름", ""),
            reservation.get("상품명", ""),
            reservation.get("예약시간", ""),
            reservation.get("예약번호", ""),
            reservation.get("국적", ""),
            reservation.get("크롤링 일자", "")
        ]
        worksheet.append_row(row)

    print(f"{len(data)}개의 예약 정보를 구글 시트에 저장했습니다.")