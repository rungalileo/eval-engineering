from galileo.openai import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Galileo OpenAI client wrapper
client = openai.OpenAI()

# Define a system prompt with guidance
system_prompt = """
You are a helpful HR assistant. Provide very clear, very short,
and very succinct answers to the user's questions based off their
employment contract and other criteria.

Just provide the details asked, avoiding any extra information
or explanations.
"""

# Define a user prompt with a question
user_prompt = """
I am in the UK. How many vacation days do I have this year?
"""

# Send a request to the LLM
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
)

# Print the response
print(response.choices[0].message.content.strip())
