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
GOOGLE_SHEET_TITLE = os.getenv("GOOGLE_SHEET_TITLE", "Ktourstory_Reservations")
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Sheet1")

# Google Sheets 인증 파일 경로
CREDENTIALS_FILE = str(Path(__file__).parent / "credentials.json")

# 예약 데이터 헤더 (구글 시트 컬럼명)
RESERVATION_DATA_HEADERS = [
    "이름",
    "상품명",
    "예약시간",
    "예약번호",
    "국적",
    "크롤링 일자"
]
