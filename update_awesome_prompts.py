import csv
import requests
from io import StringIO
from pathlib import Path
from json import load
from json import dump

timeout = 10


def get_raw(url: str):
    return requests.get(url, timeout=timeout)


def gpt_jailbreak_status(resp: dict = {}) -> dict:
    url = "https://github.com/tg12/gpt_jailbreak_status/blob/main/gpt_jb.csv?raw=true"
    raw = StringIO(get_raw(url).text)
    for row in csv.DictReader(raw):
        resp[row["name"]] = row["text"]
    return resp


def awesome_chatgpt_prompts(resp: dict = {}) -> dict:
    url = "https://github.com/f/awesome-chatgpt-prompts/blob/main/prompts.csv?raw=true"
    raw = StringIO(get_raw(url).text)
    for row in csv.DictReader(raw):
        resp[row["act"]] = row["prompt"]
    return resp


def save(resp: dict) -> None:
    path = Path("assets/all-acts.json")
    with path.open() as fh:
        prompts = load(fh)
    prompts.update(resp)
    with path.open("w") as fh:
        dump(prompts, fh, indent=4)


if __name__ == "__main__":
    prompts = awesome_chatgpt_prompts(gpt_jailbreak_status())
    save(prompts)
    print("Done")
