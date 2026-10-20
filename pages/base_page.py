from playwright.sync_api import Page

import config
from utilities.logger import get_logger

log = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, path: str) -> None:
        url = f"{config.BASE_URL}/{path.lstrip('/')}"
        log.info("Navigating to %s", url)
        self.page.goto(url)
