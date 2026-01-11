# Python 웹 크롤링 프로젝트 (SeleniumBase + Playwright + Google Sheets)

## 1. 프로젝트 개요

본 프로젝트는 Python을 사용하여 특정 웹사이트의 데이터를 스크래핑하고, 그 결과를 구글 시트(Google Sheets)에 자동으로 저장하는 것을 목표로 합니다.

특히, `SeleniumBase`의 강력한 봇 탐지 우회 기능(`uc=True` 모드)과 `Playwright`의 안정적인 최신 브라우저 제어 API를 결합하여 데이터 수집의 안정성과 성공률을 높입니다.

## 2. 기술 요구사항

*   **언어**: Python
*   **크롤링**: `SeleniumBase`와 `Playwright`의 하이브리드 방식
    *   `SeleniumBase`의 `Driver(uc=True)` 모드로 브라우저 실행하여 봇 탐지 우회
    *   실행된 브라우저에 `Playwright`가 연결하여 페이지 제어 및 데이터 추출
*   **데이터 저장**: `gspread` 라이브러리를 사용하여 구글 시트에 데이터 저장
*   **실행 환경**: 로컬 Python 환경

## 3. 개발 계획

1.  **환경 설정 및 라이브러리 설치**: Python 가상 환경을 설정하고 `requirements.txt`를 통해 필요한 라이브러리를 설치합니다.
2.  **구글 시트 연동 설정**: `gspread`와 `google-auth`를 사용하여 구글 API 인증을 설정합니다. (사용자 직접 설정 필요)
3.  **하이브리드 브라우저 컨트롤러 구현**: `SeleniumBase`로 브라우저를 열고 `Playwright`가 해당 브라우저에 접속하는 핵심 로직을 구현합니다.
4.  **웹 스크래핑 로직 개발**: `Playwright`를 이용해 지정된 웹사이트의 데이터를 추출하는 함수를 구현합니다. (URL 및 대상 데이터는 추후 지정)
5.  **데이터 저장 로직 개발**: 추출된 데이터를 구글 시트에 쓰는 함수를 구현합니다.
6.  **메인 실행 스크립트 작성**: 모든 로직을 통합하여 전체 크롤링-저장 파이프라인을 실행하는 메인 스크립트를 작성합니다.
7.  **설정 및 문서화**: `config.ini` 또는 `settings.py`와 같은 설정 파일을 추가하고, 프로젝트 사용법을 `README.md`에 상세히 기록합니다.

## 4. 사전 준비 사항

### 4.1. Python 가상 환경 및 라이브러리 설치

```bash
# 1. Python 가상환경 생성 및 활성화
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 2. 필요한 라이브러리 설치 (설치 후 requirements.txt 생성 예정)
pip install seleniumbase playwright gspread
playwright install
```

### 4.2. Google Sheets API 인증 설정

본 프로젝트는 `gspread`를 통해 구글 시트에 접근하므로, Google Cloud Platform(GCP)에서 API 사용 설정 및 인증 정보가 필요합니다.

**1. GCP 프로젝트 생성 및 API 활성화:**

*   [Google Cloud Console](https://console.cloud.google.com/)에 접속하여 새 프로젝트를 생성합니다.
*   해당 프로젝트의 `API 및 서비스` > `라이브러리`로 이동합니다.
*   `Google Drive API`와 `Google Sheets API`를 검색하여 '사용 설정'합니다.

**2. 서비스 계정 생성 및 키 발급:**

*   `API 및 서비스` > `사용자 인증 정보`로 이동합니다.
*   `+ 사용자 인증 정보 만들기` > `서비스 계정`을 선택합니다.
*   서비스 계정의 이름과 설명을 입력하고 '만들기 및 계속'을 클릭합니다.
*   '역할 선택'에서 `편집자(Editor)` 역할을 부여하고 '계속'을 누릅니다.
*   '완료'를 클릭하여 서비스 계정 생성을 마칩니다.
*   생성된 서비스 계정의 이메일 주소를 복사해 둡니다. (다음 단계에서 필요)
*   생성된 서비스 계정을 클릭한 후, `키` 탭으로 이동합니다.
*   `키 추가` > `새 키 만들기`를 선택하고, 키 유형은 `JSON`으로 선택한 후 '만들기'를 클릭합니다.
*   `credentials.json` (또는 다른 이름의) 파일이 자동으로 다운로드됩니다. **이 파일을 프로젝트의 루트 디렉토리에 저장하세요.**

**3. 구글 시트 공유 설정:**

*   데이터를 저장할 구글 시트를 새로 만들거나 기존 시트를 엽니다.
*   오른쪽 상단의 `공유` 버튼을 클릭합니다.
*   위 `2.` 단계에서 복사해 둔 **서비스 계정 이메일 주소**를 추가하고, `편집자` 권한을 부여한 후 '공유'합니다.

---

이제 프로젝트를 진행할 준비가 되었습니다.