==================================================
Ktourstory 예약 정보 크롤링 시작
==================================================
검색 대상: 1월 18일 ~ 31일 (14일간)

[1/6] 브라우저 실행 중...
(node:5170) [DEP0169] DeprecationWarning: `url.parse()` behavior is not standardized and prone to errors that have security implications. Use the WHATWG URL API instead. CVEs are not issued for `url.parse()` vulnerabilities.
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
File "/home/runner/work/ktour_crawling_v2/ktour_crawling_v2/gsheets_client.py", line 43, in save_to_sheet
gc = get_gspread_client()
File "/home/runner/work/ktour_crawling_v2/ktour_crawling_v2/gsheets_client.py", line 21, in get_gspread_client
creds_dict = json.loads(creds_json)
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

# github ai's solution

The job failed due to a JSONDecodeError: "Invalid control character at: line 5 column 69 (char 267)" in your code when saving data to Google Sheets. This means some value being serialized to JSON contains illegal control characters (such as raw newlines, carriage returns, or other non-printable characters).

**How to Fix:**

1. **Sanitize Your JSON Input**
   - Before dumping or loading data with `json`, make sure to clean or escape unwanted control characters from your data. Often, this is done by replacing or removing characters below ASCII 32 except whitespace.

2. **Example Code Correction**
   If your code uses something like:

   ```python
   import json
   json.loads(data)
   ```

   or

   ```python
   json.dumps(data)
   ```

   clean your data as shown below:

   ```python
   import re

   def sanitize_string(s):
       # Remove control characters except for whitespace
       return re.sub(r'[\x00-\x1f\x7f]', '', s)

   sanitized_data = {k: sanitize_string(v) if isinstance(v, str) else v for k,v in data.items()}
   json_str = json.dumps(sanitized_data)
   ```

3. **Where to Place This**
   - Insert sanitization right before your code saves to Google Sheets or serializes to JSON.

4. **Review Input Source**
   - Check the data being scraped—one or more entries has a raw control character. Use the above technique to clean each string in your dataset before processing.

**Direct Next Steps:**

- Clean your data as shown.
- Rerun the workflow to verify the fix.

If you need the exact code location, please mention the file used for Google Sheets writing or pasting the related snippet, and I can assist you directly in updating it.

**Related error line reference:**  
You can see the full error in your workflow logs for commit [`9b74e59`](https://github.com/Treno87/ktour_crawling_v2/blob/9b74e59c1317f974c67fda5377a99be38d5172b8), specifically the stack trace points to standard library's `json/decoder.py`.  
Focus your changes on the part of your project just before serializing to JSON.
