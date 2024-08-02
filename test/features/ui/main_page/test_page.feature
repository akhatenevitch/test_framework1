@ui
Feature: Example BDD tests

#    Scenario: user can navigate to the domains page
#        Given an example site
#        When they click on the "More information" link
#        Then they are able to navigate to the Domains page

#  Scenario Outline: user can navigate to the ican page
#    Given an example site
#    When they click on the "More information" link
#    Then they are able to navigate to the expected web page
#
#    Examples:
#      | menu_item | expected_url                   |
#      | domains   | https://www.iana.org/domains   |
#      | numbers   | https://www.iana.org/numbers   |
#      | protocols | https://www.iana.org/protocols |
#      | about us  | https://www.iana.org/about     |

  @e2e
  Scenario: e2e
    Given an example site
    When I login as standard user
    And I click on backpack product
    And On product's page I click add to cart
    Then I open my cart
    When I verify next products are in cart:
      | product  | quantity|
      | backpack |    1    |
    And I proceed to checkout
    And I fill in checkout information and continue
    And I verify checkout overview for products:
      | product  | quantity|
      | backpack |    1    |
    And I finish order

    @mytest
  Scenario: e2e different products
    Given an example site
    When I login as standard user
    And I add onesie to cart
    And I add tshirt to cart
    And I add bike_light to cart
    And I add jacket to cart
    And I remove onesie from cart on main page
    Then I open my cart
    When I verify next products are in cart:
      | product  | quantity|
      | bike_light |    1    |
      | tshirt |    1    |
      | jacket |    1    |
    And I remove jacket from cart on cart page
    When I verify next products are in cart:
      | product  | quantity|
      | bike_light |    1    |
      | tshirt |    1    |
    And I proceed to checkout
    And I fill in checkout information and continue
    And I verify checkout overview for products:
      | product  | quantity|
      | bike_light |    1    |
      | tshirt |    1    |
    And I finish order

      @error
  Scenario: error
    Given an example site
    When I login as standard user
    And I add onesie to cart
    And I add tshirt to cart
    Then I open my cart
    When I verify next products are in cart:
      | product  | quantity|
      | onesie |    1    |
      | tshirt |    1    |
    And I continue shopping
    And I add backpack to cart
    Then I open my cart
    When I verify next products are in cart:
      | product  | quantity|
      | onesie |    1    |
      | tshirt |    1    |
      | backpack |    1    |
    And I proceed to checkout
    And I try to continue checkout
    And I cancel checkout
