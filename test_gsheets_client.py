import pytest
from gsheets_client import save_to_sheet
from config import GOOGLE_SHEET_TITLE, GOOGLE_WORKSHEET_NAME, RESERVATION_DATA_HEADERS
import gspread
from datetime import datetime

import os


@pytest.fixture(scope="module")
def gsheet_client():
    """
    gspread 클라이언트를 설정하고 테스트 후 정리합니다.
    (테스트용 시트 생성 및 공유, 실제 시트에는 영향을 주지 않음)
    """
    
    # credentials.json이 존재하고 유효한지 확인합니다.
    if not os.path.exists('credentials.json'):
        pytest.fail("credentials.json 파일이 프로젝트 루트에 없습니다. README.md를 참조하세요.")

    try:
        gc = gspread.service_account(filename='credentials.json')
        
        # 시트를 찾고 없으면 생성합니다.
        try:
            spreadsheet = gc.open(GOOGLE_SHEET_TITLE)
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Spreadsheet '{GOOGLE_SHEET_TITLE}' not found. Creating a new one.")
            spreadsheet = gc.create(GOOGLE_SHEET_TITLE)
            # 새 시트를 만들었다면 서비스 계정 이메일로 공유해야 합니다.
            # 이메일은 credentials.json 파일의 'client_email' 필드에 있습니다.
            service_account_email = gc.auth.service_account_email
            spreadsheet.share(service_account_email, perm_type='user', role='writer')
            print(f"Spreadsheet '{GOOGLE_SHEET_TITLE}' created and shared with '{service_account_email}'.")

        # 워크시트를 찾고 없으면 생성합니다.
        try:
            worksheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{GOOGLE_WORKSHEET_NAME}' not found. Creating a new one.")
            worksheet = spreadsheet.add_worksheet(title=GOOGLE_WORKSHEET_NAME, rows="100", cols="20")
            print(f"Worksheet '{GOOGLE_WORKSHEET_NAME}' created.")

        yield worksheet
        
        # 테스트 후 시트 내용을 초기화할 수 있지만, 여기서는 그대로 둡니다.
        # worksheet.clear() # 실제 테스트 시 데이터가 계속 쌓이는 것을 피하려면 주석 해제

    except Exception as e:
        pytest.fail(f"Google Sheet 연동 설정 중 오류 발생: {e}. credentials.json 확인.")


def test_save_to_sheet(gsheet_client):
    """
    스크랩된 데이터를 구글 시트에 저장하는 기능을 테스트합니다.
    """
    # 1. 테스트용 모의 데이터 생성 (RESERVATION_DATA_HEADERS 키와 일치)
    mock_data = [
        {
            "날짜": "2026-01-14",
            "팀": "TEAM A",
            "고객명": "Test User 1",
            "예약번호": "TEST001",
            "채널": "L",
            "인원구분": "Adult 1",
            "국가": "KOREA",
            "예약상품": "Test Product A",
            "예약시간": "10:00",
            "금액": "110,000",
            "is_new": ""
        },
        {
            "날짜": "2026-01-14",
            "팀": "TEAM A",
            "고객명": "Test User 2",
            "예약번호": "TEST002",
            "채널": "VI",
            "인원구분": "Adult 2",
            "국가": "USA",
            "예약상품": "Test Product B",
            "예약시간": "11:00",
            "금액": "80,000",
            "is_new": ""
        }
    ]

    # 2. 저장 함수 호출
    new_reservations, existing_reservations = save_to_sheet(mock_data)

    # 3. 새 예약으로 추가되었는지 확인
    assert len(new_reservations) == 2
    assert new_reservations[0]["예약번호"] == "TEST001"
    assert new_reservations[1]["예약번호"] == "TEST002"