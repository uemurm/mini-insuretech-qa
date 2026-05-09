import pytest

@pytest.mark.ui
def test_doc_page_title(swagger_page):
    assert swagger_page.title() == 'Mini InsureTech QA Portfolio API - Swagger UI'

@pytest.mark.ui
def test_doc_page_header1(swagger_page):
    assert 'Mini InsureTech QA Portfolio API' in swagger_page.locator('H1.title').text_content()

@pytest.mark.ui
def test_doc_page_endpoints(swagger_page):
    assert swagger_page.locator('.opblock').count() == 5
