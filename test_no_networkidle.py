"""
Regression test: networkidle must not be used in crawl scripts.
networkidle causes Timeout errors in GitHub Actions headless environment.
"""
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent


def read_source(filename: str) -> str:
    return (PROJECT_ROOT / filename).read_text(encoding="utf-8")


def test_main_py_has_no_networkidle():
    source = read_source("main.py")
    assert "networkidle" not in source, (
        "main.py still contains 'networkidle' which causes timeouts in GitHub Actions"
    )


def test_crawl_january_py_has_no_networkidle():
    source = read_source("crawl_january.py")
    assert "networkidle" not in source, (
        "crawl_january.py still contains 'networkidle' which causes timeouts in GitHub Actions"
    )
