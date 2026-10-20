from pathlib import Path

LOG_FILE = (
    Path(__file__).resolve().parent.parent
    / "sample_app"
    / "logs"
    / "app.log"
)

def read_logs()->str:
    """Read application logs for investigation"""

    if not LOG_FILE.exists():
        return "No log file found."

    return LOG_FILE.read_text(encoding="utf-8")


def search_logs(keyword: str)->str:
    """Search application logs for a keyword"""

    logs = read_logs()

    matching_lines = []

    for line in logs.splitlines():
        if keyword.lower() in line.lower():
            matching_lines.append(line)

    if not matching_lines:
        return "No matching logs found"

    return "\n".join(matching_lines)

if __name__ == "__main__":
    print(search_logs("pool exhausted"))