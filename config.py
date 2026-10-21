import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

# ---------------------------------------------------------------------------
# One place for every environment: its URL and the logins per role.
# Logins are listed by the NAME of the environment variables that hold them;
# the values live in .env (local) or Jenkins Credentials (CI) - never here.
#
#   logins : role -> (username variable, password variable)
#            A test uses @pytest.mark.role("<role>"); no tag = "admin".
#            A test whose role has no login in the chosen environment is skipped.
# ---------------------------------------------------------------------------
ENVIRONMENTS = {
    "qa": {
        "base_url": "https://opensource-demo.orangehrmlive.com",
        "logins": {
            "admin": ("QA_ADMIN_USERNAME", "QA_ADMIN_PASSWORD"),
            "normal": ("QA_ADMIN_USERNAME", "QA_ADMIN_PASSWORD"),  # TODO: real normal QA user
        },
    },
    "uat": {
        "base_url": "",  # TODO: set the UAT URL
        "logins": {
            "normal": ("UAT_NORMAL_USERNAME", "UAT_NORMAL_PASSWORD"),
        },
    },
    "preprod": {
        "base_url": "",  # TODO: set the pre-production URL
        "logins": {
            "normal": ("PREPROD_NORMAL_USERNAME", "PREPROD_NORMAL_PASSWORD"),
        },
    },
}

# Page paths (same on every environment)
LOGIN_PATH = "/web/index.php/auth/login"
DASHBOARD_PATH = "/web/index.php/dashboard/index"
ADMIN_USERS_PATH = "/web/index.php/admin/viewSystemUsers"

# Used by the negative login test; not tied to an environment
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD")


def _env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name} (set it in .env / Jenkins)")
    return value


# Selected environment. Filled in by use(), which tests/conftest.py calls with the --env option.
TARGET_ENV = None
ENV = None
BASE_URL = None
USERS = {}


def use(env_name: str) -> None:
    """Select the environment: its URL and the logins (read from environment variables)."""
    global TARGET_ENV, ENV, BASE_URL, USERS
    name = env_name.strip().lower()
    if name not in ENVIRONMENTS:
        raise RuntimeError(f"--env must be one of {list(ENVIRONMENTS)}, got '{name}'")
    env = ENVIRONMENTS[name]
    if not env["base_url"]:
        raise RuntimeError(f"base_url for '{name}' is not set in config.py")
    TARGET_ENV, ENV = name, env
    BASE_URL = env["base_url"].rstrip("/")
    USERS = {
        role: {"username": _env(user_var), "password": _env(password_var)}
        for role, (user_var, password_var) in env["logins"].items()
    }
