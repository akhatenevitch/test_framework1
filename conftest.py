import os.path
from typing import Generator
import pytest
import yaml
from playwright.sync_api import Playwright, APIRequestContext


def load_config(env):
    config_file = f"configs/config_{env}.yaml"
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")


@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    return load_config(env)


@pytest.fixture(scope="session")
def my_fixture(request, api_request_context, config):
    if 'unauthorised' in request.keywords:
        yield None
    else:
        login_data = {"username": config["api"]["restful_booker"]["username"],
                      "password": config["api"]["restful_booker"]["user_password"]}
        api_request_context.post(f'{config["api"]["restful_booker"]["service_url"]}/auth', data=login_data)


@pytest.fixture
def scenario_context():
    return {}


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(ignore_https_errors=True)
    yield request_context
    request_context.dispose()
