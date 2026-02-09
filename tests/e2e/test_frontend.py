from playwright.sync_api import Page, expect

def test_visitor_counter_loads(page: Page, website_url: str):
    """
    Load the website and ensure the visitor counter replaces 'Loading...' with a number.
    """
    page.goto(website_url)

    counter = page.get_by_test_id("visitor-count")

    expect(counter).to_be_visible()

    expect(counter).not_to_contain_text("Loading...")
    
    count_text = counter.text_content()
    assert count_text.isdigit(), f"Expected a number, got: {count_text}"