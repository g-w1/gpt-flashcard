import os
import openai
import json
import sys
from prompt_genfact2 import *
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

USE_GPT_4 = False
MODEL = "gpt-4" if USE_GPT_4 else "gpt-3.5-turbo-16k"


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


def get_facts_from_paragraph(paragraph):
    CURR_PROMPT = paragraph
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER1},
        {"role": "assistant", "content": ASS1},
        {"role": "user", "content": USER2},
        {"role": "assistant", "content": ASS2},
        {"role": "user", "content": USER3},
        {"role": "assistant", "content": ASS3},
        # {"role": "user", "content": USERFACT1_WRONG},
        # {"role": "assistant", "content": ASSFACT1_WRONG},
        # {"role": "user", "content": USERFACT2_WRONG + CURR_PROMPT},
        {"role": "user", "content": CURR_PROMPT},
    ]

    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=1.3,
        max_tokens=word_count * 9,
    )

    message = completion.choices[0].message
    time.sleep(3)
    return message["content"]


def get_cards_from_facts(facts, noinfo):
    debug("get_cards_from_facts: noinfo:", noinfo)
    if noinfo:
        card = SYSTEM_CARD_NOINFO
    else:
        card = SYSTEM_CARD
    messages = [
        {"role": "system", "content": card},
        {"role": "user", "content": facts},
    ]
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=1.3,
        max_tokens=word_count * 9,
    )
    message = completion.choices[0].message
    time.sleep(3)
    return extract_json_objects(message["content"])


def debug(*args, **kwargs):
    print("DEBUG ", *args, file=sys.stderr, **kwargs)


# Sees if it is 'true'
def b(boo):
    return boo == "true" or boo == "True"


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        debug("need either True or False for noinfo")
    else:
        noinfo = b(argv[1])
        debug("noinfo:", noinfo)
        INPUT_paragraphs = sys.stdin.readlines()
        cards = []
        PROCESSED_paragraphs = [
            para.strip() for para in INPUT_paragraphs if para.strip()
        ]

        for i, paragraph in enumerate(PROCESSED_paragraphs):
            word_count = len(paragraph.split())
            if word_count < 20:
                debug("skipping paragraph because its too short:", paragraph)
                continue
            facts = get_facts_from_paragraph(paragraph)
            debug("facts:", facts)
            cs = get_cards_from_facts(facts, noinfo)
            debug("cards:", cs)
            cards.extend(cs)

        print(json.dumps(cards))
