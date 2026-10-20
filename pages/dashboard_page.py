from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.dashboard_heading = page.get_by_role("heading", name="Dashboard")

    def wait_until_loaded(self) -> None:
        self.dashboard_heading.wait_for(state="visible")
