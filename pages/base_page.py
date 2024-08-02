import re

from playwright.sync_api import Page, expect


class BasePage:
    shopping_cart_counter = ".shopping_cart_badge"
    cart_container = "id=cart_contents_container"

    buttons = {
        "CART_BUTTON": ".shopping_cart_link",
    }

    store_page_products = {
        "backpack": "[id=\"item_4_title_link\"]",
        "bike_light": "[id=\"item_0_title_link\"]",
        "tshirt": "[id=\"item_1_title_link\"]",
        "jacket": "[id=\"item_5_title_link\"]",
        "onesie": "[id=\"item_2_title_link\"]",
    }

    # product_page = {
    #     "backpack": {
    #         "title": "Sauce Labs Backpack"
    #     },
    #     "bike_light": {
    #         "title": "Sauce Labs Bike Light"
    #     },
    #     "tshirt": {
    #         "title": "Sauce Labs Bolt T-Shirt"
    #     },
    #     "jacket": {
    #         "title": "Sauce Labs Fleece Jacket"
    #     },
    #     "onesie": {
    #         "title": "Sauce Labs Onesie"
    #     },
    # }

    def __init__(self, page: Page):
        self.page = page

    def verify_page_url(self, url):
        assert self.page.url == url

    def click_button(self, button):
        self.page.click(self.buttons.get(button))

    def verify_shopping_cart_counter_increased(self, counter_before):
        assert int(self.page.inner_text(self.shopping_cart_counter)) > counter_before

    def open_cart(self):
        self.click_button("CART_BUTTON")
        expect(self.page.locator(self.cart_container)).to_be_visible()

    def find_and_assert_product_quantity_in_cart(self, product, quantity):
        # product_id = self.store_page_products.get(product).replace("[", "").replace("]", "")
        product_id = re.sub(r"[\[\]()]", "", self.store_page_products[product])
        expect(self.page.locator(f"//div[a[@{product_id}]]/preceding-sibling"
                                 f"::div")).to_have_text(quantity)

    def __getattr__(self, item):
        # This method is called only if the requested attribute is not found in the instance's __dict__
        if item in self.__class__.buttons:
            return self.__class__.buttons[item]
        elif item in self.__class__.__bases__[0].buttons:
            return self.__class__.__bases__[0].buttons[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __getitem__(self, key):
        # This method allows dict-style access for variables
        return self.__class__.variables.get(key, self.__class__.__bases__[0].buttons.get(key))
