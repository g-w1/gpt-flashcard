import os
import openai
import json
import sys
from prompt1 import *
import time

INPUT_paragraphs = sys.stdin.readlines()
cards = []


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


def get_cards_from_paragraph(paragraph, context):
    CURR_PROMPT = f"""
    {f"Here is the previous paragraph: {context}" if context != None else ""}
    Please now make cards on this paragraph:
    ===
    {paragraph}
    ===
    Remember to make the cards context free. They should be able to be completed even if the user has not read the text. They should not reference 'it' or 'that' or anything ambigious. Use names and specifics. The use should be able to do them in any order. BE SPECIFIC!!!
    """
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER1},
        {"role": "assistant", "content": ASS1},
        {"role": "user", "content": USER2},
        {"role": "assistant", "content": ASS2},
        {"role": "user", "content": USER3},
        {"role": "assistant", "content": ASS3},
        {"role": "user", "content": CURR_PROMPT},
    ]
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=1.3,
        max_tokens=word_count * 9,
    )

    message = completion.choices[0].message
    time.sleep(3)
    return extract_json_objects(message["content"])


def debug(*args, **kwargs):
    print("DEBUG ", *args, file=sys.stderr, **kwargs)


PROCESSED_paragraphs = [para.strip() for para in INPUT_paragraphs if para.strip()]

for i, paragraph in enumerate(PROCESSED_paragraphs):
    if i == 0:
        context = PROCESSED_paragraphs[i - 1]
        debug("skipping context because its the first card")
    else:
        context = None
    word_count = len(paragraph.split())
    if word_count < 20:
        debug("skipping paragraph because its too short:", paragraph)
        continue
    cs = get_cards_from_paragraph(paragraph, context)
    debug(json.dumps(cs))
    cards.extend(cs)

print(json.dumps(cards))
