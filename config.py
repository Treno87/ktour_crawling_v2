"""
프로젝트 설정 파일
환경 변수를 로드하고 전역 설정값을 정의합니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# 로그인 정보
LOGIN_ID = os.getenv("LOGIN_ID", "")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "")

# 타겟 URL
TARGET_URL = os.getenv("TARGET_URL", "https://guide.ktourstory.com/")

# Google Sheets 설정
GOOGLE_SHEET_TITLE = os.getenv("GOOGLE_SHEET_TITLE", "케이투어_관광객예약리스트")
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "crawlingDB")

# Google Sheets 인증 파일 경로
CREDENTIALS_FILE = str(Path(__file__).parent / "credentials.json")

# 예약 데이터 헤더 (구글 시트 컬럼명 - 기존 시트와 동일)
RESERVATION_DATA_HEADERS = [
    "날짜",
    "팀",
    "고객명",
    "예약번호",
    "채널",
    "인원구분",
    "국가",
    "예약상품",
    "예약시간",
    "금액",
    "is_new"
]

# 가격 데이터 파일 경로
PRICE_FILE = str(Path(__file__).parent / "price.json")

# Slack 설정
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Google Sheets URL (시트 바로가기용)
GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL", "")
