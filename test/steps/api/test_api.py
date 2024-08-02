import json
from functools import partial
from jsonpath_ng.ext import parse
from playwright.sync_api import APIRequestContext
from pytest_bdd import parsers, when, then, scenarios

from test.steps.ui.util.utils import parse_str_table, create_json_from_dict_table

scenarios("api/api.feature")


@when(
    parsers.cfparse('In {service}, I send {request_type} request to {url} with params {params}'))
def send_request_to_url(config, scenario_context: dict, service, request_type, url: str, params: str,
                        api_request_context: APIRequestContext):
    params = dict(map(str.strip, sub.split('=', 1)) for sub in params.split(',') if '=' in sub)
    response = None
    base_url = config['api'][service]['service_url']
    if request_type == "GET":
        response = api_request_context.get(f"{base_url}{url}", params=params)
    elif request_type == "POST":
        response = api_request_context.post(f"{url}")
    scenario_context['response'] = response


@then(
    parsers.cfparse('response code is {response_code: Number}', extra_types={'Number': int}))
def check_response_code(scenario_context, response_code):
    assert scenario_context['response'].status == response_code


@then(
    parsers.cfparse('In the response value in jsonpath {jsonpath} is equal to {value}'))
def verify_field_in_response(scenario_context, jsonpath, value):
    jsonpath_expression = parse(f"$.{jsonpath}")
    match = jsonpath_expression.find(scenario_context['response'].json())
    assert match[0].value == value


@when(parsers.cfparse('I create a new booking with the following information:\n{booking_info}'))
def create_new_booking(scenario_context, booking_info, api_request_context, config):
    booking_info = parse_str_table(booking_info)
    booking_info = dict(zip(booking_info.get("field"), booking_info.get("value")))
    booking_info_json = create_json_from_dict_table(booking_info)

    response = api_request_context.post(f'{config["api"]["restful_booker"]["service_url"]}/booking',
                                        data=json.dumps(booking_info_json),
                                        headers={"Content-Type": "application/json"}
                                        )
    scenario_context['response'] = response
    scenario_context['booking_info'] = booking_info_json


@when(parsers.cfparse('I update the booking with the following information:\n{booking_info}'))
def create_new_booking(scenario_context, booking_info, api_request_context, config):
    booking_info = parse_str_table(booking_info)
    booking_info = dict(zip(booking_info.get("field"), booking_info.get("value")))
    booking_info_json = create_json_from_dict_table(booking_info)
    booking_info_json["bookingid"] = scenario_context["response"].json()["bookingid"]

    response = api_request_context.post(f'{config["api"]["restful_booker"]["service_url"]}/booking',
                                        data=json.dumps(booking_info_json),
                                        headers={"Content-Type": "application/json"}
                                        )
    scenario_context['response'] = response
    scenario_context['booking_info'] = booking_info_json


@then("The booking is created successfully")
def verify_booking_was_created(scenario_context, api_request_context, config):
    response = scenario_context['response']
    assert response.status == 200
    data = response.json()
    booking_response = api_request_context.get(f'{config["api"]["restful_booker"]["service_url"]}/booking/{data["bookingid"]}')
    assert booking_response.status == 200
    booking_response = booking_response.json()
    assert data["booking"]["firstname"] == booking_response["firstname"]
    assert data["booking"]["lastname"] == booking_response["lastname"]
    assert data["booking"]["totalprice"] == booking_response["totalprice"]
    assert data["booking"]["depositpaid"] == booking_response["depositpaid"]
    assert data["booking"]["bookingdates"]["checkin"] == booking_response["bookingdates"]["checkin"]
    assert data["booking"]["bookingdates"]["checkout"] == booking_response["bookingdates"]["checkout"]
    assert data["booking"]["additionalneeds"] == booking_response["additionalneeds"]


@when("The booking is not created")
def verify_booking_not_created(scenario_context, api_request_context, config):
    response = scenario_context['response']
    assert response.status != 200
