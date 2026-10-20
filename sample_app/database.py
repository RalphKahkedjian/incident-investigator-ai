
import time


class DatabaseConnectionError(Exception):
    pass


def connect_to_database(scenario: str = "normal"):
    time.sleep(0.5)

    if scenario == "timeout":
        raise DatabaseConnectionError(
            "Database connection timed out after 500ms"
        )

    if scenario == "pool_exhausted":
        raise DatabaseConnectionError(
            "Database connection pool exhausted"
        )

    if scenario == "normal":
        raise DatabaseConnectionError(
            "Database connection failed: invalid pool configuration"
        )

    raise ValueError(f"Unknown database scenario: {scenario}")
