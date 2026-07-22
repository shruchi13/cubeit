import os
import pytest
from conftest import GITHUB_USER, GITHUB_REPO
from playwright.sync_api import APIRequestContext, Page
# Fetch credentials from environment variables (GitHub Actions), 
# or fallback to local defaults if running locally
USERNAME = os.getenv("APP_USERNAME", "local_fallback_user")
PASSWORD = os.getenv("APP_PASSWORD", "local_fallback_pass")
try:
    from creds import *
except ImportError:
    # Fallback dummy environment credentials for CI/CD
    USERNAME = "test_user"
    PASSWORD = "test_password"


def test_github_issue_lifecycle(api_context: APIRequestContext, page: Page):
    # 1. Create the issue via API
    issue_data = {
        "title": "[BUG] That went wrong",
        "body": "When doing this , that failed"
    }

    post_reponse = api_context.post(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues",
        data= issue_data

    )
    assert post_reponse.ok, f"Failed to create issue:{post_response.text()}"
    
    # 2. Verify issue exists in list via API 
    matching_issue = []
    max_tries = 5
    for attempt in range(max_tries):
        time.sleep(1)
        all_issues =api_context.get(f"repos/{GITHUB_USER}/{GITHUB_REPO}/issues")
        if all_issues.ok:
            matching_issue = [
                issue for issue in all_issues.json()
                if issue.get("title") == target_title
            ]
            if matching_issue:
                break

    assert all_issues.ok

    matching_issue =[
        issue 
        for issue in all_issues.json() 
        if issue["title"]=="[BUG] That went wrong"
    ]
    
    assert len(matching_issue)> 0, "No issue found with title '[BUG] that went wrong'"

    new_issue = matching_issue[0]

    assert new_issue["body"]=="When doing this , that failed"

    # 3. Verify issue appear in UI 
    page.goto(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/issues")
    # Reload page to bypass client side caching 
    page.reload()
    # Wait for the issue list element or title to actually load in the UI 
    page.get_by_text("[BUG] That went wrong").wait_for(timeout =10000)
    assert page.get_by_text("[BUG] That went wrong").is_visible()
    page.screenshot(path="github-issues-page.jpg", full_page=True)

