from tests.experiments.run_experiment_for_dataset import run_experiment_for_dataset

def test_inputs_without_failures():
    """
    Test for inputs that should not cause failures for the grounding metric to score the TPR of the metric.
    """

    score = run_experiment_for_dataset(
        dataset_name="no-fail-test",
        experiment_name="True Positive Rate Unit Test",
    )

    assert score > 0.9