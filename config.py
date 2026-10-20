import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def _env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name} (set it in .env)")
    return value


# URLs
BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_PATH = "/web/index.php/auth/login"
DASHBOARD_PATH = "/web/index.php/dashboard/index"
ADMIN_USERS_PATH = "/web/index.php/admin/viewSystemUsers"

# Credentials (values live in .env)
VALID_USERNAME = _env("VALID_USERNAME")
VALID_PASSWORD = _env("VALID_PASSWORD")
INVALID_PASSWORD = _env("INVALID_PASSWORD")

# Login per role, picked by @pytest.mark.role("<name>") (default: admin).
# ESS reuses the admin login for now; point it at a real normal user later.
USERS = {
    "admin": {"username": VALID_USERNAME, "password": VALID_PASSWORD},
    "ess": {"username": VALID_USERNAME, "password": VALID_PASSWORD},
}
