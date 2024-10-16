import sys
import os
import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.user_generator import UserGenerator
from tools.locators import Locators

BASE_URL = ""
REGISTER_URL = f"{BASE_URL}/User/Register"
LOGIN_URL = f"{BASE_URL}/User/Login"

def test_registration(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Generate data for the first user
    user_data_1 = UserGenerator.generate_random_user_data()
    page.goto(REGISTER_URL)
    page.get_by_label(Locators.DISPLAY_NAME_LABEL).fill(user_data_1["display_name"])
    page.get_by_label(Locators.HANDLE_NAME_LABEL).fill(user_data_1["handle_name"])
    page.get_by_label(Locators.PASSWORD_LABEL).fill(user_data_1["password"])
    page.get_by_role("button", name=Locators.REGISTER_BUTTON).click()

    # Generate data for the second user
    user_data_2 = UserGenerator.generate_random_user_data()
    page.goto(REGISTER_URL)
    page.get_by_label(Locators.DISPLAY_NAME_LABEL).fill(user_data_2["display_name"])
    page.get_by_label(Locators.HANDLE_NAME_LABEL).fill(user_data_2["handle_name"])
    page.get_by_label(Locators.PASSWORD_LABEL).fill(user_data_2["password"])
    page.get_by_role("button", name=Locators.REGISTER_BUTTON).click()

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
    page.goto(LOGIN_URL)
    page.fill(Locators.USERNAME_INPUT, user_data["handle_name"])
    page.fill(Locators.PASSWORD_INPUT, user_data["password"])
    page.get_by_role("button", name=Locators.LOGIN_BUTTON).click()

def send_private_message(page, user_data):
    """
    Send a private message to the specified user.
    """
    page.locator(Locators.PRIVATE_MESSAGES_TAB).click()
    page.locator("text=" + user_data["display_name"]).wait_for(timeout=5000)
    page.locator("text=" + user_data["display_name"]).click()
    message_input = page.locator(Locators.MESSAGE_INPUT)
    time.sleep(1)
    message_input.wait_for(timeout=5000)
    message_input.fill("toto je testovacia sprava")
    page.locator(Locators.SEND_MESSAGE_BUTTON).wait_for(timeout=5000)
    page.locator(Locators.SEND_MESSAGE_BUTTON).click()

def verify_private_message(page, user_data):
    """
    Verify that the specified user received the private message.
    """
    page.locator(Locators.PRIVATE_MESSAGES_TAB).click()
    page.locator("text=" + user_data["display_name"]).wait_for(timeout=5000)
    page.locator("text=" + user_data["display_name"]).click()
    message_locator = page.locator("text=toto je testovacia sprava")
    expect(message_locator).to_be_visible(timeout=10000)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_registration(playwright)