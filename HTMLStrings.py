# take a list of messages and convert to <img>, <a>, or just leave as text
from rfc3987 import parse

class HTMLStrings:
    
    def __init__(self):
        self.HTMLWriter = "HTMLWriter"
    
    def isHTML(self, message):
        try:
            parse(message, rule='URI')
            return True
        except ValueError:
            return False
            
    def formatHTML(self, messages):
        imageExtensions = ['.jpg', '.png', '.gif']
  
        i = 0
        for message in messages:
            if (message[-4:].lower() in imageExtensions):
                messages[i] = "<img src={} className='pictures' height=45px;/>".format(messages[i])
            elif (self.isHTML(message)):
                messages[i] = "<a href={}>{}</a>".format(messages[i], messages[i])
            else:
                temp="https://"+message
                if (self.isHTML(temp)):
                    messages[i] = "<a href={}>{}</a>".format(temp, messages[i])
            i+=1
            
    