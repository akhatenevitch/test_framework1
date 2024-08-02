from pytest_bdd import when, given, parsers

from pages.login_page import LoginPage
from pages.store_page import StorePage


@given("an example site")
def goto_website(page, config):
    main_page = StorePage(page)
    page.goto(config['ui']['login_url'])
    # main_page.verify_header_text()


@when(parsers.parse("I login as {user_type} user"))
def login_as_user(page, user_type):
    login_page = LoginPage(page)
    login_page.input_login_as_user(user_type)
    login_page.input_password()
    login_page.click_login_button()


@when('The user fills in login')
def fill_in_login(page):
    login_page = LoginPage(page)
    # login_page.input_login()


@when('The user fills in password')
def fill_in_password(page):
    login_page = LoginPage(page)
    login_page.input_password()

