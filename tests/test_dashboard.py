import pytest
from playwright.sync_api import expect

from components.side_menu import SideMenu


pytestmark = pytest.mark.usefixtures("logged_in_page")


@pytest.mark.parametrize(
    "item_name",
    [
        pytest.param("Admin", id="admin", marks=pytest.mark.admin),
        pytest.param("PIM", id="pim", marks=pytest.mark.pim),
        pytest.param("Leave", id="leave", marks=pytest.mark.leave),
        pytest.param("Time", id="time", marks=pytest.mark.time),
        pytest.param(
            "Recruitment", id="recruitment", marks=pytest.mark.recruitment
        ),
        pytest.param("My Info", id="my-info", marks=pytest.mark.my_info),
        pytest.param(
            "Performance", id="performance", marks=pytest.mark.performance
        ),
        pytest.param("Dashboard", id="dashboard", marks=pytest.mark.dashboard),
        pytest.param("Directory", id="directory", marks=pytest.mark.directory),
        pytest.param(
            "Maintenance", id="maintenance", marks=pytest.mark.maintenance
        ),
        pytest.param("Claim", id="claim", marks=pytest.mark.claim),
        pytest.param("Buzz", id="buzz", marks=pytest.mark.buzz),
    ],
)
@pytest.mark.left_menu
@pytest.mark.smoke
@pytest.mark.p0
def test_tc1_left_menu_item_visible_after_login(
    side_menu: SideMenu,
    item_name: str,
) -> None:
    """TC-1 · test_cases/dashboard.md"""
    expect(side_menu.search_input).to_be_visible()
    expect(side_menu.item(item_name)).to_be_visible()


@pytest.mark.left_menu
@pytest.mark.regression
@pytest.mark.p1
def test_tc2_left_menu_items_appear_in_expected_order(
    side_menu: SideMenu,
) -> None:
    """TC-2 · test_cases/dashboard.md"""
    expected_item_names = [
        "Admin",
        "PIM",
        "Leave",
        "Time",
        "Recruitment",
        "My Info",
        "Performance",
        "Dashboard",
        "Directory",
        "Maintenance",
        "Claim",
        "Buzz",
    ]

    expect(side_menu.menu_items).to_have_text(expected_item_names)


@pytest.mark.role("normal")
@pytest.mark.left_menu
@pytest.mark.dashboard
@pytest.mark.regression
@pytest.mark.p1
def test_tc3_dashboard_is_the_only_active_menu_item(
    side_menu: SideMenu,
) -> None:
    """TC-3 · test_cases/dashboard.md"""
    expect(side_menu.active_item()).to_have_count(1)
    expect(side_menu.active_item()).to_have_text("Dashboard")
