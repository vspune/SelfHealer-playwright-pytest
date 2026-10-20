# Test Cases — Login

| Field | Value |
|---|---|
| Feature | Login (OrangeHRM demo) |
| Application URL | https://opensource-demo.orangehrmlive.com/web/index.php/auth/login |
| Status | Ready |
| Source | Manual |
| Author | <name> |
| Last updated | 2026-10-11 |

## Acceptance criteria

> Proposed for review — no written requirement was supplied. Confirm or edit before setting Ready.

- **AC-1:** A user with valid credentials can log in and reaches the Dashboard.
- **AC-2:** A user with a wrong password cannot log in and is shown an error.
- **AC-3:** Submitting with empty Username and Password does not log in and shows validation.

---

## TC-1: Valid admin credentials log the user in and open the Dashboard

| Field | Value |
|---|---|
| Covers | AC-1 |
| Type | Positive |
| Priority | P0 |
| Tags | `login`, `smoke`, `p0` |
| Test data | `VALID_USERNAME`, `VALID_PASSWORD` |

**Preconditions**
- Not logged in (fresh browser context).
- `VALID_USERNAME` and `VALID_PASSWORD` are set in `.env`.

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Open the login page (Application URL above) | Login form is displayed with Username field, Password field and Login button |
| 2 | Enter `VALID_USERNAME` | Username field contains the entered value |
| 3 | Enter `VALID_PASSWORD` | Password field contains the entered value (masked) |
| 4 | Click Login | URL matches `**/dashboard/index` |
| 5 | Observe the page | Dashboard heading is displayed |

**Postconditions / cleanup**
- User session exists in this test's browser context only. None to clean up.

**Notes**
- The Dashboard heading and step 4 URL were confirmed during live headed inspection.

---

## TC-2: Wrong password does not log in and shows an error

| Field | Value |
|---|---|
| Covers | AC-2 |
| Type | Negative |
| Priority | P1 |
| Tags | `login`, `regression`, `p1` |
| Test data | `VALID_USERNAME`, `INVALID_PASSWORD` |

**Preconditions**
- Not logged in (fresh browser context).

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Open the login page | Login form is displayed |
| 2 | Enter `VALID_USERNAME` | Username field contains the entered value |
| 3 | Enter `INVALID_PASSWORD` | Password field contains the entered value (masked) |
| 4 | Click Login | An error message "Invalid credentials" is displayed |
| 5 | Observe the URL | URL still matches the login route |

**Postconditions / cleanup**
- None.

**Notes**
- User remaining on the login route after a failed attempt was confirmed during live headed inspection.

---

## TC-3: Empty Username and Password show validation and do not log in

| Field | Value |
|---|---|
| Covers | AC-3 |
| Type | Boundary |
| Priority | P1 |
| Tags | `login`, `regression`, `p1` |
| Test data | None — both fields left empty |

**Preconditions**
- Not logged in (fresh browser context).

**Steps**

| # | Action (one per step) | Expected result |
|---|---|---|
| 1 | Open the login page | Login form is displayed |
| 2 | Leave the Username and Password fields empty and click Login | Form is not submitted |
| 3 | Observe the Username and Password fields | Username is highlighted and says Required; Password is highlighted and says Required |
| 4 | Observe the URL | URL still matches the login route |

**Postconditions / cleanup**
- None.

**Notes**
- Both fields display “Required” after empty submission, confirmed during live headed inspection.

---

## Coverage

| AC | Positive | Negative | Boundary |
|---|---|---|---|
| AC-1 | TC-1 | Covered by AC-2 / AC-3 | Not covered — no length limits specified for username/password |
| AC-2 | — | TC-2 | Not covered — no lockout / retry-limit behaviour specified |
| AC-3 | — | — | TC-3 (both empty). Only-username-empty / only-password-empty not covered — expected behaviour not specified |
