import pytest
import os

API_URL = os.environ["API_URL"]
FRONTEND_URL = os.environ["FRONTEND_URL"]

@pytest.fixture(scope="session")
def api_endpoint():
    return API_URL

@pytest.fixture(scope="session")
def website_url():
    return FRONTEND_URL