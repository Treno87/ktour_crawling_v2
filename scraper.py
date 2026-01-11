from datetime import datetime
from playwright.sync_api import Page
import time
import json
import re
from config import PRICE_FILE


def retry_action(action, max_retries: int = 3, delay: float = 1.0):
    """
    액션을 재시도하는 래퍼 함수.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return action()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(delay)
    raise last_error


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

    page.locator(date_button_selector).wait_for(state="visible", timeout=15000)
    page.locator(date_button_selector).click()


def click_calendar_date(page: Page, day: str):
    """
    달력에서 특정 날짜를 클릭하고 'OK' 버튼을 누릅니다.
    """
    date_selector = page.locator(f"button.MuiPickersDay-root:text-is('{day}')")
    date_selector.wait_for(state="visible", timeout=10000)
    date_selector.click()

    ok_button_selector = page.get_by_role("button", name="OK", exact=True)
    ok_button_selector.wait_for(state="visible", timeout=5000)
    ok_button_selector.click()


def has_reservations(page: Page, timeout: int = 15000) -> bool:
    """
    현재 페이지에 예약이 있는지 확인합니다.
    상호(마리엠헤어)가 있으면 예약 있음.
    """
    store_selector = "div.MuiAccordionSummary-content h6"
    try:
        page.locator(store_selector).wait_for(state="visible", timeout=timeout)
        return True
    except Exception:
        return False


def click_reservation_text(page: Page):
    """
    상호(마리엠헤어) 텍스트를 클릭합니다.
    """
    store_selector = "div.MuiAccordionSummary-content h6"

    def action():
        page.locator(store_selector).wait_for(state="visible", timeout=15000)
        page.locator(store_selector).click()

    retry_action(action)


def click_team_button(page: Page):
    """
    첫 번째 팀의 펼치기 버튼을 클릭합니다.
    """
    team_expand_selector = '//ul/li[contains(@class, "MuiListSubheader-root")]//button[contains(@class, "MuiIconButton-root")]'

    def action():
        page.locator(team_expand_selector).first.wait_for(state="visible", timeout=10000)
        page.locator(team_expand_selector).first.click()

    retry_action(action)


def login(page: Page, email: str, password: str):
    """
    제공된 이메일과 비밀번호로 로그인합니다.
    """
    login_icon_selector = 'button[aria-label="log in"]'
    page.locator(login_icon_selector).wait_for(state="visible", timeout=15000)
    page.locator(login_icon_selector).click()

    email_selector = "input#email"
    password_selector = "input#password"

    page.locator(email_selector).wait_for(state="visible", timeout=10000)
    page.locator(email_selector).fill(email)
    page.locator(password_selector).fill(password)

    page.evaluate("document.querySelector('button[type=\"submit\"]').click()")

    user_menu_button_selector = "button.MuiIconButton-edgeEnd"
    page.locator(user_menu_button_selector).wait_for(state="visible", timeout=15000)


def get_team_name(page: Page) -> str:
    """
    현재 열린 팀의 이름을 가져옵니다.
    """
    team_header_selector = "li.MuiListSubheader-root"
    try:
        return page.locator(team_header_selector).first.inner_text(timeout=5000)
    except Exception:
        return ""


def scrape_details(page: Page, reservation_date: str) -> list[dict]:
    """
    예약 상세 정보 페이지에서 모든 예약 내역을 스크래핑하여 딕셔너리 리스트로 반환합니다.

    Args:
        page: Playwright Page 객체
        reservation_date: 예약 날짜 (예: "2026-01-14")
    """
    details_container_selector = "li.css-jywvn2"
    page.wait_for_selector(details_container_selector, state="visible", timeout=10000)

    # 팀 이름 가져오기
    team_name = get_team_name(page)

    # 가격 데이터 로드
    price_data = load_price_data()

    reservations = page.locator(details_container_selector).all()
    scraped_data = []

    for res in reservations:
        try:
            # 고객명
            name = res.locator("h6.css-qdk4z1").inner_text(timeout=3000)

            # 예약번호
            reservation_no = res.locator("h6.css-1r042ka").inner_text(timeout=3000)

            # 국가
            nationality = res.locator("span.css-xcju41").inner_text(timeout=3000)

            # 예약시간
            time_text = res.locator("p.css-17exa0r").inner_text(timeout=3000)
            reservation_time = time_text.replace("Time Request:", "").strip()

            # 예약상품
            product_name = res.locator("p.css-1q5lgor").inner_text(timeout=3000)

            # 채널 (MuiAvatar에서 추출 - L, VI 등)
            channel = res.locator("div.MuiAvatar-root").inner_text(timeout=3000)

            # 인원구분 (p.css-mdkayp에서 추출)
            person_info = res.locator("p.css-mdkayp").inner_text(timeout=3000)

            # 금액 계산
            price = calculate_price(product_name, price_data)

            scraped_data.append({
                "날짜": reservation_date,
                "팀": team_name,
                "고객명": name,
                "예약번호": reservation_no,
                "채널": channel,
                "인원구분": person_info,
                "국가": nationality,
                "예약상품": product_name,
                "예약시간": reservation_time,
                "금액": price,
                "is_new": ""
            })
        except Exception as e:
            print(f"예약 정보 추출 실패: {e}")
            continue

    return scraped_data


def extract_person_count(name: str) -> str:
    """
    고객명에서 인원수를 추출합니다.
    예: "Zhang Qingrong (1)" -> "1"
    """
    match = re.search(r'\((\d+)\)', name)
    if match:
        return match.group(1)
    return ""


def load_price_data() -> dict:
    """
    price.json에서 가격 데이터를 로드합니다.
    """
    try:
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"가격 데이터 로드 실패: {e}")
        return {}


def calculate_price(product_name: str, price_data: dict) -> str:
    """
    상품명에서 가격을 계산합니다.
    예: "AB: PERSONAL STYLE CONSULTING + CUT + STYLING X 1" -> "110,000"
    """
    # 상품명에서 순수 상품명 추출 (AB: 제거, X 숫자 제거)
    clean_name = product_name

    # "AB: " 같은 접두어 제거
    if ": " in clean_name:
        clean_name = clean_name.split(": ", 1)[1]

    # " X 숫자" 부분에서 수량 추출 및 제거
    quantity = 1
    quantity_match = re.search(r'\s*X\s*(\d+)\s*$', clean_name, re.IGNORECASE)
    if quantity_match:
        quantity = int(quantity_match.group(1))
        clean_name = re.sub(r'\s*X\s*\d+\s*$', '', clean_name, flags=re.IGNORECASE)

    clean_name = clean_name.strip()

    # 가격 찾기
    unit_price = price_data.get(clean_name, price_data.get("DEFAULT", 0))
    total_price = unit_price * quantity

    # 천 단위 콤마 포맷
    return f"{total_price:,}"
