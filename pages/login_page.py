from dotenv import load_dotenv
from playwright.sync_api import Page
import os

load_dotenv()


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.login_field = page.locator('id=user-name')
        self.password_field = page.locator('id=password')
        self.login_button = page.locator('id=login-button')

    def input_login(self, login):
        self.login_field.fill(login)

    def input_login_as_user(self, user_type):
        login = None
        match user_type:
            case "standard":
                login = os.environ.get('STANDARD_USER_LOGIN')
            case "problem":
                login = os.environ.get('PROBLEM_USER_LOGIN')
        self.input_login(login)

    def input_password(self):
        self.password_field.fill(os.environ.get('USER_PASSWORD'))

    def click_login_button(self):
        self.login_button.click()
