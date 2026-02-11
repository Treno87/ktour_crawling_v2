from unittest.mock import MagicMock
from browser_controller import get_cdp_port


def test_get_cdp_port_extracts_port_from_driver_capabilities():
    """driver capabilities에서 CDP 포트를 정확히 추출한다."""
    mock_driver = MagicMock()
    mock_driver.capabilities = {
        "goog:chromeOptions": {
            "debuggerAddress": "127.0.0.1:51234"
        }
    }

    port = get_cdp_port(mock_driver)

    assert port == "51234"


def test_get_cdp_port_raises_when_no_debugger_address():
    """debuggerAddress가 없으면 RuntimeError를 발생시킨다."""
    mock_driver = MagicMock()
    mock_driver.capabilities = {}

    try:
        get_cdp_port(mock_driver)
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
