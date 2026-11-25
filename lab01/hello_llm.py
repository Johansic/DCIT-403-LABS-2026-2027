
import os
from dotenv import load_dotenv
from litellm import completion

# Load settings and API key from the .env environment
load_dotenv()

MODEL = os.getenv("LLM_MODEL")

# Send a message to the language model
resp = completion(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "In one sentence, what is an intelligent agent?"
        },
    ],
)

# Display the model's response and token usage
print(resp.choices[0].message.content)
print(resp.usage)
