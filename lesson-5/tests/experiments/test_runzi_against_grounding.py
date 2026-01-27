import json
import pytest
import time
from typing import Any

from galileo.datasets import create_dataset, get_dataset
from galileo.experiments import get_experiment, run_experiment
from galileo.handlers.langchain import GalileoCallback

from dotenv import load_dotenv

load_dotenv(override=True)

DATASET_NAME = "good-inputs-unit-tests"


@pytest.fixture
def create_dataset_for_unit_tests() -> None:
    """
    Create the dataset for the unit tests if it does not exist.
    """

    dataset = get_dataset(name=DATASET_NAME, project_name="EvalsCourse")

    if dataset is None:
        with open("./datasets/good-inputs.json", "r", encoding="utf-8") as f:
            file_dataset_content = json.load(f)

        # Just get the first 10 rows for unit tests
        file_dataset_content = file_dataset_content[:10]

        # Build the dataset content
        dataset_content = [{"input": row["input"][0]} for row in file_dataset_content]

        # Create the dataset
        dataset = create_dataset(
            name=DATASET_NAME, content=dataset_content, project_name="EvalsCourse"
        )


def experiment_function(input):
    """
    The experiment function that runs Runzi against the grounding metric.
    """
    from evals_demo_app.agents.research.research_agent import (
        create_running_research_agent,
    )
    from langchain_core.runnables.config import RunnableConfig
    from langchain_core.messages import HumanMessage

    # Create the agent
    supervisor_agent = create_running_research_agent()

    # Create the callback configured for experiments so it uses the existing trace
    galileo_callback = GalileoCallback(start_new_trace=False, flush_on_chain_end=False)
    callbacks = [galileo_callback]
    runnable_config = RunnableConfig(callbacks=callbacks)

    # Prepare the input message
    messages: dict[str, Any] = {"messages": [HumanMessage(content=input)]}

    # Invoke the agent with the input
    supervisor_agent.invoke(input=messages, config=runnable_config)


def test_runzi_against_grounding(create_dataset_for_unit_tests):
    """
    Test Runzi using a dataset against grounding metric to ensure it performs above a certain threshold.
    """
    # Run the experiment
    experiment_response = run_experiment(
        experiment_name="test_runzi_against_grounding",
        dataset_name=DATASET_NAME,
        function=experiment_function,
        project="EvalsCourse",
        metrics=["system_grounding_and_data_alignment"],
    )

    # Get the score
    experiment = get_experiment(
        project_id=experiment_response["experiment"].project_id,
        experiment_name=experiment_response["experiment"].name,
    )
    while (
        experiment.aggregate_metrics is None  # type: ignore
        or "average_system_grounding_and_data_alignment"
        not in experiment.aggregate_metrics  # type: ignore
    ):
        # If we don't have the metrics calculated, Sleep for 5 seconds before polling again
        time.sleep(5)

        # Reload the experiment to see if we have the metrics
        experiment = get_experiment(
            project_id=experiment_response["experiment"].project_id,
            experiment_name=experiment_response["experiment"].name,
        )

    score = experiment.aggregate_metrics["average_system_grounding_and_data_alignment"]
    assert score > 0.9
