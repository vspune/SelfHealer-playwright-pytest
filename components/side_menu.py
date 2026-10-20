from playwright.sync_api import Locator, Page


class SideMenu:
    def __init__(self, page: Page) -> None:
        self.container = page.locator(".oxd-sidepanel")
        self.navigation = self.container.get_by_role("navigation", name="Sidepanel")
        self.search_input = self.container.get_by_placeholder("Search")
        self.menu_items = self.navigation.locator("a.oxd-main-menu-item")
        self.active_items = self.navigation.locator("a.oxd-main-menu-item.active"  )

    def item(self, name: str) -> Locator:
        return self.navigation.get_by_role("link", name=name, exact=True)

    # def item_names(self) -> list[str]:
    #     return [name.strip() for name in self.menu_items.all_inner_texts()]

    def active_item(self) -> Locator:
        return self.active_items

