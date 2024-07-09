from assertpy import assert_that
import allure
from task_2.helpers import HelperRandom


@allure.suite("Complicated Page")
class TestComplicatedPage:
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Count section buttons")
    def test_count_section_buttons(self, complicated_page):
        count = complicated_page.count_section_buttons()
        with allure.step("Check if there are buttons in the Button Section"):
            assert_that(count).is_greater_than(0)

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify Facebook links")
    def test_verify_facebook_links(self, complicated_page):
        facebook_buttons = complicated_page.page.locator(complicated_page.facebook_buttons)
        total_facebook_buttons = complicated_page.count_facebook_buttons()
        assert_that(total_facebook_buttons).is_greater_than(0)

        # we can use soft_assertions: with soft_assertions():
        with allure.step("Verify all facebook button’s href equal to ‘https://www.facebook.com/Ultimateqa1/’ "
                         "in ‘Section of Social Media Follows’"):
            for i in range(total_facebook_buttons):
                href = facebook_buttons.nth(i).get_attribute("href")
                assert_that(href).is_equal_to("https://www.facebook.com/Ultimateqa1/")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Fill form Section of Random Stuff")
    def test_fill_form(self, complicated_page):
        complicated_page.fill_form(HelperRandom.get_full_name(),
                                   HelperRandom.get_email_address(), HelperRandom.get_str())
        success_message = complicated_page.get_success_message()
        with allure.step("Verify the message: 'Thanks for contacting us' is displayed after submitting the form"):
            assert_that(success_message).contains("Thanks for contacting us")
