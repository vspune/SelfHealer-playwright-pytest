# SelfHealer-playwright-pytest

Python UI test automation framework: **Playwright + pytest** (sync API), Page Object Model,
role-based login, parallel runs, Chromium and Firefox, Allure / HTML reports with failure
screenshots, and a Jenkins pipeline. Target app: the OrangeHRM demo.

> Built with an AI-assisted workflow (locator discovery, test generation, test repair). The AI
> policy files are private and not part of this repository; the framework below runs without them.

**Highlights**

- Page Objects take only `page`: `BasePage(page)` → `LoginPage`, `DashboardPage`, …
- One `config.py` for URLs, page paths, credentials and per-role logins
- `@pytest.mark.role("normal")` + `pytest --role normal` to run as a given user role
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

Everything about environments is in **one file: `config.py`**.

| Environment | URL | Logins (roles) | Tag Jenkins runs |
|---|---|---|---|
| `qa` (default) | the demo URL, set in `config.py` | `admin`, `normal` | `smoke` |
| `uat` | `TODO` — set in `config.py` | `normal` | `regression` |
| `preprod` | `TODO` — set in `config.py` | `normal` | `regression` |

- Page paths (`LOGIN_PATH`, `DASHBOARD_PATH`, `ADMIN_USERS_PATH`) are in `config.py` too.
- Logins are listed in `config.py` by the **names** of the variables that hold them, e.g.
  `QA_ADMIN_USERNAME` / `QA_ADMIN_PASSWORD`, `UAT_NORMAL_USERNAME`, `PREPROD_NORMAL_PASSWORD`. The
  **values** live in a local `.env` (copy `.env.example`; never committed) and in Jenkins Credentials in CI.
- `QA normal` reuses the admin variables until a real normal QA user exists (see the `TODO` in `config.py`).
- Choose the environment with **`--env qa | uat | preprod`** (default `qa`), the role with
  **`--role admin | normal`**, and the tests with **`--marker <tag>`** (same as `-m`). For example:
  ```bash
  python -m pytest --env qa --role admin --marker smoke
  python -m pytest --env uat --role normal --marker regression
  ```
- The tag per environment (`qa` → `smoke`, `uat` / `preprod` → `regression`) is set in the `Jenkinsfile`;
  locally you choose it yourself with `--marker`.
- **This repository is public.** Never commit real credentials, tokens or internal URLs: logins are
  referenced by variable name only, `.env` is git-ignored, and Jenkins keeps the real values as Credentials.
- Tests, pages and test cases refer to values **by name**, never raw values.
- Session / storage-state files (`*.storage.json`) are never committed.

### Fixtures and the `page`

`page` (browser → context → page, one per test, safe for `-n` parallel runs) comes from the
**pytest-playwright** plugin. `tests/conftest.py` wraps it into page objects
(`LoginPage(page)`, `DashboardPage(page)`, …) and passes them to tests as fixtures.
Page classes never create a `Page`; they receive it in `__init__`.

### Running as a role

`logged_in_page` logs in as **admin** by default. Tag a test to run as another role:

```python
@pytest.mark.role("normal")
def test_something(logged_in_page): ...
```

The role is looked up in the chosen environment's logins in `config.py`. A test whose role has no
login in that environment (e.g. an `admin` test on `uat`) is skipped automatically.

**Example in use:** `test_tc3_dashboard_is_the_only_active_menu_item` in `tests/test_dashboard.py`
is tagged `@pytest.mark.role("normal")`. All other tests run as admin. Run only it with:

```bash
pytest --role normal        # every test tagged @pytest.mark.role("normal")
```

`--role <name>` is a custom option (`tests/conftest.py`); `-m` can't do this because it matches
marker names, not their arguments. It combines with other filters, e.g. `pytest --role normal -m smoke`.

### Examples: admin and normal (non-admin) users

Illustrative tests (the roles and their logins are defined per environment in `config.py`):

