import pytest
from playwright.sync_api import sync_playwright
import allure
from task_2.pages.complicated_page import ComplicatedPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )


@pytest.fixture(scope="session")
def browser(pytestconfig):
    headless = pytestconfig.getoption("--headless")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
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
