import pytest
from creds import *
from playwright.sync_api import Playwright, APIRequestContext

@pytest.fixture(scope="session")

def api_context(playwright: Playwright):
    context = playwright.request.new_context(

        base_url="https://api.github.com/",
        extra_http_headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {GITHUB_ACCESS_TOKEN}"
        }
    )
    yield context
    context.dispose()

@pytest.fixture(autouse=True, scope="session")

def create_test_repository(api_context: APIRequestContext):
    # Create the test repo
    post_response = api_context.post(
        "/user/repos",
        data={"name" : GITHUB_REPO}
    )

    assert post_response.ok # post response is using ok properties 

    yield

    # Delete the test repo 
    delete_response = api_context.delete(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}"
    )

    assert delete_response.ok
