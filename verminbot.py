# pylint: disable=missing-docstring
# pylint: disable=no-else-return
# pylint: disable=too-few-public-methods
import random
import requests


def about_command():
    return "I am the Verminlord."


def help_command(self):
    return "Commands: !!{}; !!{}; !!{} <text>; !!{} <text>; !!{};".format(
        self.ABOUT_COMMAND,
        self.CAT_COMMAND,
        self.LEET_COMMAND,
        self.TRANS_COMMAND,
        self.HELP_COMMAND,
    )


def funtranslate_command(to_translate):
    req_response = requests.get(
        "https://api.funtranslations.com/"
        + 'translate/mandalorian.json?text="'
        + to_translate
        + '"'
    ).json()
    try:
        if len(req_response["contents"]["translated"]) < 195:
            return req_response["contents"]["translated"]
        else:
            return "Translation exceeded message capacity :("
    except KeyError:
        return "Too many translations, try again later"


def leet_command(message_content):
    leet_translation = message_content.lower()
    translations = {"o": "0", "t": "7", "l": "1", "e": "3", "a": "4", "s": "5"}
    for key in translations:
        leet_translation = leet_translation.replace(key, translations[key])
    return str(leet_translation)


def catfact_command():
    req_response = requests.get("https://cat-fact.herokuapp.com" + "/facts").json()[
        "all"
    ]
    catfact = random.choice(req_response)["text"]
    while len(catfact) > 115:
        catfact = random.choice(req_response)["text"]
    return catfact


def unrecognize_command():
    return "That command was unrecognized. For a list of commands, type !!help"


class Verminbot:

    BOT_PREFIX = "~/ "
    ABOUT_COMMAND = "about"
    HELP_COMMAND = "help"
    TRANS_COMMAND = "funtranslate"
    LEET_COMMAND = "1337"
    CAT_COMMAND = "catfact"

    def __init__(self):
        self.bot = "ratbot"

    def handle_command(self, message_content):
        # strip spaces and figure out what command is being called
        clean_input = str(message_content).strip()
        if clean_input[0 : len(self.ABOUT_COMMAND)] == self.ABOUT_COMMAND:
            return self.BOT_PREFIX + about_command()

        elif clean_input[0 : len(self.HELP_COMMAND)] == self.HELP_COMMAND:
            return self.BOT_PREFIX + help_command(self)

        elif clean_input[0 : len(self.TRANS_COMMAND)] == self.TRANS_COMMAND:
            return self.BOT_PREFIX + funtranslate_command(
                clean_input[len(self.TRANS_COMMAND) :].strip()
            )

        elif clean_input[0 : len(self.LEET_COMMAND)] == self.LEET_COMMAND:
            return self.BOT_PREFIX + leet_command(
                clean_input[len(self.LEET_COMMAND) :].strip()
            )

        elif clean_input[0 : len(self.CAT_COMMAND)] == self.CAT_COMMAND:
            return self.BOT_PREFIX + catfact_command()

        else:
            return self.BOT_PREFIX + unrecognize_command()
