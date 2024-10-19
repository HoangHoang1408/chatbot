import os

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from together import Together

load_dotenv()

TOGETHER_AI_KEY = os.environ.get("TOGETHER_AI_KEY")
client = Together(api_key=TOGETHER_AI_KEY)
DEFAULT_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_completion(messages, model=DEFAULT_MODEL):
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

