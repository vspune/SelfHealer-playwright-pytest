import base64

import allure
from playwright.sync_api import Page
from pytest_html import extras

from utilities.logger import get_logger

log = get_logger(__name__)


def attach_failure_screenshot(page: Page, report, nodeid: str) -> None:
    """Attach a full-page screenshot to the Allure and pytest-html reports."""
    try:
        png = page.screenshot(full_page=True)
    except Exception as error:
        log.warning("Could not take failure screenshot: %s", error)
        return
    log.error("%s failed (%s) - screenshot attached", nodeid, report.when)
    allure.attach(png, name="failure-screenshot", attachment_type=allure.attachment_type.PNG)
    report.extras = getattr(report, "extras", []) + [
        extras.png(base64.b64encode(png).decode(), "failure-screenshot")
    ]
