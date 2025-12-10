import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


create_training_agent = create_agent(
    name="agent",
    model=ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), name="training-assistant-agent"
    ),
    system_prompt="""
    You are a helpful runner training assistant agent. You assist users in building training plans and advice
    based on their running needs. 

    This training advice includes:
    - Correct use of interval, VO2 max, tempo, threshold, and long runs
    - Advice on weekly mileage progression
    - Strength training recommendations
    - Rest and recovery strategies
        
    Be sure to take into account:
    - Physical characteristics, such as age, weight, injury history, etc.
    - Specific goals such as race distance, target finish time, etc.
    - Personal preferences, such as favorite types of runs, available training days, etc.
    - Available equipment and terrain (e.g., treadmill, trails, track, etc.)
    """,
)


@tool
def get_training_advice(request: str) -> str:
    """Get training advice for runners based on user input.

    Use this to get advice on training plans, workouts, recovery, etc.

    Input: Natural language training request from the user, including all the details about what they are training for, such as the race, terrain,
    time to the race, injuries, and any specific goals or preferences.
    """
    result = create_training_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return result["messages"][-1].text
