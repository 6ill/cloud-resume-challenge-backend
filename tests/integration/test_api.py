from playwright.sync_api import APIRequestContext, Playwright
import pytest

def test_api_counter_increment(playwright: Playwright, api_endpoint: str):
    """
    Test that the API endpoint is reachable and increments the counter.
    """
    api_context: APIRequestContext = playwright.request.new_context()

    response = api_context.post(api_endpoint)

    assert response.ok, f"API failed with status {response.status}: {response.text()}"
    
    data = response.json()
    
    assert "count" in data
    assert isinstance(data["count"], int)
    assert data["count"] > 0
    
    print(f"API Verified. Current Count: {data['count']}")

    api_context.dispose()