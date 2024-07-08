from playwright.sync_api import Page
import ast


def safe_eval(expr: str) -> int:
    """
    Safely evaluate a simple math expression.
    Only allows addition, subtraction, multiplication, and division.
    """
    allowed_nodes = {
        ast.Expression, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Num, ast.Constant
    }

    node = ast.parse(expr, mode='eval')

    for child in ast.walk(node):
        if type(child) not in allowed_nodes:
            raise ValueError(f"Disallowed operation: {type(child)}")

    compiled_expr = compile(node, '<string>', 'eval')
    return eval(compiled_expr)


class ComplicatedPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://ultimateqa.com/complicated-page"
        self.section_buttons = '//div[contains(@class, "et_pb_button_module_wrapper")]'
        self.facebook_buttons = '//div[@class="et_pb_row et_pb_row_4"]//a[@title="Follow on Facebook"]'
        self.name_field = '//input[@name="et_pb_contact_name_0"]'
        self.email_field = '//input[@name="et_pb_contact_email_0"]'
        self.message_field = '//textarea[@name="et_pb_contact_message_0"]'
        self.math_field = '//input[@name="et_pb_contact_captcha_0"]'
        self.math_question = '//span[@class="et_pb_contact_captcha_question"]'
        self.submit_button = '//button[@class="et_pb_contact_submit et_pb_button"]'
        self.success_message = '//div[@class="et-pb-contact-message"]//p'

    def navigate(self):
        self.page.goto(self.url)

    def count_section_buttons(self):
        return self.page.locator(self.section_buttons).count()

    def count_facebook_buttons(self):
        return self.page.locator(self.facebook_buttons).count()

    def fill_form(self, name: str, email: str, message: str):
        self.page.locator(self.name_field).fill(name)
        self.page.locator(self.email_field).fill(email)
        self.page.locator(self.message_field).fill(message)

        math_question_text = self.page.locator(f"({self.math_question})[1]").inner_text()
        answer = safe_eval(math_question_text)
        self.page.locator(self.math_field).fill(str(answer))

        self.page.locator(f"({self.submit_button})[1]").click()

    def get_success_message(self):
        self.page.wait_for_selector(self.success_message)
        return self.page.locator(self.success_message).inner_text()
