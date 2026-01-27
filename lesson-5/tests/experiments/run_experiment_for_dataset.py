import time
from galileo.datasets import get_dataset
from galileo.experiments import get_experiment, run_experiment

from dotenv import load_dotenv

load_dotenv(override=True)


def load_dataset(dataset_name: str) -> dict:
    """
    Loads a dataset into a dictionary to look up the outputs by input.

    :param dataset_name: The name of the dataset to load
    :type dataset_name: str
    """
    dataset = get_dataset(name=dataset_name, project_name="EvalsCourse")
    dataset_content = dataset.get_content()

    input_output_data = {}
    for row in dataset_content.rows:
        input = row.values_dict["input"]
        output = row.values_dict["output"]
        input_output_data[input] = output

    return input_output_data


# Load the input/output data for the dataset
dataset_data = {}


def simulate_agent(input: str) -> str:
    """
    A mock function to simulate the agent's response.
    This looks up the output from the appropriate dataset for the given input.

    :param input: The input to get the output for
    :type input: str
    :return: The relevant output message
    :rtype: str
    """
    return dataset_data[input]


def run_experiment_for_dataset(dataset_name: str, experiment_name: str) -> float:
    """
    Runs the experiment for the given dataset.

    :param dataset_name: The name of the dataset to run the experiment on
    :type dataset_name: str
    :param experiment_name: The name of the experiment to run
    :type experiment_name: str
    """
    global dataset_data

    # Load the input/output data for the dataset
    dataset_data = load_dataset(dataset_name)

    # Run the experiment
    experiment_response = run_experiment(
        experiment_name=f"{experiment_name} - {dataset_name}",
        dataset_name=dataset_name,
        function=simulate_agent,
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
        or "average_system_grounding_and_data_alignment" not in experiment.aggregate_metrics  # type: ignore
    ):
        # If we don't have the metrics calculated, Sleep for 5 seconds before polling again
        time.sleep(5)

        # Reload the experiment to see if we have the metrics
        experiment = get_experiment(
            project_id=experiment_response["experiment"].project_id,
            experiment_name=experiment_response["experiment"].name,
        )
    
    return experiment.aggregate_metrics["average_system_grounding_and_data_alignment"] 
