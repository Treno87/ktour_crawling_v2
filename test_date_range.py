"""
Tests for get_date_range_for_month: should return today to last day of month.
Past dates are skipped because no new reservations or cancellations occur.
"""
from datetime import datetime, timezone, timedelta
from main import get_date_range_for_month

KST = timezone(timedelta(hours=9))


def test_date_range_starts_from_today():
    """get_date_range_for_month should start from today, not day 1"""
    today = datetime(2026, 2, 15, tzinfo=KST)
    result = get_date_range_for_month(today)
    assert result[0] == "15"


def test_date_range_ends_at_last_day():
    """get_date_range_for_month should end at the last day of the month"""
    today = datetime(2026, 2, 15, tzinfo=KST)
    result = get_date_range_for_month(today)
    assert result[-1] == "28"


def test_date_range_covers_today_to_end():
    """get_date_range_for_month should return today through end of month"""
    today = datetime(2026, 2, 15, tzinfo=KST)
    result = get_date_range_for_month(today)
    assert len(result) == 14
    assert result == [str(d) for d in range(15, 29)]


def test_date_range_on_first_day():
    """On the 1st, should return all days of the month"""
    today = datetime(2026, 2, 1, tzinfo=KST)
    result = get_date_range_for_month(today)
    assert len(result) == 28
    assert result[0] == "1"
    assert result[-1] == "28"


def test_date_range_on_last_day():
    """On the last day, should return only that day"""
    today = datetime(2026, 2, 28, tzinfo=KST)
    result = get_date_range_for_month(today)
    assert result == ["28"]
