# take a list of messages and convert to <img>, <a>, or just leave as text
from rfc3987 import parse

class HTMLStrings:
    
    imageExtensions = ['.jpg', '.png', '.gif']
    urlExtensions = ['.com','.org','.gov','.edu','.net','.gg','.io']
  
    def __init__(self):
        self.HTMLWriter = "HTMLWriter"
    
    def isHTML(self, message):
        for suffix in self.urlExtensions:
            if suffix in message:
                try:
                    parse(message, rule='URI')
                    return True
                except ValueError:
                    pass
        return False
    def formatHTML(self, messages):

        i = 0
        for message in messages:
            if (message[-4:].lower() in self.imageExtensions):
                messages[i] = "<img src={} className='pictures' height=45px;/>".format(messages[i])
            elif (self.isHTML(message)):
                messages[i] = "<a href={}>{}</a>".format(messages[i], messages[i])
            else:
                temp="https://"+message
                if (self.isHTML(temp)):
                    messages[i] = "<a href={}>{}</a>".format(temp, messages[i])
            i+=1
            
    