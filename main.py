# main.py
from browser_controller import setup_browser
from scraper import (
    login,
    close_login_dialog,
    click_date_button,
    click_calendar_date,
    has_reservations,
    click_reservation_text,
    click_team_button,
    scrape_details
)
from gsheets_client import save_to_sheet
from config import TARGET_URL, LOGIN_ID, LOGIN_PASSWORD


def main():
    """
    메인 실행 함수
    1. 브라우저 실행
    2. 로그인
    3. 날짜 선택 및 예약 내역 조회
    4. 데이터 스크래핑
    5. 데이터 저장
    6. 브라우저 종료
    """
    print("=" * 50)
    print("Ktourstory 예약 정보 크롤링 시작")
    print("=" * 50)

    # 1. 브라우저 실행
    print("\n[1/6] 브라우저 실행 중...")
    page, browser, context = setup_browser()
    print("[OK] 브라우저 실행 완료")

    try:
        # 2. 타겟 URL로 이동 및 로그인
        print("\n[2/6] 로그인 중...")
        page.goto(TARGET_URL)
        login(page, LOGIN_ID, LOGIN_PASSWORD)
        print("[OK] 로그인 완료")

        # 3. 날짜 선택 (14일 기준)
        print("\n[3/6] 날짜 선택 중...")
        click_date_button(page)
        click_calendar_date(page, "14")
        print("[OK] 날짜 선택 완료 (14일)")

        # 4. 예약 내역 확인
        print("\n[4/6] 예약 내역 확인 중...")
        if not has_reservations(page):
            print("[INFO] 해당 날짜에 예약이 없습니다.")
            print("\n" + "=" * 50)
            print("작업 완료 (예약 없음)")
            print("=" * 50)
            return

        # 5. 예약 내역 조회
        print("[OK] 예약이 존재합니다. 상세 조회 중...")
        click_reservation_text(page)
        click_team_button(page)
        print("[OK] 예약 내역 조회 완료")

        # 6. 데이터 스크래핑
        print("\n[5/6] 데이터 스크래핑 중...")
        scraped_data = scrape_details(page)
        print(f"[OK] 데이터 스크래핑 완료 ({len(scraped_data)}개의 예약 정보)")

        # 7. 데이터 저장
        print("\n[6/6] Google Sheets에 데이터 저장 중...")
        save_to_sheet(scraped_data)
        print("[OK] 데이터 저장 완료")

        print("\n" + "=" * 50)
        print("모든 작업 완료!")
        print("=" * 50)

    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        raise

    finally:
        # 7. 브라우저 종료
        print("\n브라우저 종료 중...")
        context.close()
        browser.close()
        print("[OK] 브라우저 종료 완료")


if __name__ == "__main__":
    main()