```python
# No role tag = admin
@pytest.mark.smoke
def test_admin_can_open_user_management(logged_in_page, side_menu, user_management_page):
    user_management_page.open_from_menu(side_menu)

# Runs as the normal (non-admin) user
@pytest.mark.role("normal")
@pytest.mark.regression
def test_normal_user_sees_dashboard(logged_in_page, dashboard_page):
    dashboard_page.wait_until_loaded()
```

Commands (same in PowerShell, bash and Git Bash):

```bash
python -m pytest                                            # QA, every test (admin and normal)
python -m pytest --env qa --role admin                      # QA, admin tests only (untagged ones)
python -m pytest --env qa --role normal                     # QA, normal-user tests only
python -m pytest --env qa --role admin --marker smoke       # QA, admin smoke tests
python -m pytest --env qa --marker "smoke and admin"        # any tag expression works
python -m pytest --env uat --role normal --marker regression       # UAT, regression tests as the normal user
python -m pytest --env preprod --role normal --marker regression   # PreProd, regression tests as the normal user
```

(`uat` and `preprod` need their URL set in `config.py` first.)

On `uat` and `preprod` only the `normal` login exists in `config.py`, so tests that need `admin` are
skipped there automatically.

### Logging and failure screenshots

- Logs: use `from utilities.logger import get_logger` then `log = get_logger(__name__)`. Level and
  format come from `pytest.ini`; logs show live in the console and are attached per test in the reports.
  Never log passwords.
- On any failed test (including a failed login fixture) a full-page screenshot is attached to the
  **Allure** and **HTML** reports (`utilities/screenshot.py`, hooked in `tests/conftest.py`).
  Traces are kept on failure (`--tracing=retain-on-failure`).

### Reports

Every run writes reports; a failed test also gets a full-page screenshot attached.

| Report | Where (local) | Where (Jenkins) |
|---|---|---|
| HTML (self-contained) | `html-report/report.html` | `html-report/<env>-<browser>.html`, archived with the build |
| Allure results | `allure-results/` (`allure serve allure-results`, needs the Allure CLI) | `allure-results/<env>-<browser>`, shown by the Allure plugin on the build page |
| JUnit XML | — | `junit/<env>-<browser>.xml`, drives the test trend graph |
| Traces (failures only) | `test-results/` | archived with the build |

**E-mail report (Jenkins):** after each run the `Jenkinsfile` e-mails the result (status, which
environment + browser runs, links to the build and the Allure report, the HTML reports attached)
when a build is **not successful**, and after **every nightly run**. Passing commit builds send nothing.

To switch it on (nothing secret goes in this public repo):
1. Install the **Email Extension** plugin and set up SMTP (Manage Jenkins → System).
2. Add a global variable `REPORT_RECIPIENTS` (Manage Jenkins → System → Global properties →
   Environment variables) with the comma-separated addresses.

