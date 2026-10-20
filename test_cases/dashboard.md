# Test Cases — Dashboard: Left Menu UI

| Field | Value |
|---|---|
| Feature | Dashboard — left menu UI (OrangeHRM demo) |
| Application URL | https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index |
| Status | Ready |
| Source | Manual |
| Author | <name> |
| Last updated | 2026-10-12 |

## Acceptance criteria

- **AC-1:** After login, the left menu shows the Search box and all 12 module items.
- **AC-2:** The menu items appear in the expected order.
- **AC-3:** On the Dashboard page, the Dashboard item is shown as the active (highlighted) item.

Source: screenshot of the live app for the Admin user (2026-10-12).

## Expected menu (top to bottom)

| # | Item | Tag |
|---|---|---|
| 1 | Admin | `admin` |
| 2 | PIM | `pim` |
| 3 | Leave | `leave` |
| 4 | Time | `time` |
| 5 | Recruitment | `recruitment` |
| 6 | My Info | `my_info` |
| 7 | Performance | `performance` |
| 8 | Dashboard | `dashboard` |
| 9 | Directory | `directory` |
| 10 | Maintenance | `maintenance` |
| 11 | Claim | `claim` |
| 12 | Buzz | `buzz` |

---

## TC-1: Each left-menu item is visible after login

| Field | Value |
|---|---|
| Covers | AC-1 |
| Type | Positive |
| Priority | P0 |
| Tags | `left_menu`, `smoke`, `p0` + **the item's own tag** (see Expected menu) |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in via the login fixture; Dashboard is displayed.

**Steps** — run once **per menu item** (12 tests, one per row of Expected menu):

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the left menu | The Search box is visible |
| 2 | Look for the menu item `<Item>` | `<Item>` is visible in the left menu |

**Postconditions / cleanup**
- None.

**Notes**
- One test per item so each carries its module tag, e.g. `pytest -m admin` runs only the Admin item.

---

## TC-2: Left-menu items appear in the expected order

| Field | Value |
|---|---|
| Covers | AC-2 |
| Type | Positive |
| Priority | P1 |
| Tags | `left_menu`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in via the login fixture; Dashboard is displayed.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Read all menu item names top to bottom | The list is exactly the 12 items of Expected menu, in that order |

**Postconditions / cleanup**
- None.

---

## TC-3: Dashboard is the active menu item on the Dashboard page

| Field | Value |
|---|---|
| Covers | AC-3 |
| Type | Positive |
| Priority | P1 |
| Tags | `left_menu`, `dashboard`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in via the login fixture; Dashboard is displayed.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the left menu | The Dashboard item is shown as active (highlighted) |
| 2 | Observe the other items | No other item is shown as active |

**Postconditions / cleanup**
- None.

**Notes**
- Inferred: "highlighted" is exposed as an active state in the DOM (e.g. an active class or
  `aria-current`). How it is detected must be confirmed during discovery — not by colour.

---

## Coverage

| AC | Positive | Negative | Boundary |
|---|---|---|---|
| AC-1 | TC-1 | Not covered — no hidden/restricted items specified for this user | — |
| AC-2 | TC-2 | — | — |
| AC-3 | TC-3 | — | — |

**Not covered yet (add as new TCs once behaviour is confirmed):**
- Search box filters the menu — expected filtering behaviour not specified.
- Collapse / expand toggle — expected collapsed state not specified.
- Clicking each item opens its page — target URLs / headings not specified.
- Other user roles — menu may differ; only the Admin user is covered.
