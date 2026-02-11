"""
Cancellation detection unit tests.
Tests for save_to_sheet with crawled_dates parameter.
"""
import pytest
from unittest.mock import patch, MagicMock, call
from gsheets_client import save_to_sheet
from config import RESERVATION_DATA_HEADERS


class TestCancellationDetection:
    """save_to_sheet의 취소 감지 기능 테스트"""

    def _make_sheet_row(self, date, team, name, reservation_no, channel,
                        people, country, product, time, price, is_new, status=""):
        """시트 행 데이터를 생성하는 헬퍼"""
        row = [date, team, name, reservation_no, channel,
               people, country, product, time, price, is_new]
        if status:
            row.append(status)
        return row

    def _make_reservation(self, reservation_no, date="2026-02-15", price="50,000"):
        """예약 딕셔너리를 생성하는 헬퍼"""
        return {
            "날짜": date,
            "팀": "TEAM 1",
            "고객명": "Test User",
            "예약번호": reservation_no,
            "채널": "L",
            "인원구분": "Adult 1",
            "국가": "KOREA",
            "예약상품": "Test Product",
            "예약시간": "10:00",
            "금액": price,
            "is_new": ""
        }

    @patch('gsheets_client.get_gspread_client')
    def test_returns_three_tuple(self, mock_gc):
        """save_to_sheet는 (new, existing, cancelled) 3-tuple을 반환해야 한다"""
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        data = [self._make_reservation("RES-001")]
        result = save_to_sheet(data, crawled_dates=["2026-02-15"])

        assert len(result) == 3
        new, existing, cancelled = result
        assert isinstance(new, list)
        assert isinstance(existing, list)
        assert isinstance(cancelled, list)

    @patch('gsheets_client.get_gspread_client')
    def test_returns_three_tuple_without_crawled_dates(self, mock_gc):
        """crawled_dates 없이도 3-tuple을 반환해야 한다"""
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        data = [self._make_reservation("RES-001")]
        result = save_to_sheet(data)

        assert len(result) == 3
        _, _, cancelled = result
        assert cancelled == []

    @patch('gsheets_client.get_gspread_client')
    def test_detects_cancelled_reservation(self, mock_gc):
        """크롤링 데이터에 없는 기존 예약을 취소로 감지해야 한다"""
        existing_row = self._make_sheet_row(
            "2026-02-15", "TEAM 1", "Old User", "RES-OLD", "L",
            "Adult 1", "KOREA", "Old Product", "09:00", "30000", ""
        )
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        # RES-OLD는 크롤링 데이터에 없음 → 취소 대상
        data = [self._make_reservation("RES-NEW", date="2026-02-15")]
        _, _, cancelled = save_to_sheet(data, crawled_dates=["2026-02-15"])

        assert len(cancelled) == 1
        assert cancelled[0]["예약번호"] == "RES-OLD"

    @patch('gsheets_client.get_gspread_client')
    def test_skips_already_cancelled(self, mock_gc):
        """이미 취소 상태인 예약은 다시 취소 처리하지 않아야 한다"""
        existing_row = self._make_sheet_row(
            "2026-02-15", "TEAM 1", "Old User", "RES-OLD", "L",
            "Adult 1", "KOREA", "Old Product", "09:00", "0", "", "취소"
        )
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        data = [self._make_reservation("RES-NEW", date="2026-02-15")]
        _, _, cancelled = save_to_sheet(data, crawled_dates=["2026-02-15"])

        assert len(cancelled) == 0

    @patch('gsheets_client.get_gspread_client')
    def test_skips_dates_not_in_crawled_dates(self, mock_gc):
        """crawled_dates에 포함되지 않은 날짜의 예약은 취소로 감지하지 않아야 한다"""
        existing_row = self._make_sheet_row(
            "2026-02-20", "TEAM 1", "Other User", "RES-OTHER", "L",
            "Adult 1", "KOREA", "Other Product", "09:00", "30000", ""
        )
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        # crawled_dates에 2026-02-20이 없음 → 취소 대상 아님
        data = [self._make_reservation("RES-NEW", date="2026-02-15")]
        _, _, cancelled = save_to_sheet(data, crawled_dates=["2026-02-15"])

        assert len(cancelled) == 0

    @patch('gsheets_client.get_gspread_client')
    def test_cancelled_reservation_updates_sheet(self, mock_gc):
        """취소된 예약은 시트에서 상태='취소', 금액=0으로 업데이트해야 한다"""
        existing_row = self._make_sheet_row(
            "2026-02-15", "TEAM 1", "Old User", "RES-OLD", "L",
            "Adult 1", "KOREA", "Old Product", "09:00", "30000", ""
        )
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        data = [self._make_reservation("RES-NEW", date="2026-02-15")]
        save_to_sheet(data, crawled_dates=["2026-02-15"])

        # 상태 컬럼(L열)에 "취소" 기록 확인
        status_col_idx = RESERVATION_DATA_HEADERS.index("상태") + 1  # 1-based
        price_col_idx = RESERVATION_DATA_HEADERS.index("금액") + 1  # 1-based
        row_num = 2  # header + 1

        # batch_update or update calls should include status and price updates
        worksheet.update_cell.assert_any_call(row_num, status_col_idx, "취소")
        worksheet.update_cell.assert_any_call(row_num, price_col_idx, 0)

    @patch('gsheets_client.get_gspread_client')
    def test_cancelled_reservation_gets_formatting(self, mock_gc):
        """취소된 예약 행에 취소선 + 빨간 배경 포맷팅이 적용되어야 한다"""
        existing_row = self._make_sheet_row(
            "2026-02-15", "TEAM 1", "Old User", "RES-OLD", "L",
            "Adult 1", "KOREA", "Old Product", "09:00", "30000", ""
        )
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        data = [self._make_reservation("RES-NEW", date="2026-02-15")]
        save_to_sheet(data, crawled_dates=["2026-02-15"])

        # format_cell_range or batch format should be called
        worksheet.format.assert_called()
        format_call = worksheet.format.call_args
        format_dict = format_call[0][1] if len(format_call[0]) > 1 else format_call[1].get('cell_format', {})

        # Check strikethrough
        assert format_dict.get("textFormat", {}).get("strikethrough") is True
        # Check red background
        bg = format_dict.get("backgroundColor", {})
        assert bg.get("red", 0) > 0.9


