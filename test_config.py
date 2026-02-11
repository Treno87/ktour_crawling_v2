import pytest
from unittest.mock import patch


def test_validate_config_raises_when_login_id_missing():
    """LOGIN_ID가 비어있으면 ValueError를 발생시킨다."""
    with patch.dict("os.environ", {"LOGIN_ID": "", "LOGIN_PASSWORD": "pass"}, clear=False):
        from config import validate_config
        with pytest.raises(ValueError, match="LOGIN_ID"):
            validate_config()


def test_validate_config_raises_when_login_password_missing():
    """LOGIN_PASSWORD가 비어있으면 ValueError를 발생시킨다."""
    with patch.dict("os.environ", {"LOGIN_ID": "user@test.com", "LOGIN_PASSWORD": ""}, clear=False):
        from config import validate_config
        with pytest.raises(ValueError, match="LOGIN_PASSWORD"):
            validate_config()


def test_validate_config_passes_with_valid_settings():
    """필수 설정이 모두 있으면 에러 없이 통과한다."""
    with patch.dict("os.environ", {"LOGIN_ID": "user@test.com", "LOGIN_PASSWORD": "pass"}, clear=False):
        from config import validate_config
        validate_config()
