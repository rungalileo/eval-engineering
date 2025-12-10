import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


nutrition_agent = create_agent(
    name="agent",
    model=ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), name="nutrition-assistant-agent"
    ),
    system_prompt="""
    You are a helpful nutrition assistant agent. You assist users in finding nutrition plans and advice
    based on their running needs. 

    This nutrition advice includes:
    - general healthy eating for endurance athletes
    - pre-race fueling
    - post-run recovery nutrition
    - fueling during long runs
        
    Be sure to take into account:
    - dietary restrictions, such as vegetarian, vegan, gluten-free, etc.
    - specific goals, such as weight loss, muscle gain, improved endurance, etc.
    - personal preferences, such as favorite foods, meal timing, etc.
    - The types of running they do (e.g., long-distance, sprinting, trail running, etc.)
    """,
)


@tool
def get_nutrition_information(request: str) -> str:
    """Get nutrition information based on user input.

    Use this to get details about nutrition plans and advice, including healthy eating
    for endurance athletes, pre-race fueling, post-run recovery nutrition, and fueling during long runs.

    Input: Natural language nutrition request from the user, including all the details about
    what they are looking for.
    """
    result = nutrition_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return result["messages"][-1].text
