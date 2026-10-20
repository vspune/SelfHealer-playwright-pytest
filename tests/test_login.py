import re

import pytest
from playwright.sync_api import Locator, Page, expect

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


def _expect_input_value(locator: Locator, expected: str, field_name: str) -> None:
    if locator.input_value() != expected:
        pytest.fail(
            f"{field_name} field did not retain the supplied value",
            pytrace=False,
        )


def _expect_login_form(login_page: LoginPage) -> None:
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.login_button).to_be_visible()


def test_tc1_valid_admin_credentials_open_dashboard(
    page: Page,
    login_page: LoginPage,
    dashboard_page: DashboardPage,
    valid_username: str,
    valid_password: str,    
) -> None:
    """TC-1 · test_cases/login.md"""
    login_page.open()
    _expect_login_form(login_page)

    login_page.enter_username(valid_username)
    _expect_input_value(login_page.username_input, valid_username, "Username")

    login_page.enter_password(valid_password)
    _expect_input_value(login_page.password_input, valid_password, "Password")
    expect(login_page.password_input).to_have_attribute("type", "password")

    login_page.submit()
    expect(page).to_have_url(re.compile(r".*/dashboard/index$"))
    dashboard_page.wait_until_loaded()
    expect(dashboard_page.dashboard_heading).to_be_visible()


def test_tc2_wrong_password_shows_error_without_logging_in(
    page: Page,
    login_page: LoginPage,
    valid_username: str,
    invalid_password: str,
) -> None:
    """TC-2 · test_cases/login.md"""
    login_page.open()
    _expect_login_form(login_page)

    login_page.enter_username(valid_username)
    _expect_input_value(login_page.username_input, valid_username, "Username")

    login_page.enter_password(invalid_password)
    _expect_input_value(login_page.password_input, invalid_password, "Password")
    expect(login_page.password_input).to_have_attribute("type", "password")

    login_page.submit()
    expect(login_page.error_message).to_have_text("Invalid credentials")
    expect(page).to_have_url(re.compile(r".*/auth/login$"))


def test_tc3_empty_credentials_show_required_validation(
    page: Page,
    login_page: LoginPage,
) -> None:
    """TC-3 · test_cases/login.md"""
    login_page.open()
    _expect_login_form(login_page)
    expect(login_page.username_input).to_have_value("")
    expect(login_page.password_input).to_have_value("")

    login_page.submit()
    expect(login_page.username_required_message).to_have_text("Required")
    expect(login_page.password_required_message).to_have_text("Required")
    expect(page).to_have_url(re.compile(r".*/auth/login$"))
