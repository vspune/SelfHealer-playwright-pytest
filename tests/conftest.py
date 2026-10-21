import pytest
from playwright.sync_api import Page

import config as settings
from components.side_menu import SideMenu
from pages.admin.user_management_page import UserManagementPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utilities.logger import get_logger
from utilities.screenshot import attach_failure_screenshot


log = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", choices=list(settings.ENVIRONMENTS),
                     help="Environment to test (URL and logins come from config.py); default qa")
    parser.addoption("--role", action="store", default=None,
                     help='Run only tests tagged @pytest.mark.role("<name>"), e.g. --role normal')
    parser.addoption("--marker", action="store", default=None,
                     help='Run only tests with this tag expression, e.g. --marker smoke (same as -m)')


def pytest_configure(config):
    if config.getoption("--marker"):
        config.option.markexpr = config.getoption("--marker")  # same effect as -m
    try:
        settings.use(config.getoption("--env"))
    except RuntimeError as error:
        raise pytest.UsageError(str(error))


def _role_of(item) -> str:
    marker = item.get_closest_marker("role")
    return marker.args[0] if marker and marker.args else "admin"


def _keep(config, items, wanted) -> None:
    kept = [i for i in items if wanted(i)]
    config.hook.pytest_deselected(items=[i for i in items if i not in kept])
    items[:] = kept


def pytest_collection_modifyitems(config, items):
    """Narrow the tests: roles the environment has a login for, then --role."""
    _keep(config, items, lambda i: _role_of(i) in settings.USERS)  # env has no login for the role
    if config.getoption("--role"):
        _keep(config, items, lambda i: _role_of(i) == config.getoption("--role"))


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
    return _role_of(request.node)


@pytest.fixture
def logged_in_page(
    page: Page,
    login_page: LoginPage,
    dashboard_page: DashboardPage,
    role: str,
) -> Page:
    user = settings.USERS[role]
    log.info("Logging in as role '%s' (user '%s')", role, user["username"])
    login_page.open()
    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/dashboard/index")
    dashboard_page.wait_until_loaded()
    return page


@pytest.fixture
def valid_username() -> str:
    return settings.USERS["admin"]["username"]


@pytest.fixture
def valid_password() -> str:
    return settings.USERS["admin"]["password"]


@pytest.fixture
def invalid_password() -> str:
    if not settings.INVALID_PASSWORD:
        raise pytest.UsageError("Missing required environment variable: INVALID_PASSWORD")
    return settings.INVALID_PASSWORD
