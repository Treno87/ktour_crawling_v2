# crawl_january.py
# 2026년 1월 1일 ~ 1월 31일 크롤링용 별도 스크립트
# Playwright 자체 Chromium 사용 (SeleniumBase 불필요, Chrome 충돌 없음)

from playwright.sync_api import sync_playwright
from scraper import (
    login,
    click_date_button,
    has_reservations,
    click_reservation_text,
    click_team_button,
    get_team_count,
    scrape_details
)
from gsheets_client import save_to_sheet
from config import TARGET_URL, LOGIN_ID, LOGIN_PASSWORD

TARGET_YEAR = 2026
TARGET_MONTH = 2
TARGET_DAYS = list(range(1, 29))  # 2월 1일 ~ 28일


def format_date(year: int, month: int, day: int) -> str:
    return f"{year}-{month:02d}-{day:02d}"


def navigate_calendar_to_month(page, target_month_label: str):
    """
    달력 헤더를 확인하고 목표 월이 될 때까지 이동합니다.
    target_month_label: 달력 헤더에 표시되는 텍스트 (예: "January 2026")
    """
    header_selector = "div.MuiPickersCalendarHeader-label"
    prev_selector = 'button[aria-label="Previous month"]'
    next_selector = 'button[aria-label="Next month"]'

    for _ in range(12):
        header_text = page.locator(header_selector).inner_text(timeout=5000)
        if target_month_label in header_text:
            return
        # 목표가 과거 월이면 Previous, 미래면 Next
        page.locator(prev_selector).click()
        page.wait_for_timeout(500)


def click_calendar_date_january(page, day: str):
    """달력에서 1월의 특정 날짜를 클릭하고 OK 버튼을 누릅니다."""
    navigate_calendar_to_month(page, "February 2026")

    date_selector = page.locator(f"button.MuiPickersDay-root:text-is('{day}')")
    date_selector.wait_for(state="visible", timeout=10000)
    date_selector.click()

    ok_button = page.get_by_role("button", name="OK", exact=True)
    ok_button.wait_for(state="visible", timeout=5000)
    ok_button.click()


def main():
    print("=" * 50)
    print("Ktourstory 예약 정보 크롤링 (2월 1일 ~ 28일)")
    print("=" * 50)

    # 1. Playwright 자체 Chromium으로 브라우저 실행
    print("\n[1/4] 브라우저 실행 중...")
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    print("[OK] 브라우저 실행 완료")

    all_scraped_data = []

    try:
        # 2. 로그인
        print("\n[2/4] 로그인 중...")
        page.goto(TARGET_URL)
        login(page, LOGIN_ID, LOGIN_PASSWORD)
        page.wait_for_timeout(1000)
        print("[OK] 로그인 완료")

        # 3. 날짜별 스크래핑
        print(f"\n[3/4] {TARGET_MONTH}월 날짜별 예약 조회 중... (총 {len(TARGET_DAYS)}일)")
        for idx, day in enumerate(TARGET_DAYS, 1):
            reservation_date = format_date(TARGET_YEAR, TARGET_MONTH, day)
            print(f"\n  [{idx}/{len(TARGET_DAYS)}] {reservation_date} 조회 중...")

            click_date_button(page)
            page.wait_for_timeout(500)
            click_calendar_date_january(page, str(day))
            page.wait_for_timeout(500)

            if not has_reservations(page, timeout=3000):
                print(f"  [{idx}/{len(TARGET_DAYS)}] {reservation_date}: 예약 없음")
                continue

            click_reservation_text(page)
            page.wait_for_timeout(500)

            team_count = get_team_count(page)
            scraped_data = []
            for team_idx in range(team_count):
                click_team_button(page, team_idx)
                page.wait_for_timeout(500)
                team_data = scrape_details(page, reservation_date, team_idx)
                scraped_data.extend(team_data)
                click_team_button(page, team_idx)
                page.wait_for_timeout(500)

            all_scraped_data.extend(scraped_data)
            print(f"  [{idx}/{len(TARGET_DAYS)}] {reservation_date}: {len(scraped_data)}건 수집 ({team_count}팀)")

        print(f"\n[4/4] 전체 스크래핑 완료 (총 {len(all_scraped_data)}건)")

        # 4. Google Sheets에 저장 + 취소 감지
        crawled_dates = [format_date(TARGET_YEAR, TARGET_MONTH, d) for d in TARGET_DAYS]
        if all_scraped_data or crawled_dates:
            print("\nGoogle Sheets에 데이터 저장 중...")
            new_reservations, existing_reservations, cancelled_reservations = save_to_sheet(
                all_scraped_data, crawled_dates=crawled_dates
            )
            print(f"새로 추가: {len(new_reservations)}건, 기존(중복): {len(existing_reservations)}건, 취소: {len(cancelled_reservations)}건")
        else:
            print("\n저장할 데이터가 없습니다.")

        print("\n" + "=" * 50)
        print(f"{TARGET_MONTH}월 크롤링 완료!")
        print(f"총 {len(all_scraped_data)}건 수집")
        print("=" * 50)

    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        raise

    finally:
        print("\n브라우저 종료 중...")
        try:
            context.close()
            browser.close()
            pw.stop()
        except Exception:
            pass
        print("[OK] 브라우저 종료 완료")


if __name__ == "__main__":
    main()
