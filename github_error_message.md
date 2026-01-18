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
