
import logging
from pathlib import Path
from database import connect_to_database, DatabaseConnectionError

# Configure application logging
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def login(username: str, password: str, scenario: str = "normal"):
    logger.info("Login attempt for user: %s", username)

    try:
        connect_to_database(scenario)

        if username == "admin" and password == "1234":
            logger.info("Login successful for user: %s", username)
            return True

        if username == "admin":
            logger.error("Invalid password for admin: %s", username)
            return False

        logger.error("Login failed for user: %s", username)
        return False
    except DatabaseConnectionError:
        logger.exception(
            "Login failed due to database connection error"
        )
        return False


if __name__ == "__main__":
    login("admin", "1234", "normal")
    login("ralph", "wrongpassword", "timeout")
    login("admin", "1234", "pool_exhausted")
