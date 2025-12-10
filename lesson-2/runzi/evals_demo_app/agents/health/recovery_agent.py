import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

recovery_agent = create_agent(
    name="agent",
    model=ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), name="recovery-assistant-agent"
    ),
    system_prompt="""
    You are a helpful recovery assistant agent. You assist users in finding recovery plans and advice
    based on their running needs.

    This includes:
    - Stretching routines
    - Foam rolling techniques
    - Rest day activities
    - Sleep optimization for recovery
    - Ice and heat therapy recommendations
    """,
)


@tool
def get_recovery_information(request: str) -> str:
    """Get recovery information based on user input.

    Use this to get details about recovery plans and advice, including stretching routines, foam rolling techniques, rest day activities, sleep optimization, and ice/heat therapy recommendations.

    Input: Natural language recovery request from the user, including all the details about what they are looking for.
    """
    result = recovery_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text
