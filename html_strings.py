# pylint: disable=missing-docstring

# take a list of messages and convert to <img>, <a>, or just leave as text
from rfc3987 import parse


class HTMLStrings:

    imageExtensions = [".jpg", ".png", ".gif"]
    urlExtensions = [".com", ".org", ".gov", ".edu", ".net", ".gg", ".io"]

    def __init__(self):
        self.html_writer = "HTMLWriter"

    def is_html(self, message):
        for suffix in self.urlExtensions:
            if suffix in message:
                try:
                    parse(message, rule="URI")
                    return True
                except ValueError:
                    pass
        return False

    def format_html(self, messages):

        i = 0
        for message in messages:
            if message[-4:].lower() in self.imageExtensions:
                messages[
                    i
                ] = "<img src={} className='chat-pictures' height= 90%; />".format(
                    messages[i]
                )
            elif self.is_html(message):
                messages[i] = "<a href={}>{}</a>".format(messages[i], messages[i])
            else:
                temp = "https://" + message
                if self.is_html(temp):
                    messages[i] = "<a href={}>{}</a>".format(temp, messages[i])
            i += 1
