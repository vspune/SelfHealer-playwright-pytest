import re

import pytest
from playwright.sync_api import Page, expect

from components.side_menu import SideMenu
from pages.admin.user_management_page import UserManagementPage


@pytest.mark.admin
@pytest.mark.left_menu
@pytest.mark.smoke
@pytest.mark.p0

def test_tc1_admin_menu_opens_user_management(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-1 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)

    expect(logged_in_page).to_have_url(re.compile(r".*/admin/viewSystemUsers$"))
    expect(user_management_page.system_users_heading).to_be_visible()


@pytest.mark.admin
@pytest.mark.regression
@pytest.mark.p1
def test_tc2_username_and_employee_name_inputs_are_visible(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-2 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)

    expect(user_management_page.username_input).to_be_visible()
    expect(user_management_page.employee_name_input).to_be_visible()
    expect(user_management_page.employee_name_input).to_have_attribute(
        "placeholder", "Type for hints..."
    )


@pytest.mark.admin
@pytest.mark.regression
@pytest.mark.p1
def test_tc3_user_role_default_and_options(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-3 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)

    expect(user_management_page.user_role_value).to_have_text("-- Select --")
    user_management_page.open_user_role()
    expect(user_management_page.dropdown_options).to_have_text(
        ["-- Select --", "Admin", "ESS"]
    )
    user_management_page.close_dropdown()
    expect(user_management_page.user_role_value).to_have_text("-- Select --")


@pytest.mark.admin
@pytest.mark.regression
@pytest.mark.p1
def test_tc4_status_default_and_options(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-4 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)

    expect(user_management_page.status_value).to_have_text("-- Select --")
    user_management_page.open_status()
    expect(user_management_page.dropdown_options).to_have_text(
        ["-- Select --", "Enabled", "Disabled"]
    )
    user_management_page.close_dropdown()
    expect(user_management_page.status_value).to_have_text("-- Select --")


@pytest.mark.admin
@pytest.mark.regression
@pytest.mark.p1
def test_tc5_reset_search_and_add_buttons_are_visible(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-5 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)

    expect(user_management_page.reset_button).to_be_visible()
    expect(user_management_page.search_button).to_be_visible()
    expect(user_management_page.add_button).to_be_visible()


@pytest.mark.admin
@pytest.mark.regression
@pytest.mark.p1
def test_tc6_add_opens_form_with_cancel_and_save(
    logged_in_page: Page,
    side_menu: SideMenu,
    user_management_page: UserManagementPage,
) -> None:
    """TC-6 · test_cases/admin_user_management.md"""
    user_management_page.open_from_menu(side_menu)
    user_management_page.click_add()

    expect(logged_in_page).to_have_url(re.compile(r".*/admin/saveSystemUser$"))
    expect(user_management_page.cancel_button).to_be_visible()
    expect(user_management_page.save_button).to_be_visible()
