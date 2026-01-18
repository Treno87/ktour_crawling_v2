from config import (
    GOOGLE_SHEET_TITLE,
    GOOGLE_WORKSHEET_NAME,
    RESERVATION_DATA_HEADERS,
    CREDENTIALS_FILE
)
import gspread
import json
import os


def fix_json_newlines(json_str):
    """JSON 문자열 내부의 실제 줄바꿈을 \\n으로 변환"""
    result = []
    in_string = False
    i = 0
    while i < len(json_str):
        char = json_str[i]

        if char == '"' and (i == 0 or json_str[i-1] != '\\'):
            in_string = not in_string
            result.append(char)
        elif in_string and char == '\n':
            result.append('\\n')
        elif in_string and char == '\r':
            pass
        else:
            result.append(char)

        i += 1

    return ''.join(result)


def get_gspread_client():
    """
    Google Sheets API 클라이언트를 반환합니다.
    환경변수 GOOGLE_CREDENTIALS_JSON이 있으면 해당 값을 사용하고,
    없으면 credentials.json 파일을 사용합니다.
    """
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if creds_json:
        creds_json = fix_json_newlines(creds_json)
        creds_dict = json.loads(creds_json)
        return gspread.service_account_from_dict(creds_dict)
    else:
        return gspread.service_account(filename=CREDENTIALS_FILE)


def save_to_sheet(data: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    스크랩된 데이터를 구글 시트에 저장합니다.
    중복 확인 후 새로운 데이터만 추가합니다.

    Args:
        data: 저장할 예약 정보 딕셔너리 리스트

    Returns:
        tuple: (새로 추가된 예약 리스트, 기존 예약 리스트)
    """
    if not data:
        print("저장할 데이터가 없습니다.")
        return [], []

    # 1. Google Sheets API 인증
    gc = get_gspread_client()

    # 2. 스프레드시트 열기 (이미 존재해야 함)
    try:
        spreadsheet = gc.open(GOOGLE_SHEET_TITLE)
        print(f"스프레드시트 '{GOOGLE_SHEET_TITLE}' 열기 완료")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"[ERROR] 스프레드시트 '{GOOGLE_SHEET_TITLE}'를 찾을 수 없습니다.")
        print("Google Drive에서 스프레드시트를 생성하고 서비스 계정과 공유해주세요.")
        raise

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

    # 4. 기존 데이터 가져오기
    all_values = worksheet.get_all_values()

    # 5. 헤더 확인 및 작성
    if not all_values or all_values[0] != RESERVATION_DATA_HEADERS:
        # 첫 행에 헤더가 없으면 추가
        if not all_values:
            worksheet.append_row(RESERVATION_DATA_HEADERS)
            print("헤더 작성 완료.")
            all_values = [RESERVATION_DATA_HEADERS]
        elif all_values[0] != RESERVATION_DATA_HEADERS:
            # 헤더가 다르면 첫 행에 삽입
            worksheet.insert_row(RESERVATION_DATA_HEADERS, 1)
            print("헤더 삽입 완료.")
            all_values = [RESERVATION_DATA_HEADERS] + all_values

    # 6. 기존 예약번호 목록 추출 (중복 확인용)
    existing_reservation_nos = set()
    if len(all_values) > 1:
        # 예약번호는 4번째 컬럼 (인덱스 3)
        reservation_no_idx = RESERVATION_DATA_HEADERS.index("예약번호")
        for row in all_values[1:]:  # 헤더 제외
            if len(row) > reservation_no_idx:
                existing_reservation_nos.add(row[reservation_no_idx])

    print(f"기존 예약 {len(existing_reservation_nos)}건 확인")

    # 7. 중복 제거 및 새 데이터만 추가
    new_data = []
    for reservation in data:
        reservation_no = reservation.get("예약번호", "")
        if reservation_no and reservation_no not in existing_reservation_nos:
            new_data.append(reservation)

    # 기존 예약 리스트 (중복된 것들)
    existing_data = [
        reservation for reservation in data
        if reservation.get("예약번호", "") in existing_reservation_nos
    ]

    if not new_data:
        print("새로 추가할 데이터가 없습니다. (모두 중복)")
        return [], existing_data

    # 8. 새 데이터 행 추가
    rows_to_add = []
    for reservation in new_data:
        row = [
            reservation.get("날짜", ""),
            reservation.get("팀", ""),
            reservation.get("고객명", ""),
            reservation.get("예약번호", ""),
            reservation.get("채널", ""),
            reservation.get("인원구분", ""),
            reservation.get("국가", ""),
            reservation.get("예약상품", ""),
            reservation.get("예약시간", ""),
            reservation.get("금액", ""),
            reservation.get("is_new", "")
        ]
        rows_to_add.append(row)

    # 배치로 추가 (효율성)
    worksheet.append_rows(rows_to_add)

    print(f"{len(new_data)}개의 새 예약 정보를 구글 시트에 저장했습니다.")
    if len(data) - len(new_data) > 0:
        print(f"({len(data) - len(new_data)}개는 중복으로 제외됨)")

    # 새 예약에 is_new 플래그 설정
    for reservation in new_data:
        reservation['is_new'] = True
    for reservation in existing_data:
        reservation['is_new'] = False

    return new_data, existing_data
