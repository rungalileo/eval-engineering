from galileo import GalileoMetrics
from galileo.prompts import get_prompt
from galileo.resources.models.prompt_run_settings import PromptRunSettings
from galileo.experiments import run_experiment

from dotenv import load_dotenv

load_dotenv()

# Get the prompt
prompt = get_prompt(name="nutrition-agent-prompt")

# Build the prompt run settings
prompt_run_settings = PromptRunSettings(
    model_alias="gpt-5-mini"
)

# Run the experiment
experiment_result = run_experiment(
    "nutrition-experiment",
    dataset_name="synthetic_runzi_nutrition_dataset",
    prompt_template=prompt,
    prompt_settings=prompt_run_settings,
    metrics=[GalileoMetrics.correctness],
    project="EvalsCourse"
)

print(f"Experiment URL: {experiment_result['link']}")
