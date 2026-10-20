from playwright.sync_api import Page

import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_text("Invalid credentials", exact=True)
        username_group = page.locator(".oxd-input-group").filter(
            has=self.username_input
        )
        password_group = page.locator(".oxd-input-group").filter(
            has=self.password_input
        )
        self.username_required_message = username_group.get_by_text(
            "Required", exact=True
        )
        self.password_required_message = password_group.get_by_text(
            "Required", exact=True
        )

    def open(self) -> None:
        self.goto(config.LOGIN_PATH)
        self.username_input.wait_for(state="visible")
        self.password_input.wait_for(state="visible")
        self.login_button.wait_for(state="visible")

    def enter_username(self, username: str) -> None:
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)

    def submit(self) -> None:
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
