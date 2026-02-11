from scraper import calculate_price


def test_calculate_price_returns_formatted_price():
    """가격 데이터에서 정확한 금액을 반환한다."""
    price_data = {"PERSONAL STYLE CONSULTING + CUT + STYLING": 110000}
    result = calculate_price("AB: PERSONAL STYLE CONSULTING + CUT + STYLING X 2", price_data)
    assert result == "220,000"


def test_calculate_price_warns_on_unknown_product(capsys):
    """알 수 없는 상품이면 경고를 출력한다."""
    price_data = {"KNOWN PRODUCT": 50000}
    result = calculate_price("AB: UNKNOWN PRODUCT X 1", price_data)

    captured = capsys.readouterr()
    assert "UNKNOWN PRODUCT" in captured.out
    assert result == "0"
