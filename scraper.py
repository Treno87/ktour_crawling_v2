from datetime import datetime
from playwright.sync_api import Page


def close_login_dialog(page: Page):
    """
    페이지에 로그인 다이얼로그가 있다면 닫습니다.
    """
    backdrop_selector = "div.MuiBackdrop-root.MuiModal-backdrop"

    try:
        page.locator(backdrop_selector).click(timeout=1000)
        page.wait_for_selector(backdrop_selector, state="hidden", timeout=5000)
    except Exception:
        pass


def click_date_button(page: Page):
    """
    페이지 상단의 날짜 버튼을 클릭하여 달력을 엽니다.
    """
    date_button_selector = "button.MuiButtonBase-root.css-ab6e07"

    page.locator(date_button_selector).wait_for(state="visible", timeout=10000)
    page.locator(date_button_selector).click()


def click_calendar_date(page: Page, day: str):
    """
    달력에서 특정 날짜를 클릭하고 'OK' 버튼을 누릅니다.
    """
    date_selector = page.get_by_role("gridcell", name=day, exact=True)
    date_selector.wait_for(state="visible", timeout=5000)
    date_selector.click()

    ok_button_selector = page.get_by_role("button", name="OK", exact=True)
    ok_button_selector.wait_for(state="visible", timeout=5000)
    ok_button_selector.click()


def has_reservations(page: Page) -> bool:
    """
    현재 페이지에 예약이 있는지 확인합니다.
    """
    reservation_item_selector = "div.MuiPaper-root"
    try:
        page.locator(reservation_item_selector).first.wait_for(state="visible", timeout=3000)
        return True
    except Exception:
        return False


def click_reservation_text(page: Page):
    """
    '마리엠헤어' 텍스트를 클릭합니다.
    """
    reservation_text_selector = 'text="마리엠헤어"'
    page.locator(reservation_text_selector).wait_for(state="visible", timeout=10000)
    page.locator(reservation_text_selector).first.click()


def click_team_button(page: Page):
    """
    'TEAM' 버튼을 클릭합니다.
    """
    team_button_selector = 'div.MuiChip-root:has-text("TEAM")'
    page.locator(team_button_selector).wait_for(state="visible", timeout=5000)
    page.locator(team_button_selector).first.click()


def login(page: Page, email: str, password: str):
    """
    제공된 이메일과 비밀번호로 로그인합니다.
    """
    login_icon_selector = 'button[aria-label="log in"]'
    page.locator(login_icon_selector).wait_for(state="visible", timeout=10000)
    page.locator(login_icon_selector).click()

    email_selector = "input#email"
    password_selector = "input#password"

    page.locator(email_selector).wait_for(state="visible", timeout=5000)
    page.locator(email_selector).fill(email)
    page.locator(password_selector).fill(password)

    page.evaluate("document.querySelector('button[type=\"submit\"]').click()")

    user_menu_button_selector = "button.MuiIconButton-edgeEnd"
    page.locator(user_menu_button_selector).wait_for(state="visible", timeout=10000)


def scrape_details(page: Page) -> list[dict]:
    """
    예약 상세 정보 페이지에서 모든 예약 내역을 스크래핑하여 딕셔너리 리스트로 반환합니다.
    """
    details_container_selector = "li.css-jywvn2"
    page.wait_for_selector(details_container_selector, state="visible", timeout=5000)

    reservations = page.locator(details_container_selector).all()
    scraped_data = []

    for res in reservations:
        name = res.locator("h6.css-qdk4z1").inner_text()
        reservation_no = res.locator("h6.css-1r042ka").inner_text()
        nationality = res.locator("span.css-xcju41").inner_text()

        time_text = res.locator("p.css-17exa0r").inner_text()
        reservation_time = time_text.replace("Time Request:", "").strip()

        product_name = res.locator("p.css-1q5lgor").inner_text()

        scraped_data.append({
            "이름": name,
            "상품명": product_name,
            "예약시간": reservation_time,
            "예약번호": reservation_no,
            "국적": nationality,
            "크롤링 일자": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return scraped_data
