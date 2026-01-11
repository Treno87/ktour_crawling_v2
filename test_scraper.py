import pytest
from playwright.sync_api import Page, BrowserContext
from browser_controller import setup_browser
from config import TARGET_URL, LOGIN_ID, LOGIN_PASSWORD
from scraper import (
    close_login_dialog,
    click_date_button,
    click_calendar_date,
    click_reservation_text,
    click_team_button,
    login,
    scrape_details,
)

# --- Fixture definitions (copied from conftest.py) ---
@pytest.fixture(scope="session")
def browser_context():
    """
    테스트 세션 전체에서 한 번만 브라우저와 컨텍스트를 설정합니다.
    """
    _page, browser, context = setup_browser()
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(browser_context: BrowserContext):
    """
    각 테스트 함수를 위해 새로운, 깨끗한 페이지를 제공합니다.
    """
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    """
    인증이 필요한 테스트를 위해 로그인된 페이지를 제공합니다.
    """
    page.goto(TARGET_URL)
    login(page, LOGIN_ID, LOGIN_PASSWORD)
    yield page
# --- End Fixture definitions ---


def test_scraper_can_open_calendar(page: Page):
    """
    TARGET_URL로 이동 후 로그인 다이얼로그를 닫고,
    날짜 버튼을 클릭하여 달력이 열리는지 확인하는 테스트.
    """
    page.goto(TARGET_URL)
    close_login_dialog(page)
    click_date_button(page)
    calendar_selector = "div.MuiCalendarPicker-root"
    page.wait_for_selector(calendar_selector, state="visible", timeout=5000)
    calendar = page.locator(calendar_selector)
    assert calendar.is_visible()

def test_scraper_login_and_find_reservation(logged_in_page: Page):
    """
    로그인 후 달력을 열고, 특정 날짜(14일)를 클릭하여 '마리엠헤어' 텍스트가 나타나는지 확인합니다.
    """
    page = logged_in_page
    click_date_button(page)
    click_calendar_date(page, "14")
    reservation_text_selector = 'text="마리엠헤어"'
    page.wait_for_selector(reservation_text_selector, state="visible", timeout=10000)
    reservation_text = page.locator(reservation_text_selector).first
    assert reservation_text.is_visible()

def test_click_reservation_and_team_to_see_details(logged_in_page: Page):
    """
    예약 텍스트('마리엠헤어')와 'TEAM' 버튼을 클릭하여 최종 예약 내역이 보이는지 확인합니다.
    """
    page = logged_in_page
    click_date_button(page)
    click_calendar_date(page, "14")
    click_reservation_text(page)
    click_team_button(page)
    details_container_selector = "li.css-jywvn2"
    page.wait_for_selector(details_container_selector, state="visible", timeout=5000)
    details_container = page.locator(details_container_selector).first
    assert details_container.is_visible()

def test_scrape_reservation_details(logged_in_page: Page):
    """
    최종 예약 내역 페이지에서 상세 정보를 스크래핑합니다.
    """
    page = logged_in_page
    click_date_button(page)
    click_calendar_date(page, "14")
    click_reservation_text(page)
    click_team_button(page)

    # 데이터 스크래핑 함수 호출
    scraped_data = scrape_details(page)

    # 결과 확인
    assert scraped_data is not None
    assert isinstance(scraped_data, list)
    assert len(scraped_data) > 0

    first_reservation = scraped_data[0]
    assert "이름" in first_reservation
    assert "상품명" in first_reservation
    assert "예약시간" in first_reservation
    assert "예약번호" in first_reservation
    assert "국적" in first_reservation

    # 간단한 데이터 값 검증
    assert first_reservation["이름"] == "Zhang Qingrong (1)"
