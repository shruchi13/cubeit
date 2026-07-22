import os
from conftest import GITHUB_USER, GITHUB_REPO
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
from playwright.sync_api import APIRequestContext, Page

def test_create_issue(api_context: APIRequestContext):
    issue_data = {
        "title": "[BUG] That went wrong",
        "body": "When doing this , that failed"
    }

    post_reponse = api_context.post(
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues",
        data= issue_data

    )

    assert post_reponse.ok

def test_take_issues_screenshot(page: Page):
    page.goto(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/issues")
    # Reload page to bypass client side caching 
    page.reload()
    # Wait for the issue list element or title to actually load in the UI 
    page.get_by_text("[BUG] That went wrong").wait_for()

    page.screenshot(path="github-issues-page.jpg", full_page=True)

def test_new_issue_in_repo(api_context: APIRequestContext):
    all_issues =api_context.get(
        f"repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    )

    assert all_issues.ok

    matching_issue =[
        issue 
        for issue in all_issues.json() 
        if issue["title"]=="[BUG] That went wrong"
    ]
    
    assert len(matching_issue)> 0, "No issue found with title '[BUG] that went wrong'"

    new_issue = matching_issue[0]

    assert new_issue["body"]=="When doing this , that failed"