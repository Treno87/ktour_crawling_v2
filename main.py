# main.py
from datetime import datetime
import calendar
from browser_controller import setup_browser
from scraper import (
    login,
    click_date_button,
    click_calendar_date,
    has_reservations,
    click_reservation_text,
    click_team_button,
    scrape_details
)
from gsheets_client import save_to_sheet
from slack_notifier import SlackNotifier
from config import TARGET_URL, LOGIN_ID, LOGIN_PASSWORD, GOOGLE_SHEETS_URL


def get_date_range_for_month() -> list[str]:
    """
    오늘부터 해당 월의 마지막 날까지의 날짜(일) 목록을 반환합니다.
    예: 1/18 실행 시 ["18", "19", ..., "31"] 반환
    """
    today = datetime.now()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return [str(day) for day in range(today.day, last_day + 1)]


def main():
    """
    메인 실행 함수
    1. 브라우저 실행
    2. 로그인
    3. 오늘부터 월말까지 모든 날짜 순회
    4. 각 날짜별 예약 데이터 스크래핑
    5. Google Sheets에 중복 제외 저장
    6. Slack 알림 (당일 예약현황 + 새로 추가된 예약 구분)
    7. 브라우저 종료
    """
    today = datetime.now()
    today_str = f"{today.year}-{today.month:02d}-{today.day:02d}"

    print("=" * 50)
    print("Ktourstory 예약 정보 크롤링 시작")
    print("=" * 50)

    # 날짜 범위 계산
    target_days = get_date_range_for_month()
    print(f"검색 대상: {today.month}월 {target_days[0]}일 ~ {target_days[-1]}일 ({len(target_days)}일간)")

    # 1. 브라우저 실행
    print("\n[1/6] 브라우저 실행 중...")
    page, browser, context = setup_browser()
    print("[OK] 브라우저 실행 완료")

    all_scraped_data = []  # 전체 스크래핑 데이터

    try:
        # 2. 타겟 URL로 이동 및 로그인
        print("\n[2/6] 로그인 중...")
        page.goto(TARGET_URL)
        login(page, LOGIN_ID, LOGIN_PASSWORD)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        print("[OK] 로그인 완료")

        # 3. 각 날짜별 스크래핑
        print(f"\n[3/6] 날짜별 예약 조회 중... (총 {len(target_days)}일)")
        for idx, target_day in enumerate(target_days, 1):
            reservation_date = f"{today.year}-{today.month:02d}-{int(target_day):02d}"
            print(f"\n  [{idx}/{len(target_days)}] {reservation_date} 조회 중...")

            # 날짜 선택
            click_date_button(page)
            page.wait_for_timeout(1000)
            click_calendar_date(page, target_day)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # 예약 내역 확인
            if not has_reservations(page):
                print(f"  [{idx}/{len(target_days)}] {reservation_date}: 예약 없음")
                continue

            # 예약 상세 조회
            click_reservation_text(page)
            page.wait_for_timeout(2000)
            click_team_button(page)
            page.wait_for_timeout(2000)

            # 데이터 스크래핑
            scraped_data = scrape_details(page, reservation_date)
            all_scraped_data.extend(scraped_data)
            print(f"  [{idx}/{len(target_days)}] {reservation_date}: {len(scraped_data)}건 수집")

        print(f"\n[4/6] 전체 스크래핑 완료 (총 {len(all_scraped_data)}건)")

        # 4. 데이터 저장
        print("\n[5/6] Google Sheets에 데이터 저장 중...")
        if all_scraped_data:
            new_reservations, existing_reservations = save_to_sheet(all_scraped_data)
        else:
            new_reservations, existing_reservations = [], []
        print("[OK] 데이터 저장 완료")

        # 5. Slack 알림 전송
        print("\n[6/6] Slack 알림 전송 중...")
        slack = SlackNotifier()

        # 당일 예약 필터링
        today_reservations = [
            r for r in (new_reservations + existing_reservations)
            if r.get("날짜") == today_str
        ]

        # Slack 메시지 생성 및 전송
        message = slack.format_daily_summary_message(
            today_reservations=today_reservations,
            new_reservations=new_reservations,
            today_date=today_str,
            notify_everyone=bool(new_reservations),
            sheet_url=GOOGLE_SHEETS_URL if GOOGLE_SHEETS_URL else None
        )
        slack.send_message(message)

        print("\n" + "=" * 50)
        print("모든 작업 완료!")
        print(f"  - 당일({today_str}) 예약: {len(today_reservations)}건")
        print(f"  - 새로 추가된 예약: {len(new_reservations)}건")
        print("=" * 50)

    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        try:
            slack = SlackNotifier()
            slack.send_message(f"🚨 크롤링 작업 실패: {e}")
        except Exception:
            pass
        raise

    finally:
        print("\n브라우저 종료 중...")
        try:
            context.close()
            browser.close()
        except Exception:
            pass
        print("[OK] 브라우저 종료 완료")


if __name__ == "__main__":
    main()