# Playwright POM Guidelines (Python)

Single source of truth for how Page Objects, components, fixtures and tests are structured in
this project. Used as the team's coding standard.

- **Part A** — general rules for Page Objects, components, fixtures and tests.
- **Part B** — Python conventions (pytest + pytest-playwright, sync API).
- **Part D** — execution and reporting commands.

> **Language:** this project is Python only. Never mix in other languages.

---

# Part A — Shared Rules

## A1. Separation of concerns

| Lives in Page Objects / components | Lives in test files |
|---|---|
| Locators | Test scenario and business flow |
| Reusable UI actions | Test data references |
| Waits for page/component state | Assertions (`expect`) |
| Page/component-specific helpers | Traceability to TC ID |

- Never put business assertions inside a Page Object.
- Never put locators inside a test file.
- Tests and pages are always **separate files**.

## A2. Page Objects and components

- One Page Object per application page or screen.
- One component class per reusable UI element that appears within or across pages
  (e.g. side menu, top bar / header, modal, search box, date picker, table toolbar).
- Keep `components/` separate from `pages/`.
- All Page Objects extend a shared **`BasePage`**, which holds:
  - navigation (`goto` to a path relative to the base URL)
  - common load waits
  - shared components used on every authenticated page (e.g. side menu, top bar)

## A3. Locator declaration

- Declare each locator once, in the constructor, as a class attribute.
- Name locators after the element's **purpose**, not its selector
  (`username_input`, not `input_3` / `css_input`).
- Do not write methods that re-query the same locator repeatedly.
- Only add locators confirmed in the live DOM (inspect the live page). LOW and
  NOT CONFIRMED locators never go into a Page Object.

## A4. Locator priority

1. Role + accessible name
2. Label
3. Text
4. Placeholder
5. Test ID — fallback when the above can't uniquely identify the element
6. Stable CSS / attribute — last resort, with a reason noted
7. XPath — only when nothing else works, with a reason noted

Prefer scoping to a container (row, dialog, section) over positional `first` / `nth` / `last`.

## A5. Navigation between pages

- A Page Object method that triggers navigation returns **nothing** (`None`).
- Never return the next Page Object; no fluent chaining across Page Objects.
- The test controls the flow and uses whichever Page Objects it needs from fixtures.

## A6. Authentication and login reuse

- Login is implemented **once**, in the `LoginPage` Page Object.
- All tests reuse that same method — no duplicated login locators anywhere.
- Tests needing an authenticated user get it via a fixture (UI login or saved storage state).
- Storage state files are never committed and never written to `report/`.

## A7. Fixtures

- Page Objects and components are provided through fixtures.
- Tests never instantiate a Page Object that a fixture already provides.

## A8. Test independence

- Every test runs on its own, in any order.
- No test relies on another test's browser state, data or output.
- Tests are linked only through shared Page Objects, components and fixtures.
- Browser / context / page cleanup is handled by fixtures — never add "close browser" steps to tests or test cases.

## A9. Test data and secrets

- Test data is referenced by **name** (e.g. `valid_username`, `valid_password`, `invalid_password`).
- Naming rule: the name in test cases (lowercase) is the `.env` variable in UPPERCASE
  (`valid_username` → `VALID_USERNAME`).
- Non-secret data sets live in `test_data/`.
- Secrets (passwords, tokens) come from **environment variables** only. Locally from a
  `.env` file that is never committed; in Jenkins from the Credentials store.
- Never hardcode credentials or concrete values in pages, tests or test cases.
- If a needed value is not defined, flag it: `Test data to confirm — not specified in test case`.

## A10. Traceability

- Each test maps to exactly one test case ID (`TC-x`) from `test_cases/*.md`.
- The TC ID appears in the test name and in the test's docstring, together with
  the test case file.

## A11. Waiting

- Rely on Playwright auto-waiting and web-first assertions.
- Never use fixed sleeps (`wait_for_timeout`, `time.sleep`) except as a documented last resort.
- Page-level waits (e.g. "dashboard loaded") belong in the Page Object.

## A12. No guessing

All work follows these rules:

- No expected result that doesn't trace to the test case → write
  `Expected result to confirm — not specified in test case`.
- No invented UI behaviour, error messages or data.
- Inferences are labelled as inferences.

## A13. Reusability

- Reuse existing Page Objects, components and methods before creating anything new.
- Never create a duplicate Page Object or component.
- Create a new one only when the test case needs something the framework lacks.

