import os
import openai
import json
from prompt import *

INPUT = input()

messages = [
    {"role": "system", "content": SYSTEM},
    {"role": "user", "content": USER1},
    {"role": "assistant", "content": ASS1},
    {"role": "user", "content": USER2},
    {"role": "assistant", "content": ASS2},
    {"role": "user", "content": USER3},
    {"role": "assistant", "content": ASS3},
    {"role": "user", "content": INPUT},
]
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k", messages=messages, temperature=1.3, max_tokens=1024
)

message = completion.choices[0].message


def extract_json_objects(string):
    json_objects = []

    lines = string.strip().split("\n")  # Split the string into lines

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        try:
            json_object = json.loads(line)  # Attempt to parse the line as JSON
            json_objects.append(json_object)  # Add the JSON object to the array
        except json.JSONDecodeError:
            pass  # Ignore lines that are not valid JSON

    return json_objects


cards = extract_json_objects(message["content"])
print(json.dumps(cards))
