import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_git_history():
  result = subprocess.run(
    ["git", "log", "--oneline", "-5"],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
  )

  if result.returncode != 0:
    return f"Git error: {result.stderr}"

  return result.stdout


def get_commit_changes(commit_hash: str)->str:
  """Show the code changes introduced by a Git commit."""

  result = subprocess.run(
    ["git", "show", "--format=fuller", commit_hash],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
  )

  if result.returncode != 0:
    return f"Git error: {result.stderr}"

  return result.stdout

def compare_commits(old_commit:str, new_commit:str)->str:
  """Compare code changes between two Git commits"""

  result = subprocess.run(
    ["git", "diff", old_commit, new_commit, "--", "sample_app/"],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
  )

  if result.returncode != 0:
    return f"Git error: {result.stderr}"

  return result.stdout or "No differences found."

if __name__ == "__main__":
    print(compare_commits("51c779b", "aab34e2"))