class TestStatusHeaderInConfig:
    """config.py의 RESERVATION_DATA_HEADERS에 '상태' 컬럼이 있어야 한다"""

    def test_headers_contain_status_column(self):
        assert "상태" in RESERVATION_DATA_HEADERS

    def test_status_column_is_last(self):
        assert RESERVATION_DATA_HEADERS[-1] == "상태"


class TestEmptyDataWithCrawledDates:
    """빈 데이터로 호출 시에도 취소 감지가 동작해야 한다"""

    @patch('gsheets_client.get_gspread_client')
    def test_empty_data_still_detects_cancellations(self, mock_gc):
        """data가 빈 리스트여도 crawled_dates가 있으면 취소 감지 수행"""
        existing_row = [
            "2026-02-15", "TEAM 1", "Old User", "RES-OLD", "L",
            "Adult 1", "KOREA", "Old Product", "09:00", "30000", ""
        ]
        worksheet = MagicMock()
        worksheet.get_all_values.return_value = [RESERVATION_DATA_HEADERS, existing_row]
        mock_gc.return_value.open.return_value.worksheet.return_value = worksheet

        new, existing, cancelled = save_to_sheet([], crawled_dates=["2026-02-15"])

        assert len(cancelled) == 1
        assert cancelled[0]["예약번호"] == "RES-OLD"
        assert new == []
        assert existing == []
