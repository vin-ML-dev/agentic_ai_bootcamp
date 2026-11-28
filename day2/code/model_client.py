"""
Day 2 - Course API client
Sends our messages to the AI model and returns its reply.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # read settings from the .env file

# Settings
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE"))  # 0 = same answer every time
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))      # longest answer allowed

# Connect to the model provider using our secret API key
client = OpenAI(
    api_key=os.getenv("MODEL_API_KEY"),
    base_url=os.getenv("MODEL_BASE_URL"),
)


# Ask the model a normal question -> it replies with text
def ask_model(messages):
    return client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )


# Ask the model with tools -> it can reply with a tool call request
def ask_model_with_tools(messages, tools):
    return client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        tools=tools,
        tool_choice="required",  # always reply with a tool call
    )
