from tests.experiments.run_experiment_for_dataset import run_experiment_for_dataset

def test_grounding_failures():
    """
    Test grounding failures experiment on the grounding_failures dataset to score the TNR of the metric.
    """

    score = run_experiment_for_dataset(
        dataset_name="grounding-data-test",
        experiment_name="True Negative Rate Unit Test",
    )

    assert (1 - score) > 0.9