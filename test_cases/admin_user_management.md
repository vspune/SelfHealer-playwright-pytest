# Test Cases — Admin: User Management UI

| Field | Value |
|---|---|
| Feature | Admin → User Management tab (System Users) — filter form UI (OrangeHRM demo) |
| Application URL | https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers |
| Status | Ready |
| Source | Manual |
| Author | <name> |
| Last updated | 2026-10-14 |

## Acceptance criteria

- **AC-1:** Clicking **Admin** in the left menu opens the User Management tab with the System Users card.
- **AC-2:** The filter form shows the Username and Employee Name inputs.
- **AC-3:** The User Role dropdown defaults to `-- Select --` and offers `-- Select --`, `Admin`, `ESS`.
- **AC-4:** The Status dropdown defaults to `-- Select --` and offers `-- Select --`, `Enabled`, `Disabled`.
- **AC-5:** The Reset, Search and Add buttons are shown.
- **AC-6:** Clicking **Add** opens the Add User page, which shows **Cancel** and **Save** buttons.

Source: user list + screenshot of the live page (2026-10-12).

---

## TC-1: Admin in the left menu opens User Management

| Field | Value |
|---|---|
| Covers | AC-1 |
| Type | Positive |
| Priority | P0 |
| Tags | `admin`, `smoke`, `p0` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in via the login fixture; Dashboard is displayed.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Click **Admin** in the left menu | URL matches `**/admin/viewSystemUsers` |
| 2 | Observe the page | The **System Users** heading is visible |

**Postconditions / cleanup**
- None.

**Notes**
- The User Management tab appears selected (highlighted) in the screenshot. Not asserted here —
  how "selected" is exposed in the DOM is not confirmed yet.

---

## TC-2: Username and Employee Name inputs are shown

| Field | Value |
|---|---|
| Covers | AC-2 |
| Type | Positive |
| Priority | P1 |
| Tags | `admin`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in; User Management opened by clicking **Admin** in the left menu.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the Username field | Username input is visible |
| 2 | Observe the Employee Name field | Employee Name input is visible with placeholder `Type for hints...` |

**Postconditions / cleanup**
- None.

---

## TC-3: User Role dropdown shows the expected default and options

| Field | Value |
|---|---|
| Covers | AC-3 |
| Type | Positive |
| Priority | P1 |
| Tags | `admin`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in; User Management opened by clicking **Admin** in the left menu.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the User Role dropdown | It shows `-- Select --` |
| 2 | Open the User Role dropdown | Options are exactly `-- Select --`, `Admin`, `ESS`, in that order |
| 3 | Close the dropdown without selecting | The dropdown still shows `-- Select --` |

**Postconditions / cleanup**
- None — nothing is selected.

**Notes**
- Default text confirmed from screenshot. Option list from user; if the live option spacing differs, report it.

---

## TC-4: Status dropdown shows the expected default and options

| Field | Value |
|---|---|
| Covers | AC-4 |
| Type | Positive |
| Priority | P1 |
| Tags | `admin`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in; User Management opened by clicking **Admin** in the left menu.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the Status dropdown | It shows `-- Select --` |
| 2 | Open the Status dropdown | Options are exactly `-- Select --`, `Enabled`, `Disabled`, in that order |
| 3 | Close the dropdown without selecting | The dropdown still shows `-- Select --` |

**Postconditions / cleanup**
- None — nothing is selected.

**Notes**
- Same note as TC-3.

---

## TC-5: Reset, Search and Add buttons are shown

| Field | Value |
|---|---|
| Covers | AC-5 |
| Type | Positive |
| Priority | P1 |
| Tags | `admin`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in; User Management opened by clicking **Admin** in the left menu.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Observe the filter form buttons | **Reset** and **Search** buttons are visible |
| 2 | Observe the area above the users table | **Add** button is visible (shown as `+ Add`) |

**Postconditions / cleanup**
- None — no button is clicked.

---

## TC-6: Clicking Add opens the Add User page with Cancel and Save buttons

| Field | Value |
|---|---|
| Covers | AC-6 |
| Type | Positive |
| Priority | P1 |
| Tags | `admin`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` (via login fixture) |

**Preconditions**
- Logged in; User Management opened by clicking **Admin** in the left menu.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Click **Add** (shown as `+ Add`) | URL matches `**/admin/saveSystemUser` |
| 2 | Observe the form buttons | **Cancel** and **Save** buttons are visible |

**Postconditions / cleanup**
- None — the Add User form is opened but nothing is saved (**Save** is never clicked).

---

## Coverage

| AC | Positive | Negative | Boundary |
|---|---|---|---|
| AC-1 | TC-1 | — | — |
| AC-2 | TC-2 | — | — |
| AC-3 | TC-3 | — | — |
| AC-4 | TC-4 | — | — |
| AC-5 | TC-5 | — | — |
| AC-6 | TC-6 | — | — |

**Not covered yet (next, one by one):**
- Admin top tabs (Job, Organization, …) — each gets its own test cases.
- Search by each filter, Reset behaviour, Employee Name hints — behaviour not specified.
- Add User form fields and saving a user — only navigation + Cancel/Save visibility is covered (TC-6).
- Users table ("Records Found" count, columns, sorting), Edit / Delete — out of scope for now.
