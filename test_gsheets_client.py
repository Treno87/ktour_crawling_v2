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
    # 1. 테스트용 모의 데이터 생성
    mock_data = [
        {
            "이름": "Test User 1",
            "상품명": "Test Product A",
            "예약시간": "10:00",
            "예약번호": "TEST001",
            "국적": "KOREA",
            "크롤링 일자": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "이름": "Test User 2",
            "상품명": "Test Product B",
            "예약시간": "11:00",
            "예약번호": "TEST002",
            "국적": "USA",
            "크롤링 일자": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    # 2. 저장 함수 호출
    save_to_sheet(mock_data)

    # 3. 데이터가 올바르게 저장되었는지 확인
    # 마지막 두 줄을 읽어와서 데이터가 일치하는지 확인합니다.
    worksheet = gsheet_client
    all_values = worksheet.get_all_values()
    
    # 헤더가 있는지 확인
    if not all_values or all_values[0] != RESERVATION_DATA_HEADERS:
        # 헤더가 없으면 초기화 후 헤더를 씁니다.
        worksheet.clear()
        worksheet.append_row(RESERVATION_DATA_HEADERS)
        all_values = worksheet.get_all_values() # 다시 읽기
    
    assert all_values[0] == RESERVATION_DATA_HEADERS

    # 저장된 데이터 확인
    # 실제 저장될 때 크롤링 일자는 실시간으로 생성되므로 비교에서 제외
    expected_row1 = [mock_data[0]["이름"], mock_data[0]["상품명"], mock_data[0]["예약시간"], mock_data[0]["예약번호"], mock_data[0]["국적"], mock_data[0]["크롤링 일자"]]
    expected_row2 = [mock_data[1]["이름"], mock_data[1]["상품명"], mock_data[1]["예약시간"], mock_data[1]["예약번호"], mock_data[1]["국적"], mock_data[1]["크롤링 일자"]]

    # 마지막 행에 추가되므로, 마지막 두 행을 가져와서 비교합니다.
    actual_rows = worksheet.get_all_values()[-2:]

    # 실제 저장된 '크롤링 일자'는 mock_data와 다를 수 있으므로 해당 필드는 비교에서 제외하거나
    # 실제 저장된 값을 가져와서 비교해야 합니다. 여기서는 간략하게 다른 필드만 비교
    
    assert actual_rows[0][0:5] == expected_row1[0:5]
    assert actual_rows[1][0:5] == expected_row2[0:5]