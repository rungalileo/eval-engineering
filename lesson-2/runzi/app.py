"""
Chainlit app entry point.
"""

from datetime import datetime
from typing import Any
import chainlit as cl
from dotenv import load_dotenv

from galileo import galileo_context
from galileo.handlers.langchain import GalileoAsyncCallback

from langchain_core.runnables.config import RunnableConfig
from langchain_core.callbacks import Callbacks
from langchain_core.messages import HumanMessage, AIMessage

from evals_demo_app.agents.research.research_agent import create_running_research_agent

# Load the environment variables
load_dotenv(override=True)

# Build the agent graph
supervisor_agent = create_running_research_agent()

galileo_context.init(project="EvalsCourse", log_stream="runzi")

def create_galileo_session():
    """
    Create a new Galileo session for tracking user interactions.

    This session is then stored in the Chainlit user session for later use.
    """
    try:
        # Start Galileo session with unique session name
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_name = f"Runzi - {current_time}"
        galileo_context.start_session(
            name=session_name, external_id=cl.context.session.id
        )

        # Create the callback. This needs to be created in the same thread as the session
        # so that it uses the same session context.
        galileo_callback = GalileoAsyncCallback()
        cl.user_session.set("galileo_callback", galileo_callback)

        # Store session info in user session for later use
        cl.user_session.set("galileo_session_started", True)
        cl.user_session.set("session_name", session_name)

        print(f"✅ Galileo session started: {session_name}")

    except Exception as e:
        print(f"❌ Failed to start Galileo session: {str(e)}")
        # Continue without Galileo rather than failing completely
        cl.user_session.set("galileo_session_started", False)


@cl.on_chat_start
def start_chat():
    """
    Initialize the chat session.
    """
    create_galileo_session()


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the Chainlit UI.
    """
    # Create a config using the current Chainlit session ID. This is linked to the memory saver in the graph
    # to allow you to continue the conversation with the same context.
    config: dict[str, Any] = {"configurable": {"thread_id": cl.context.session.id}}

    # Prepare the final answer message to stream the response back to the user
    final_answer = cl.Message(content="")

    # Build the messages dictionary with the user's message
    messages: dict[str, Any] = {"messages": [HumanMessage(content=message.content)]}

    # Create a callback handler to log the response to Galileo
    callbacks: Callbacks = []
    if cl.user_session.get("galileo_session_started", False):
        galileo_callback = cl.user_session.get("galileo_callback")
        callbacks: Callbacks = [galileo_callback]  # type: ignore
    else:
        print("Galileo session not started, using default callbacks.")

    # Set up the config for the streaming response
    runnable_config = RunnableConfig(callbacks=callbacks, **config)

    # Call the graph with the user's message and stream the response back to the user
    async for response_msg in supervisor_agent.astream(
        input=messages, stream_mode="updates", config=runnable_config
    ):
        # Check for a response from the supervisor agent with the final message
        if (
            "model" in response_msg
            and "messages" in response_msg["model"]
            and response_msg["model"]["messages"][0].content
        ):
            # Get the last message from the supervisor's response
            response_message = response_msg["model"]["messages"][-1]
            # If it is an AI message, then it is the final answer
            if isinstance(response_message, AIMessage) and response_message.content:
                await final_answer.stream_token(response_message.content)  # type: ignore

    # Send the final answer message to the user
    await final_answer.send()


if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    run_chainlit(__file__)
