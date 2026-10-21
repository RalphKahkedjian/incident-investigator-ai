from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from investigator.log_tools import read_logs, search_logs
from investigator.code_tools import list_directory, read_file
from investigator.git_tools import (
    get_git_history,
    get_commit_changes,
    compare_commits
)

from investigator.schemas import InvestigationReport

load_dotenv()

system_prompt="""
You are an expert AI Backend Incident Investigator.

Your job is to investigate application failures.

Follow these rules:
1. Use available tools to inspect application logs.
2. Identify errors and relevant Python tracebacks.
3. Explain the likely cause based on evidence.
4. Suggest possible solutions.
5. Never invent evidence or claim certainty without proof.
6. Clearly distinguish symptoms from verified root causes.

When investigating a possible regression:
1. Examine application logs to identify the failure.
2. Inspect source code for relevant behavior.
3. Check Git history for recent commits.
4. Compare relevant commits to identify code changes.
5. Cite the commit hash and changed file when explaining a regression.
6. Distinguish verified causes from hypotheses.
7. Never claim a commit caused a failure without supporting evidence.

Format your answer with:
- Problem
- Evidence
- Possible Root Cause
- Suggested Fix
"""

llm = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai"
)

@tool
def read_application_logs()->str:
    """Read the application logs to investigate errors"""
    return read_logs()

@tool
def search_application_logs(keyword:str)->str:
    """Search application logs for a specific keyword or error"""
    return search_logs(keyword)

@tool
def list_application_directory()->dict:
    """List available files and folders in the sample application"""
    return list_directory()

@tool
def read_application_file(filename:str)->str:
    """Read a python source file or log file from the sample application"""
    return read_file(filename)

@tool
def get_application_git_history() -> str:
    """Retrieve recent Git commits from the application repository."""
    return get_git_history()


@tool
def inspect_git_commit(commit_hash: str) -> str:
    """Inspect the code changes introduced by a Git commit."""
    return get_commit_changes(commit_hash)


@tool
def compare_git_commits(old_commit: str, new_commit: str) -> str:
    """Compare two Git commits to identify changes that may have introduced bugs."""
    return compare_commits(old_commit, new_commit)


agent = create_agent(
    model=llm,
    tools=[read_application_logs,
           search_application_logs,
           list_application_directory,
           read_application_file,
           get_application_git_history,
           inspect_git_commit,
           compare_git_commits
          ],
    system_prompt=system_prompt,
    response_format=InvestigationReport
)

if __name__ == "__main__":
    user_input = input("What would you like to investigate? ")

    response = agent.invoke({
        "messages": [{
            "role": "user",
            "content": user_input
        }]
    })

    for message in response['messages']:

        if hasattr(message, "tool_calls") and message.tool_calls:
            for call in message.tool_calls:
                print(f"Tool called: {call['name']}")
                print(f"Args: {call['args']}")

    report = response["structured_response"]
    print("\n" + 20*"=" + "INVESTIGATION REPORT" + 20*"=" + "\n")
    print(report.model_dump_json(indent=2))