## A14. Generic folder structure

```text
pages/            BasePage + one Page Object per page (group by feature when the suite grows)
components/       shared UI components
tests/            test files (group by feature when the suite grows)
test_cases/       Markdown test cases
test_data/        named non-secret data sets
conftest.py       fixtures
pytest.ini        config and registered markers
```

Larger suites group by feature, e.g. `pages/admin/job_titles_page.py`, `tests/admin/test_job_titles.py`.

## A15. Tagging

Every test carries the tags listed in its test case (`Tags` field). Three kinds:

| Kind | Examples | Purpose |
|---|---|---|
| Module | `login`, `admin`, `pim`, `leave`, `time`, `my_info`, … | Run everything for one module (menu checks + that module's pages) |
| Area / suite | `left_menu`, `smoke`, `regression` | Run one UI area, or a CI suite |
| Priority | `p0`, `p1`, `p2` | Taken from the test case Priority |

Rules:

- Lowercase, underscores, no spaces (`My Info` → `my_info`).
- A test checking one module gets that module's tag — e.g. the left-menu check for Admin is
  tagged `left_menu` + `admin`. When one test case covers several modules, generate **one test
  per module** so each carries its own module tag.
- Every tag must be registered under `markers` in `pytest.ini` (`--strict-markers` is on,
  so an unregistered tag fails the run instead of being silently ignored).

| Action | Command / syntax |
|---|---|
| Tag a test | `@pytest.mark.admin` · per item: `pytest.param("Admin", marks=pytest.mark.admin)` |
| Run one tag | `pytest -m admin` |
| Both tags | `pytest -m "admin and left_menu"` |
| Either tag | `pytest -m "admin or leave"` |
| Exclude | `pytest -m "not regression"` |

---

# Part B — Python Conventions

## B1. Python (pytest + pytest-playwright, sync API)

| Item | Convention |
|---|---|
| Runner | pytest with the pytest-playwright plugin |
| API | **Sync** (`playwright.sync_api`) — no `async` / `await` |
| Page Object file | snake_case: `login_page.py`, `base_page.py` |
| Component file | snake_case: `side_menu.py`, `top_bar.py` |
| Class names | PascalCase: `LoginPage`, `SideMenu` |
| Locator / method names | snake_case: `username_input`, `login()` |
| Test file | must start with `test_`: `test_login.py` |
| Test function | must start with `test_`: `test_tc1_valid_login` |
| Fixtures file | `conftest.py` (root of tests) |
| Config | `pytest.ini` |
| Assertions | `expect` from `playwright.sync_api` |
| Locator API | `get_by_role`, `get_by_label`, `get_by_text`, `get_by_placeholder`, `get_by_test_id` |
| Traceability | docstring `"""TC-1 · test_cases/login.md"""` |
| Skip as app defect | `pytest.mark.skip(reason=...)` or `pytest.mark.xfail(reason=...)` |
| Type hints | Use them (`page: Page`, `-> None`) |

Locator declaration (illustrative only):

```python
class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
```

Notes:

- pytest-playwright provides the built-in `page`, `context` and `browser` fixtures; project
  fixtures in `conftest.py` build Page Objects on top of `page`.
- Authenticated state, when used, is supplied by overriding `browser_context_args` with a
  storage state file in `conftest.py`.
- Base URL and credentials come from `config.py` (credentials from `.env`), not from tests.

---

# Part D — Execution and Reporting

| Action | Command |
|---|---|
| Run one file | `pytest <test-file-path>` |
| Run all | `pytest` |
| Headed | `pytest --headed` |
| Pick browser | `pytest --browser chromium` |
| HTML report | `pytest --html=<path>/report.html --self-contained-html` (pytest-html) |
| Open HTML report | open the generated `report.html` |
| Allure results | `pytest --alluredir=allure-results` (allure-pytest) |
| Open Allure | `allure serve allure-results` |

Rules:

- Always use the **actual generated file path** — never a hardcoded filename.
- Use the reporting already configured in `pytest.ini`; don't change it unless asked.
- After a run, state which reports were generated and how to open them.
- In Jenkins, Allure is the primary report (pytest-html as well).

---

## Coding standards

- Clean, readable, meaningful names; no duplicated code.
- Avoid unnecessary comments — traceability docstrings are required, not optional.
- Keep Page Objects focused; keep business logic and assertions in tests.
- Follow Playwright (Python) best practices.