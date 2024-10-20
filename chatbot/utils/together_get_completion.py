import os
from datetime import datetime

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    os.environ.get("HUGGINGFACE_DEFAULT_MODEL"),
    token=os.environ.get("HUGGINGFACE_TOKEN"),
)


# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_completion(
    messages,
    tools=None,
    model=os.environ.get("TOGETHER_AI_DEFAULT_MODEL"),
    tokenizer=tokenizer,
    stream=False,
    temperature=float(os.environ.get("GENERATION_CONFIG_TEMPERATURE")),
    max_tokens=int(os.environ.get("GENERATION_CONFIG_MAX_TOKENS")),
):

    client = OpenAI(
        api_key=os.environ.get("TOGETHER_AI_KEY"),
        base_url="https://api.together.xyz/v1",
    )
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        tools=tools,
        tools_in_user_message=False,
        date_string=datetime.now().strftime("%d-%m-%Y"),
        add_generation_prompt=True,
    )
    return (
        client.completions.create(
            model=model,
            prompt=prompt,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        .choices[0]
        .text
    )
