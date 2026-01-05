import json

from datetime import datetime
from typing import Any

from dotenv import load_dotenv

from galileo import galileo_context
from galileo.handlers.langchain import GalileoCallback
from galileo.config import GalileoPythonConfig

from langchain_core.runnables.config import RunnableConfig
from langchain_core.callbacks import Callbacks
from langchain_core.messages import HumanMessage

from evals_demo_app.agents.research.research_agent import create_running_research_agent

DATASET_NAMEs = ["good-inputs", "bad-inputs"]

dataset_logstreams = {}

# Load the environment variables
load_dotenv(override=True)

# Process each dataset
for dataset_name in DATASET_NAMEs:
    print(f"Starting processing for dataset: {dataset_name}")

    # Initialize Galileo with the current project, and a new log stream for each dataset
    galileo_context.init(project="EvalsCourse", log_stream=f"runzi-{dataset_name}")

    # Get the Log stream name from the Galileo config for this dataset
    config = GalileoPythonConfig.get()
    logger = galileo_context.get_logger_instance()
    project_url = f"{config.console_url}project/{logger.project_id}"
    log_stream_url = f"{project_url}/log-streams/{logger.log_stream_id}"

    dataset_logstreams[dataset_name] = log_stream_url

    # Load the dataset
    with open(f"./datasets/{dataset_name}.json", "r", encoding="utf-8") as f:
        dataset_content = json.load(f)

    # Loop through each row in the dataset
    for rows in dataset_content:
        print(f"\tProcessing input: {rows['input']}")

        # Create a new session for each row
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_name = f"Runzi - {current_time}"
        session_id = galileo_context.start_session(name=session_name)

        # Create the callback to log to Galileo
        galileo_callback = GalileoCallback()
        callbacks: Callbacks = [galileo_callback]  # type: ignore

        # Set up the config for the streaming response
        runnable_config = RunnableConfig(callbacks=callbacks)

        # Build the agent graph
        supervisor_agent = create_running_research_agent()

        # Run each line in the input as a message in the current session
        for item in rows["input"]:
            messages: dict[str, Any] = {"messages": [HumanMessage(content=item)]}
            supervisor_agent.invoke(input=messages, config=runnable_config)


# Print the log stream URLs for each dataset
for dataset_name, log_stream_url in dataset_logstreams.items():
    print(f"Dataset: {dataset_name} - Log Stream URL: {log_stream_url}")
