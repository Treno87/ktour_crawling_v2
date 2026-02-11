"""
Tests for get_date_range_for_month: should return 1st to last day of month.
"""
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))


def test_date_range_starts_from_day_1():
    """get_date_range_for_month should always start from day 1, not today"""
    with patch('main.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2026, 2, 15, tzinfo=KST)
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        from main import get_date_range_for_month
        # Force reimport to pick up patched datetime
        import importlib
        import main
        importlib.reload(main)

        result = main.get_date_range_for_month()
        assert result[0] == "1", f"Expected '1' but got '{result[0]}'"


def test_date_range_ends_at_last_day():
    """get_date_range_for_month should end at the last day of the month"""
    with patch('main.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2026, 2, 15, tzinfo=KST)
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        import importlib
        import main
        importlib.reload(main)

        result = main.get_date_range_for_month()
        assert result[-1] == "28", f"Expected '28' but got '{result[-1]}'"


def test_date_range_covers_full_month():
    """get_date_range_for_month should return all days of the month"""
    with patch('main.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2026, 2, 15, tzinfo=KST)
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        import importlib
        import main
        importlib.reload(main)

        result = main.get_date_range_for_month()
        assert len(result) == 28
        assert result == [str(d) for d in range(1, 29)]
