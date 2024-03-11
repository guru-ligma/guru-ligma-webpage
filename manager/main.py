import json
import cliTextTools as ctt
import math
import clipboard
from typing import Union


file = "additions.json"
with open(file) as f:
    data = json.load(f)

basic_additions = """Check out me out on my other social media's! https://linkin.bio/guru-ligma
For More information, like how to support me, or how to use my art see my website:
https://guru-ligma.github.io/guruligma.github.io"""


def convert(text: str, additions: str) -> str:
    text_len = len(text)
    sep = math.floor(math.floor(text_len / 2) * 15 / 10) + 1
    text = f"{text}\n{'='*sep}\n{additions}"
    return text


def get_name() -> Union[str, None]:
    msg = "Enter the name of the piece:"
    result = ctt.get_user_input(msg, ctt.STR_TYPE, allow_newlines=False, can_cancel=True)
    if result is not None:
        result = result.title()
    return result


def new_post() -> None:
    name = get_name()
    if name is None:
        print("No name entered, ending post!")
        return
    print(f"The name of the post is {name}")
    for key in data.keys():
        print(f"\n\n\n\nThe profile this text is set for is {key.upper()}")
        tagins = data[key]["tagins"]
        hashtags = data[key]["hashtags"]
        additions = f"{basic_additions}\n{tagins}{hashtags}"
        text = convert(name, additions)
        print(f"\n\nThe Result: \n{text}\n")
        print(f"It is {len(text)} chars long\n")
        clipboard.copy(text)
        msg = "do you wish to continue?"
        if not ctt.get_user_input(msg, ctt.BOOL_TYPE, help_msg=ctt.BOOL_HELP, can_cancel=False):
            break


def main():
    while True:
        new_post()
        msg = "Do you wish to make a new post?"
        if not ctt.get_user_input(msg, ctt.BOOL_TYPE, help_msg=ctt.BOOL_HELP, can_cancel=False):
            break



if __name__ == "__main__":
    main()