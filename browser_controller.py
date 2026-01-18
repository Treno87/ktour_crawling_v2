"""
브라우저 컨트롤러 모듈
SeleniumBase의 uc 모드로 브라우저를 실행하고,
Playwright가 해당 브라우저에 접속하여 제어합니다.
"""
from seleniumbase import Driver
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import time
import subprocess
import re
import os
import platform


def is_headless_mode() -> bool:
    """환경변수로 headless 모드 여부 확인"""
    return os.getenv("HEADLESS", "").lower() in ("true", "1", "yes")


def get_cdp_port() -> str:
    """Chrome 프로세스에서 디버깅 포트 추출"""
    cdp_port = None
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.run(
                ['wmic', 'process', 'where', "name='chrome.exe'", 'get', 'commandline'],
                capture_output=True,
                text=True,
                encoding='cp949'
            )
        else:
            # Linux/Mac
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )

        for line in result.stdout.split('\n'):
            match = re.search(r'--remote-debugging-port=(\d+)', line)
            if match:
                cdp_port = match.group(1)
                break
    except Exception as e:
        print(f"Warning: Could not detect CDP port automatically: {e}")

    return cdp_port or "9222"


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
    driver = Driver(uc=True, headless=headless)
    driver.get("about:blank")

    # 2. Playwright가 디버깅 포트로 연결할 수 있도록 대기
    time.sleep(3)

    # 3. Chrome 프로세스에서 디버깅 포트 추출
    cdp_port = get_cdp_port()

    # 4. Playwright를 통해 실행 중인 브라우저에 연결
    playwright = sync_playwright().start()

    ws_endpoint = f"http://127.0.0.1:{cdp_port}"
    browser = playwright.chromium.connect_over_cdp(ws_endpoint)

    # 기존 컨텍스트와 페이지 사용
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()

    return page, browser, context, driver
