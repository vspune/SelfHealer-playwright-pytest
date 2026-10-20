import pytest
from playwright.sync_api import Page

import config
from components.side_menu import SideMenu
from pages.admin.user_management_page import UserManagementPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utilities.logger import get_logger
from utilities.screenshot import attach_failure_screenshot


log = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption("--role", action="store", default=None,
                     help='Run only tests tagged @pytest.mark.role("<name>"), e.g. --role ess')


def pytest_collection_modifyitems(config, items):
    """--role <name>: keep only tests whose role("<name>") tag matches."""
    wanted = config.getoption("--role")
    if not wanted:
        return
    kept = [i for i in items
            if (m := i.get_closest_marker("role")) and m.args and m.args[0] == wanted]
    config.hook.pytest_deselected(items=[i for i in items if i not in kept])
    items[:] = kept


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, attach a full-page screenshot to the Allure and HTML reports."""
    report = (yield).get_result()
    page = item.funcargs.get("page")
    if report.failed and page is not None:
        attach_failure_screenshot(page, report, item.nodeid)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    return DashboardPage(page)


@pytest.fixture
def side_menu(page: Page) -> SideMenu:
    return SideMenu(page)


@pytest.fixture
def user_management_page(page: Page) -> UserManagementPage:
    return UserManagementPage(page)


@pytest.fixture
def role(request: pytest.FixtureRequest) -> str:
    marker = request.node.get_closest_marker("role")
    return marker.args[0] if marker else "admin"


@pytest.fixture
def logged_in_page(
    page: Page,
    login_page: LoginPage,
    dashboard_page: DashboardPage,
    role: str,
) -> Page:
    user = config.USERS[role]
    log.info("Logging in as role '%s' (user '%s')", role, user["username"])
    login_page.open()
    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/dashboard/index")
    dashboard_page.wait_until_loaded()
    return page


@pytest.fixture
def valid_username() -> str:
    return config.VALID_USERNAME


@pytest.fixture
def valid_password() -> str:
    return config.VALID_PASSWORD


@pytest.fixture
def invalid_password() -> str:
    return config.INVALID_PASSWORD
