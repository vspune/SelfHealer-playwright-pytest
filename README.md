# SelfHealer-playwright-pytest

Python UI test automation framework: **Playwright + pytest** (sync API), Page Object Model,
role-based login, parallel runs, Chromium and Firefox, Allure / HTML reports with failure
screenshots, and a Jenkins pipeline. Target app: the OrangeHRM demo.

> Built with an AI-assisted workflow (locator discovery, test generation, test repair). The AI
> policy files are private and not part of this repository; the framework below runs without them.

**Highlights**

- Page Objects take only `page`: `BasePage(page)` → `LoginPage`, `DashboardPage`, …
- One `config.py` for URLs, page paths, credentials and per-role logins
- `@pytest.mark.role("ess")` + `pytest --role ess` to run as a given user role
- Parallel (`-n`), cross-browser (`--browser`), markers for suite / priority / module
- Failure screenshots and logs attached to the Allure and HTML reports
- Jenkins: runs on every commit and nightly, on Chromium and Firefox

---

## AI-assisted workflow (not included)

This project was built with Claude Code guided by private policy files (`agents/`, `guardrails/`,
`skills/`), which are not published. **If you fork this project and want the same workflow,
create your own:**

- **Test Generator agent** — turns a Markdown test case into a Page Object and tests (reuse
  existing pages, find real locators first, never invent data).
- **Healer agent** — fixes a failing test (separate automation issues from application defects,
  fix locators only, never weaken or remove assertions).
- **Guardrails** — never invent locators, data or expected results; flag gaps instead; a
  readiness checklist before generating tests.

The framework itself runs without any of this.

---

## Setup

