@api
Feature: api test

  @123
  Scenario: api test

    When I create a new booking with the following information:
      |field|value|
      |firstname|  1   |
      |lastname|    2 |
      |totalprice|   3  |
      |depositpaid|   4  |
      |bookingdates.checkin|  5   |
      |bookingdates.checkout|  6   |
      |additionalneeds|   7  |

    Then The booking is created successfully
#    Then The booking is not created
#
#    When I get an existing booking with the following information
#    |||
#
#    When I delete a booking
    When I update the booking with the following information:
      |field|value|
      |firstname|  11   |
      |lastname|   22 |
      |totalprice|   33  |
      |depositpaid|   44  |
      |bookingdates.checkin|  55   |
      |bookingdates.checkout|  66   |
      |additionalneeds|   77  |
#
#
#    dates = [today, x days in the future, x days in the past]