from galileo.datasets import create_dataset, extend_dataset

from dotenv import load_dotenv

load_dotenv()


# Generate synthetic data
synthetic_dataset = extend_dataset(
    prompt_settings={"model_alias": "gpt-5-mini"},
    prompt="Running chatbot",
    instructions="""
I am building a demo multi-agent AI application for runners. It can answer questions about nutrition for runners.

I need typical questions that runners might have about nutrition both in general, and during races.
    """,
    examples=[
        "How many grams of carbohydrates and protein should I aim for on a typical training day when I run 30 miles per week?",
        "Can you give me ideas for a good pre-run breakfast for a 90-minute long run?",
    ],
    data_types=["General Query"],
    count=10,
)

# Prepare the dataset content
dataset_content = [{"input": row.values[0]} for row in synthetic_dataset]

# Upload the dataset
dataset = create_dataset(
    name="synthetic_runzi_nutrition_dataset",
    project_name="EvalsCourse",
    content=dataset_content,
)
