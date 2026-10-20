from playwright.sync_api import Locator, Page

from components.side_menu import SideMenu
from pages.base_page import BasePage


class UserManagementPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.system_users_heading = page.get_by_role("heading", name="System Users")
        self.add_user_heading = page.get_by_role("heading", name="Add User")
        self.username_group = page.locator(".oxd-input-group").filter(
            has=page.get_by_text("Username", exact=True)
        )
        self.username_input = self.username_group.locator("input")
        self.user_role_group = page.locator(".oxd-input-group").filter(
            has=page.get_by_text("User Role", exact=True)
        )
        self.user_role_dropdown = self.user_role_group.locator(".oxd-select-text")
        self.user_role_value = self.user_role_group.locator(".oxd-select-text-input")
        self.employee_name_input = page.get_by_placeholder("Type for hints...")
        self.status_group = page.locator(".oxd-input-group").filter(
            has=page.get_by_text("Status", exact=True)
        )
        self.status_dropdown = self.status_group.locator(".oxd-select-text")
        self.status_value = self.status_group.locator(".oxd-select-text-input")
        self.dropdown_options = page.get_by_role("option")
        self.reset_button = page.get_by_role("button", name="Reset", exact=True)
        self.search_button = page.get_by_role("button", name="Search", exact=True)
        self.add_button = page.get_by_role("button", name="Add")
        self.cancel_button = page.get_by_role("button", name="Cancel", exact=True)
        self.save_button = page.get_by_role("button", name="Save", exact=True)

    def open_from_menu(self, side_menu: SideMenu) -> None:
        side_menu.item("Admin").click()
        self.wait_until_loaded()

    def wait_until_loaded(self) -> None:
        self.system_users_heading.wait_for(state="visible")

    def open_user_role(self) -> None:
        self.user_role_dropdown.click()

    def open_status(self) -> None:
        self.status_dropdown.click()

    def close_dropdown(self) -> None:
        self.page.keyboard.press("Escape")

    def click_add(self) -> None:
        self.add_button.click()
        self.add_user_heading.wait_for(state="visible")
