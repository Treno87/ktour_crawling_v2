==================================================
Ktourstory 예약 정보 크롤링 시작
==================================================
검색 대상: 1월 18일 ~ 31일 (14일간)

[1/6] 브라우저 실행 중...
(node:5103) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
(Use `node --trace-deprecation ...` to show where the warning was created)
[OK] 브라우저 실행 완료

[2/6] 로그인 중...
[OK] 로그인 완료

[3/6] 날짜별 예약 조회 중... (총 14일)

[1/14] 2026-01-18 조회 중...
[1/14] 2026-01-18: 1건 수집

[2/14] 2026-01-19 조회 중...
[2/14] 2026-01-19: 예약 없음

[3/14] 2026-01-20 조회 중...
[3/14] 2026-01-20: 1건 수집

[4/14] 2026-01-21 조회 중...
[4/14] 2026-01-21: 1건 수집

[5/14] 2026-01-22 조회 중...
[5/14] 2026-01-22: 예약 없음

[6/14] 2026-01-23 조회 중...
[6/14] 2026-01-23: 2건 수집

[7/14] 2026-01-24 조회 중...
[7/14] 2026-01-24: 예약 없음

[8/14] 2026-01-25 조회 중...
[8/14] 2026-01-25: 예약 없음

[9/14] 2026-01-26 조회 중...
[9/14] 2026-01-26: 예약 없음

[10/14] 2026-01-27 조회 중...
[10/14] 2026-01-27: 예약 없음

[11/14] 2026-01-28 조회 중...
[11/14] 2026-01-28: 예약 없음

[12/14] 2026-01-29 조회 중...
[12/14] 2026-01-29: 예약 없음

[13/14] 2026-01-30 조회 중...
[13/14] 2026-01-30: 예약 없음

[14/14] 2026-01-31 조회 중...
[14/14] 2026-01-31: 1건 수집

[4/6] 전체 스크래핑 완료 (총 6건)

[5/6] Google Sheets에 데이터 저장 중...

Error: 오류 발생: Invalid control character at: line 5 column 69 (char 267)
[OK] 슬랙 알림 전송 성공

브라우저 종료 중...
[OK] 브라우저 종료 완료
Traceback (most recent call last):
File "/home/runner/work/ktour_crawling_v2/ktour_crawling_v2/main.py", line 163, in <module>
main()
~~~~^^
File "/home/runner/work/ktour_crawling_v2/ktour_crawling_v2/main.py", line 111, in main
new_reservations, existing_reservations = save_to_sheet(all_scraped_data)
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
File "/home/runner/work/ktour_crawling_v2/ktour_crawling_v2/gsheets_client.py", line 27, in save_to_sheet
gc = gspread.service_account(filename=CREDENTIALS_FILE)
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/site-packages/gspread/auth.py", line 329, in service_account
creds = SACredentials.from_service_account_file(filename, scopes=scopes)
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/site-packages/google/oauth2/service_account.py", line 262, in from_service_account_file
info, signer = \_service_account_info.from_filename(
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
filename, require=["client_email", "token_uri"]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
)
^
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/site-packages/google/auth/\_service_account_info.py", line 79, in from_filename
data = json.load(json_file)
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/json/**init**.py", line 298, in load
return loads(fp.read(),
cls=cls, object_hook=object_hook,
parse_float=parse_float, parse_int=parse_int,
parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, \*\*kw)
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/json/**init**.py", line 352, in loads
return \_default_decoder.decode(s)
~~~~~~~~~~~~~~~~~~~~~~~^^^
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/json/decoder.py", line 345, in decode
obj, end = self.raw_decode(s, idx=\_w(s, 0).end())
~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
File "/opt/hostedtoolcache/Python/3.13.11/x64/lib/python3.13/json/decoder.py", line 361, in raw_decode
obj, end = self.scan_once(s, idx)
~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Invalid control character at: line 5 column 69 (char 267)
Error: Process completed with exit code 1.