Prerequisites: Python 3.10+, Git, VS Code (recommended).

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
```

Verify:
```bash
python -m pip show playwright pytest-playwright
pytest --version
```

Optional / later:
- **Allure CLI** (needs Java) — to open Allure reports locally. Jenkins provides it via the Allure plugin.

---

## Configuration, secrets and test data

All URLs and logins are in **one place: `config.py`** (project root).

| What | Where |
|---|---|
| Base URL and page paths (`LOGIN_PATH`, `DASHBOARD_PATH`, `ADMIN_USERS_PATH`) | `config.py` (not secret) |
| Credentials (`VALID_USERNAME`, `VALID_PASSWORD`, `INVALID_PASSWORD`) | local `.env` (never committed; Jenkins Credentials in CI), read by `config.py` |
| Logins per role (`config.USERS`: `admin`, `ess`) | `config.py` — `ess` reuses the admin login until a real normal user exists |

- Copy `.env.example` to `.env` and fill in the three credential values.
- Tests, pages and test cases refer to values **by name** (e.g. `valid_username` → `VALID_USERNAME`), never raw values.
- Session / storage-state files (`*.storage.json`) are never committed.

### Fixtures and the `page`

`page` (browser → context → page, one per test, safe for `-n` parallel runs) comes from the
**pytest-playwright** plugin. `tests/conftest.py` wraps it into page objects
(`LoginPage(page)`, `DashboardPage(page)`, …) and passes them to tests as fixtures.
Page classes never create a `Page`; they receive it in `__init__`.

### Running as a role

`logged_in_page` logs in as **admin** by default. Tag a test to run as another role:

```python
@pytest.mark.role("ess")
def test_something(logged_in_page): ...
```

The tag selects the login from `config.USERS`. An unknown role fails with `KeyError`.

**Example in use:** `test_tc3_dashboard_is_the_only_active_menu_item` in
`tests/test_dashboard.py` is tagged `@pytest.mark.role("ess")`, so it runs as the normal user
(currently the same login as admin). All other tests run as admin. Run only it with:

```bash
pytest tests/test_dashboard.py::test_tc3_dashboard_is_the_only_active_menu_item
pytest --role ess           # every test tagged @pytest.mark.role("ess")
```

`--role <name>` is a custom option (`tests/conftest.py`) that keeps only tests whose
`role("<name>")` tag matches. (`-m` can't do this: it matches marker names, not their arguments.)
It combines with other filters, e.g. `pytest --role ess -m smoke`.

When a real normal user exists, change only the `ess` entry in `config.USERS` — the tagged tests
need no edits.

### Logging and failure screenshots

- Logs: use `from utilities.logger import get_logger` then `log = get_logger(__name__)`. Level and
  format come from `pytest.ini`; logs show live in the console and are attached per test in the reports.
  Never log passwords.
- On any failed test (including a failed login fixture) a full-page screenshot is attached to the
  **Allure** and **HTML** reports (`utilities/screenshot.py`, hooked in `tests/conftest.py`).
  Traces are kept on failure (`--tracing=retain-on-failure`).

---

## Adding a new page

1. **Write the test cases** in `test_cases/<feature>.md` (copy `test_cases/_TEMPLATE.md`): an ID per
   case (`TC-1`…), steps, an expected result per step, priority, tags, and test data *names*
   (never real values). Write "To confirm" for anything you are not sure about.
2. **Add a Page Object** in `pages/` (extend `BasePage`, take `page` in `__init__`). Locators are
   named by purpose and use role / label / placeholder / text before CSS. Put the page path in
   `config.py`.
3. **Add a fixture** for it in `tests/conftest.py`: `return MyPage(page)`.
4. **Write the tests** in `tests/`, one test per TC ID, with the docstring
   `"""TC-1 · test_cases/<feature>.md"""` and markers (`smoke`, `p0`, module tag, …).
5. **Run** `pytest tests/test_<feature>.py`, then commit.

See `docs/POM.md` for the full coding rules.

---

## Run tests

```bash
pytest                                   # all tests
pytest tests/test_login.py               # one file
pytest tests/test_login.py::test_tc1_x   # one test
pytest --headed                          # see the browser
pytest --browser firefox                 # pick the browser (default chromium)
pytest --role ess                        # only tests tagged @pytest.mark.role("ess")
pytest tests/test_dashboard.py -n 2 --browser chromium --headed   # 2 parallel workers, visible
pytest --html=html-report/report.html --self-contained-html
pytest --alluredir=allure-results
pytest -n 2 -m p1 tests/admin/test_user_management.py
allure serve allure-results              # needs Allure CLI
```

### Browsers

Chromium is the default. Pick another browser from the command line (no code change):

```bash
python -m playwright install firefox webkit      # one-time download
pytest --browser firefox
pytest --browser chromium --browser firefox      # run the suite on both
pytest --browser webkit
```

Verified: the `ess`-tagged dashboard test passes on Firefox. The full suite has only been run on Chromium.

> If `pytest` fails with *"Fatal error in launcher"*, the virtual environment was moved/copied and
> its launchers point at the old path. Run `python -m pytest ...` instead, or recreate the venv
> (see Setup). There is no `--headless` option: tests are headless by default, `--headed` shows the browser.

### Markers (tags)

Markers are **registered in `pytest.ini`** (`--strict-markers` is on, so an unregistered marker
fails the run) and **applied on tests** with `@pytest.mark.<name>` or `pytest.param(..., marks=...)`.

| Kind | Markers |
|---|---|
| Suite | `smoke`, `regression` |
| Priority | `p0`, `p1`, `p2` |
| Module | `login`, `admin`, `pim`, `leave`, `time`, `recruitment`, `my_info`, `performance`, `dashboard`, `directory`, `maintenance`, `claim`, `buzz` |
| Feature | `left_menu` |
| Role | `role("<name>")` — which user the test logs in as (default `admin`) |

Run by tag (see `docs/POM.md` A15):

```bash
pytest -m smoke                       # smoke suite
pytest -m admin                       # everything for the Admin module
pytest -m "left_menu and admin"       # only the Admin left-menu check
pytest -m left_menu                   # whole left menu
```

To add a new marker, register it in the `markers =` list in `pytest.ini`, then use it on tests.
Note: `-m` filters on tags such as `smoke`; the `role` marker only selects the login.

---

## Jenkins (CI)

One pipeline: `ci/Jenkinsfile`, used by a **multibranch pipeline** job on a **Windows** agent
(Script Path `ci/Jenkinsfile`, source = this GitHub repo).

| Trigger | When | What runs |
|---|---|---|
| Commit / push | GitHub webhook, any branch | Full suite on **Chromium and Firefox** (in parallel) |
| Nightly cron | Only on the `nightly` branch, `H 2 * * *` (about 2 AM) | Same |

- Change the cron branch name or time at the top of `ci/Jenkinsfile` (`NIGHTLY_BRANCH`, `cron(...)`).
- Each browser writes its own reports: `html-report/<browser>.html`, `allure-results/<browser>`,
  `junit/<browser>.xml`, so the two runs never overwrite each other.
- Jenkins credentials to create (kind *Secret text*): `orangehrm-valid-username` → `VALID_USERNAME`,
  `orangehrm-valid-password` → `VALID_PASSWORD`, `orangehrm-invalid-password` → `INVALID_PASSWORD`.
  The pipeline exposes them as the environment
  variables `config.py` reads; no `.env` is needed on the agent.
- **Public repo:** in the Jenkins GitHub source, set trust for pull requests from forks to *Nobody* (or *Collaborators*), so a fork's Jenkinsfile can never run with your credentials.
- Agent needs: Python 3.10+ on `PATH`, Git, and the Jenkins Allure plugin.
- Setup stage: creates `.venv`, installs `requirements.txt`, runs `playwright install chromium firefox`.

---

## Folder map

```text
SelfHealer-playwright-pytest/
├── README.md, requirements.txt, pytest.ini, LICENSE, .gitignore
├── config.py             URLs, page paths, credentials (from .env), users per role
├── .env.example          template for the local .env (.env is never committed)
├── docs/                 POM.md — coding rules
├── test_cases/           Markdown test cases
├── pages/  components/   page objects (BasePage(page) → LoginPage, …) and reusable UI parts
├── tests/                tests + conftest.py (page-object fixtures, login/role, failure screenshot hook)
├── utilities/            logger.py, screenshot.py — shared helpers
└── ci/                   Jenkinsfile
```

---

## Team rules

- Python only. Don't mix languages.
- Tests and pages are always separate files.
- Never invent locators, data or expected results — flag gaps instead.
- Small, reviewable changes through Git.

## License and copyright

© 2026 Vaibhav Sharma. All rights reserved.

This repository is public for viewing and evaluation only. No license is granted to copy, modify,
redistribute or reuse the code, in whole or in part, without written permission.

## Target application

OrangeHRM demo: https://opensource-demo.orangehrmlive.com (Login, Dashboard, Admin → User Management).
