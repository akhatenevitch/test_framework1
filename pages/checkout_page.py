import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):

    checkout_complete_container = "id=checkout_complete_container"
    checkout_container = "id=checkout_info_container"
    checkout_summary_container = "id=checkout_summary_container"
    item_price = ".inventory_item_price"
    subtotal = ".summary_subtotal_label"
    tax = ".summary_tax_label"
    total = ".summary_total_label"
    checkout_error = "data-test=error"

    buttons = {
        "CONTINUE": ".cart_button",
        "CANCEL": ".cart_cancel_link",
        "FINISH": ".cart_button"
    }

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator("id=first-name")
        self.last_name_input = page.locator("id=last-name")
        self.postal_code_input = page.locator("id=postal-code")
        super().__init__(page)

    def verify_header_text(self):
        assert self.page.inner_text(self.HEADER) == 'Example Domain'

    def select_more_information_link(self):
        with self.page.expect_navigation():
            self.click_button("MORE_INFO_LINK")

    def verify_on_checkout_page(self):
        expect(self.page.locator(self.checkout_container)).to_be_visible()

    def verify_on_checkout_summary_page(self):
        expect(self.page.locator(self.checkout_summary_container)).to_be_visible()

    def fill_in_information_and_continue(self):
        self.first_name_input.fill("fgjh")
        self.last_name_input.fill("last_name")
        self.postal_code_input.fill("123")
        expect(self.first_name_input).to_have_value("fgjh")
        expect(self.last_name_input).to_have_value("last_name")
        expect(self.postal_code_input).to_have_value("123")
        self.click_button("CONTINUE")

    def find_and_assert_product_price_checkout_overview(self):
        TOTAL = "total"
        SUBTOTAL = "subtotal"
        TAX = "tax"
        list_of_product_prices = self.page.locator(self.item_price)
        total_price = 0
        for price in list_of_product_prices.all_inner_texts():
            total_price += float(price.strip("$"))
        summary_values = {SUBTOTAL: {"selector": self.subtotal, "value": 0},
                          TAX: {"selector": self.tax, "value": 0},
                          TOTAL: {"selector": self.total, "value": 0}
                          }
        for summary_value in summary_values:
            summary_values[summary_value]["value"] = float(re.findall(r"\d*\.*\d+",
                                                           self.page.locator(summary_values[summary_value]["selector"])
                                                           .inner_text())[0])

        assert total_price == summary_values[SUBTOTAL]["value"]
        assert round(summary_values[SUBTOTAL]["value"] + summary_values[TAX]["value"], 2) == summary_values[TOTAL]["value"]

    def finish_order(self):
        self.click_button("FINISH")
        expect(self.page.locator(self.checkout_complete_container)).to_be_visible()

    def error_is_shown(self):
        expect(self.page.locator(self.checkout_error)).to_be_visible()
