import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from evals_demo_app.agents.health.nutrition_agent import get_nutrition_information
from evals_demo_app.agents.health.recovery_agent import get_recovery_information
from evals_demo_app.agents.races.races_agent import get_races
from evals_demo_app.agents.shoes_and_apparel.apparel_agent import (
    get_apparel_information,
)
from evals_demo_app.agents.shoes_and_apparel.brand_agent import get_brand_information
from evals_demo_app.agents.shoes_and_apparel.shoe_agent import get_shoe_information
from evals_demo_app.agents.training.training_agent import get_training_advice


def create_running_research_agent():
    """
    Create and return the running research agent.
    """
    return create_agent(
        tools=[
            get_nutrition_information,
            get_recovery_information,
            get_races,
            get_apparel_information,
            get_brand_information,
            get_shoe_information,
            get_training_advice,
        ],
        model=ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), name="running-research-agent"
        ),
        name="agent",
        system_prompt="""
        You are a research agent that can research information related to running. This includes:
        - Shoes
        - Apparel
        - Brands for shoes and apparel
        - Nutrition for runners
        - Training plans and advice for runners

        Use the tools available to you to research the user's queries and provide a concise summary of your findings.
        Only use information from the tools available to you.

        Make sure markdown is correctly used, and any image links are properly formatted as markdown.

        When you create a summary, be positive and encouraging, ensuring the user feels loved and well supported on their running journey.
        """,
    )
