import pytest

@pytest.fixture
def swagger_page(page):
    page.goto('127.0.0.1:8000/docs')
    return page
