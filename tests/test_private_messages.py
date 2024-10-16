import sys
import os
import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.user_generator import UserGenerator

def test_registration(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Generate data for the first user
    user_data_1 = UserGenerator.generate_random_user_data()
    page.goto("https://a2dev.iresoft.cz:9130/IreChatTester/User/Register")
    page.get_by_label("Display name").click()
    page.get_by_label("Display name").fill(user_data_1["display_name"])
    page.get_by_label("Display name").press("Tab")
    page.get_by_label("Handle name").fill(user_data_1["handle_name"])
    page.get_by_label("Handle name").press("Tab")
    page.get_by_label("Password").fill(user_data_1["password"])
    page.get_by_role("button", name=" Register").click()

    # Generate data for the second user
    user_data_2 = UserGenerator.generate_random_user_data()
    page.goto("https://a2dev.iresoft.cz:9130/IreChatTester/User/Register")
    page.get_by_label("Display name").click()
    page.get_by_label("Display name").fill(user_data_2["display_name"])
    page.get_by_label("Display name").press("Tab")
    page.get_by_label("Handle name").fill(user_data_2["handle_name"])
    page.get_by_label("Handle name").press("Tab")
    page.get_by_label("Password").fill(user_data_2["password"])
    page.get_by_role("button", name=" Register").click()

    # Login with the first user
    login_user(page, user_data_1)

    # Send a private message to the second user
    send_private_message(page, user_data_2)

    # Login with the second user and verify the message
    login_user(page, user_data_2)
    verify_private_message(page, user_data_1)

    # ---------------------
    context.close()
    browser.close()

def login_user(page, user_data):
    """
    Log in with the provided user data.
    """
    page.goto("https://a2dev.iresoft.cz:9130/IreChatTester/User/Login")
    page.fill("#UserName", user_data["handle_name"])
    page.fill("#Password", user_data["password"])
    page.get_by_role("button", name="Login").click()

def send_private_message(page, user_data):
    """
    Send a private message to the specified user.
    """
    page.locator("span", has_text="Private Messages").click()
    page.locator("text=" + user_data["display_name"]).wait_for(timeout=5000)
    page.locator("text=" + user_data["display_name"]).click()
    message_input = page.locator("input[placeholder='Enter a message...']")
    time.sleep(1)
    message_input.wait_for(timeout=5000)
    message_input.fill("toto je testovacia sprava")
    page.locator("button.ui.labeled.icon.green.button").wait_for(timeout=5000)
    page.locator("button.ui.labeled.icon.green.button").click()

def verify_private_message(page, user_data):
    """
    Verify that the specified user received the private message.
    """
    page.locator("span", has_text="Private Messages").click()
    page.locator("text=" + user_data["display_name"]).wait_for(timeout=5000)
    page.locator("text=" + user_data["display_name"]).click()
    message_locator = page.locator("text=toto je testovacia sprava")
    expect(message_locator).to_be_visible(timeout=10000)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_registration(playwright)