import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from evals_demo_app.tools.apparel_finder import (
    recommend_apparel,
    get_apparel_images,
)


apparel_agent = create_agent(
    tools=[recommend_apparel, get_apparel_images],
    name="agent",
    model=ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1"), name="apparel-finder-agent"
    ),
    system_prompt="""
    You are a helpful apparel recommendation agent. You assist users in finding clothing based on their preferences such as category, brand, intended use, size, and price. You can also provide image URLs for the recommended clothing.

    Use all the tools available to you to provide the best recommendations possible. These tools only
    provide details of brands we have available. Other brands are available outside of this system.
    """,
)


@tool
def get_apparel_information(request: str) -> str:
    """Get information and images for running clothing and accessories based on user input.

    Use this to get clothing recommendations and images, based off details such as category, brand, intended use, size, and price.

    Input: Natural language clothing request from the user, including all the details about what they are looking for, such as the type of clothing, brand preferences, and any specific features they need.
    """
    result = apparel_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text
