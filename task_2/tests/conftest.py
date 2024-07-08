import pytest
from playwright.sync_api import sync_playwright
import allure
from pages.complicated_page import ComplicatedPage


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def complicated_page(page):
    with allure.step("Creating a session"):
        page_obj = ComplicatedPage(page)
        page_obj.navigate()

    return page_obj
