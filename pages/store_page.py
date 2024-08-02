import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class StorePage(BasePage):
    HEADER: str = 'h1'

    cart_container = "id=cart_contents_container"
    product_title = ".inventory_details_name"
    store_page_container = ".inventory_container"

    buttons = {
        "CART_BUTTON": ".shopping_cart_link",
        "ADD_TO_CART_BUTTON": "text=ADD TO CART",
        "CHECKOUT": ".checkout_button",
        "CONTINUE_SHOPPING": ".cart_footer .btn_secondary"
    }

    product_page = {
        "backpack": {
            "title": "Sauce Labs Backpack"
        },
        "bike_light": {
            "title": "Sauce Labs Bike Light"
        },
        "tshirt": {
            "title": "Sauce Labs Bolt T-Shirt"
        },
        "jacket": {
            "title": "Sauce Labs Fleece Jacket"
        },
        "onesie": {
            "title": "Sauce Labs Onesie"
        },
    }

    def __init__(self, page: Page):
        self.page = page
        super().__init__(page)

    def click_product_link(self, product):
        self.page.click(self.store_page_products.get(product))

    def is_on_cart_page(self):
        expect(self.page.locator(self.cart_container)).to_be_visible()

    def is_on_store_page(self):
        expect(self.page.locator(self.store_page_container)).to_be_visible()

    def verify_on_product_page(self, product):
        expect(self.page.locator(self.product_title).and_(
            self.page.get_by_text(self.product_page.get(product).get("title")))).to_be_visible()

    def click_add_or_remove_product_to_from_cart(self, add, product, page_type="main"):
        product_id = re.sub(r"[\[\]()]", "", self.store_page_products.get(product))
        product_add_to_cart_button_selector = f"//div[div[a[@{product_id}]]]//button"
        product_add_to_cart_button = self.page.locator(product_add_to_cart_button_selector)
        if add:
            expect(product_add_to_cart_button).to_have_text("ADD TO CART")
        else:
            expect(product_add_to_cart_button).to_have_text("REMOVE")

        product_add_to_cart_button.click()

        if page_type == "main":
            if add:
                expect(product_add_to_cart_button).to_have_text("REMOVE")
            else:
                expect(product_add_to_cart_button).to_have_text("ADD TO CART")
