from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from investigator.log_tools import read_logs, search_logs
from investigator.code_tools import list_directory, read_file

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

agent = create_agent(
    model=llm,
    tools=[read_application_logs,
           search_application_logs,
           list_application_directory,
           read_application_file
          ],
    system_prompt=system_prompt
)

if __name__ == "__main__":
    user_input = input("What would you like to investigate? ")

    response = agent.invoke({
        "messages": [{
            "role": "user",
            "content": user_input
        }]
    })

    print(10*"=" + "INVESTIGATION REPORT" + 10*"=")

    for message in response['messages']:
        print(f"Message type: {message.type}")

        if hasattr(message, "tool_calls") and message.tool_calls:
            for call in message.tool_calls:
                print(f"Tool called: {call['name']}")
                print(f"Args: {call['args']}")
    
    print(response["messages"][-1].text)

