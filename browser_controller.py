"""
브라우저 컨트롤러 모듈
SeleniumBase의 uc 모드로 브라우저를 실행하고,
Playwright가 해당 브라우저에 접속하여 제어합니다.
"""
from seleniumbase import Driver
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import time
import os
import tempfile


def is_headless_mode() -> bool:
    """환경변수로 headless 모드 여부 확인"""
    return os.getenv("HEADLESS", "").lower() in ("true", "1", "yes")


def get_cdp_port(driver) -> str:
    """Driver capabilities에서 CDP 디버깅 포트를 추출합니다."""
    debugger_address = driver.capabilities.get(
        "goog:chromeOptions", {}
    ).get("debuggerAddress", "")

    if debugger_address:
        port = debugger_address.split(":")[-1]
        print(f"  CDP port detected: {port}")
        return port

    raise RuntimeError("Cannot detect CDP debugger port from driver capabilities")


def setup_browser() -> tuple[Page, Browser, BrowserContext, "Driver"]:
    """
    SeleniumBase(uc=True)로 브라우저를 실행하고,
    Playwright가 해당 브라우저에 연결하여 제어합니다.

    환경변수:
        HEADLESS: "true"로 설정하면 headless 모드로 실행

    Returns:
        tuple[Page, Browser, BrowserContext, Driver]: Playwright Page, Browser, Context, SeleniumBase Driver 객체
    """
    headless = is_headless_mode()

    # 1. SeleniumBase로 브라우저 실행 (uc=True로 봇 탐지 우회)
    # 별도 프로필 + 별도 포트 사용 → 기존 Chrome과 충돌 방지
    user_data_dir = os.path.join(tempfile.gettempdir(), "crawl_chrome_profile")
    driver = Driver(
        uc=True,
        headless=headless,
        user_data_dir=user_data_dir,
        chromium_arg="--remote-debugging-port=9242",
    )
    driver.get("about:blank")
    time.sleep(2)

    # 2. Driver capabilities에서 CDP 포트 추출
    cdp_port = get_cdp_port(driver)

    # 3. Playwright를 통해 실행 중인 브라우저에 연결 (재시도 포함)
    playwright = sync_playwright().start()
    ws_endpoint = f"http://127.0.0.1:{cdp_port}"

    last_error = None
    for attempt in range(3):
        try:
            browser = playwright.chromium.connect_over_cdp(ws_endpoint)
            break
        except Exception as e:
            last_error = e
            print(f"  Playwright connection attempt {attempt + 1}/3 failed, retrying...")
            time.sleep(2)
    else:
        raise RuntimeError(f"Failed to connect Playwright to CDP: {last_error}")

    # 기존 컨텍스트와 페이지 사용
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()

    return page, browser, context, driver
