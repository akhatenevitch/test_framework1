from pages.checkout_page import CheckoutPage
from pages.store_page import StorePage
from pytest_bdd import when, scenarios, then
from ..common_steps import *
from ..util.utils import parse_str_table

scenarios("ui/main_page/test_page.feature")


@when(parsers.parse('I click {button} button'))
def click_button(page, button):
    store_page = StorePage(page)
    store_page.click_button(button)


@when(parsers.parse('I click on {product_name} product'))
def open_product_page(page, product_name):
    store_page = StorePage(page)
    store_page.click_product_link(product_name)
    store_page.verify_on_product_page(product_name)


@when('On product\'s page I click add to cart')
def click_add_to_card_on_product_page(page):
    store_page = StorePage(page)
    if store_page.page.query_selector(store_page.shopping_cart_counter) is None:
        shopping_cart_counter_before = 0
    else:
        shopping_cart_counter_before = int(store_page.page.inner_text(store_page.shopping_cart_counter))
    store_page.click_button("ADD_TO_CART_BUTTON")
    store_page.verify_shopping_cart_counter_increased(shopping_cart_counter_before)


@then("I open my cart")
def open_cart(page):
    cart_page = StorePage(page)
    cart_page.open_cart()


@when(parsers.parse('I verify next products are in cart:\n{products_table}'))
def verify_products_in_cart(page, products_table):
    products_table = parse_str_table(products_table)
    cart_page = StorePage(page)
    products_table = dict(zip(products_table.get("product"), products_table.get("quantity")))
    for product, quantity in products_table.items():
        cart_page.find_and_assert_product_quantity_in_cart(product, quantity)


@when("I proceed to checkout")
def click_proceed_to_checkout(page):
    store_page = StorePage(page)
    store_page.click_button("CHECKOUT")
    checkout_page = CheckoutPage(page)
    checkout_page.verify_on_checkout_page()


@when("I fill in checkout information and continue")
def fill_in_checkout_information(page):
    checkout_page = CheckoutPage(page)
    checkout_page.fill_in_information_and_continue()
    checkout_page.verify_on_checkout_summary_page()


@when(parsers.parse("I verify checkout overview for products:\n{products_table}"))
def verify_checkout_overview_for_products(page, products_table):
    checkout_page = CheckoutPage(page)
    products_table = parse_str_table(products_table)
    products_table = dict(zip(products_table.get("product"), products_table.get("quantity")))
    store_page = StorePage(page)
    for product, quantity in products_table.items():
        store_page.find_and_assert_product_quantity_in_cart(product, quantity)
    checkout_page.find_and_assert_product_price_checkout_overview()


@when("I finish order")
def finish_order(page):
    checkout_page = CheckoutPage(page)
    checkout_page.finish_order()


@when(parsers.parse("I add {product} to cart"))
def add_product_to_cart(page, product):
    store_page = StorePage(page)
    store_page.click_add_or_remove_product_to_from_cart(True, product)


@when(parsers.parse("I remove {product} from cart on {page_type} page"))
def remove_product_from_cart(page, product, page_type):
    store_page = StorePage(page)
    store_page.click_add_or_remove_product_to_from_cart(False, product, page_type)


@when("I try to continue checkout")
def continue_checkout_with_error(page):
    checkout_page = CheckoutPage(page)
    checkout_page.click_button("CONTINUE")
    checkout_page.error_is_shown()


@when("I cancel checkout")
def cancel_checkout(page):
    checkout_page = CheckoutPage(page)
    checkout_page.click_button("CANCEL")
    store_page = StorePage(page)
    store_page.is_on_cart_page()


@when("I continue shopping")
def continue_shopping_from_cart(page):
    store_page = StorePage(page)
    store_page.click_button("CONTINUE_SHOPPING")
    store_page.is_on_store_page()
