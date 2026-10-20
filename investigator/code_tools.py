import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKING_DIR = PROJECT_ROOT / "sample_app"

def list_directory():
    files = []
    folders = []

    for item in os.listdir(WORKING_DIR):
        item_path = os.path.join(WORKING_DIR, item)

        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)

    return {
        "Folders": folders,
        "Files": files
    }


def read_file(filename: str):
    file_path = (WORKING_DIR / filename).resolve()

    if not file_path.is_relative_to(WORKING_DIR.resolve()):
        return "Access denied"

    if file_path.suffix not in [".py", ".log"]:
        return "Unsupported file type"

    if not os.path.isfile(file_path):
        return "File not found"

    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    print(read_file("database.py"))