If either is missing, the e-mail step is skipped and the build result is not affected.
Slack / Teams notifications are not built.

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
pytest --role normal                     # only tests tagged @pytest.mark.role("normal")
pytest tests/test_dashboard.py -n 2 --browser chromium --headed   # 2 parallel workers, visible
pytest --html=html-report/report.html --self-contained-html
pytest --alluredir=allure-results
pytest -n 2 -m p1 tests/admin/test_user_management.py
allure serve allure-results              # needs Allure CLI
```

### Local vs Jenkins

| | On your machine | In Jenkins |
|---|---|---|
| Who runs the tests | **You**, by typing the command | **The `Jenkinsfile`**, automatically on a trigger (commit, nightly cron, or a manual build) |
| Choosing the environment | `--env uat` (default `qa`) | The `Jenkinsfile` passes `--env <name>` for each stage |
| Choosing the tests | `--marker <tag>` (or `-m`) and `--role` | The `Jenkinsfile` passes `--marker` (your `MARKER` parameter, or the environment's tag) and `--role` |
| Secrets | your local `.env` | Jenkins Credentials |

So the commands in this README are for running locally; in Jenkins nobody types them, because the
`Jenkinsfile` builds the same `pytest` command itself.

### Browsers

Chromium is the default. Pick another browser from the command line (no code change):

```bash
python -m playwright install firefox webkit      # one-time download
pytest --browser firefox
pytest --browser chromium --browser firefox      # run the suite on both
pytest --browser webkit
```

Verified: the `normal`-tagged dashboard test passes on Firefox. The full suite has only been run on Chromium.

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
(Script Path `ci/Jenkinsfile`, source = this GitHub repo, branch scan every 2 minutes).

There is one stage per environment. Each build runs the stage chosen by its trigger; moving a build from one
environment to the next is a **human step** (deployment is outside this pipeline).

```text
Commit:   QA (smoke)
Nightly:  UAT (regression)
Manual:   PREPROD (regression), run after a person has deployed to PreProd
```

| Trigger | Stages that run | Tag |
|---|---|---|
| Commit / push | `QA` | `smoke` |
| Nightly cron (`master` branch, `H 2 * * *`, about 2 AM) | `UAT` | `regression` |
| Manual **Build with Parameters** | `QA`, or the `TARGET_ENV` you pick (e.g. `preprod` after a person deployed) | `MARKER` you type, or the environment's tag |

Inside each stage the tests run on **Chromium and Firefox** in parallel.

- **Parameters:** `TARGET_ENV` (`auto` = by trigger, or `qa` / `uat` / `preprod`), `MARKER` (a pytest `-m` expression, e.g.
  `smoke`, `p0`, `smoke and admin`; overrides the environment's tag) and `ROLE` (e.g. `normal`). They appear
  after the first build that runs this Jenkinsfile.
- **Where the logic lives:** which environment runs, and its tag, is decided in `ci/Jenkinsfile`;
  each environment's URL and logins are only in `config.py`.
- **Promotion is a human step.** When UAT passes, a person (dev / release manager) deploys the build to
  PreProd, then the PreProd tests are started with **Build with Parameters** → `TARGET_ENV=preprod`.
- **Deployment is not part of this pipeline.** A separate process, owned by the dev / DevOps team,
  puts the build on QA, UAT and PreProd. This pipeline only **verifies** an environment that is already
  deployed. A deploy job can start it for a given environment with the `TARGET_ENV` parameter, e.g.
  `curl -X POST -u <user>:<api-token> ".../job/SelfHealer-playwright-pytest/job/master/buildWithParameters?TARGET_ENV=preprod"`.
- **No tests selected** (for example no test carries the tag) is not a failure.
- Each run writes its own reports: `html-report/<env>-<browser>.html`,
  `allure-results/<env>-<browser>`, `junit/<env>-<browser>.xml`.
- **Jenkins credentials** (kind *Secret text*): `orangehrm-invalid-password` → `INVALID_PASSWORD`;
  `orangehrm-valid-username` / `orangehrm-valid-password` → `QA_ADMIN_USERNAME` / `QA_ADMIN_PASSWORD`;
  `orangehrm-uat-normal-username` / `-password` → `UAT_NORMAL_USERNAME` / `UAT_NORMAL_PASSWORD`;
  `orangehrm-preprod-normal-username` / `-password` → `PREPROD_NORMAL_USERNAME` / `PREPROD_NORMAL_PASSWORD`.
  No `.env` is needed on the agent.
- **How a change reaches UAT:** a QA engineer pushes a branch (a commit run checks it on QA), it is
  merged to `master`, and that night the cron on `master` runs the merged tests against UAT.
- Change the cron branch or time at the top of `ci/Jenkinsfile` (`NIGHTLY_BRANCH`, `cron(...)`).
- **Public repo:** in the Jenkins GitHub source, set trust for pull requests from forks to *Nobody*
  (or *Collaborators*), so a fork's Jenkinsfile can never run with your credentials.
- Agent needs: Python 3.10+ on `PATH`, Git, and the Jenkins Allure plugin.
- Setup stage: creates `.venv`, installs `requirements.txt`, runs `playwright install chromium firefox`.
- Not built yet: the `uat` and `preprod` URLs (the OrangeHRM demo has no
  UAT or production).

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
