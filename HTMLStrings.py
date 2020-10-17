# take a list of messages and convert to <img>, <a>, or just leave as text
class HTMLStrings:
    
    def __init__(self):
        self.HTMLWriter = "HTMLWriter"
        
    def formatHTML(self, messages):
        imageExtensions = ['.jpg', '.png', '.gif']
        urlExtensions = ['.com', '.org', '.net', '.gov', '.edu']
        i = 0
        for message in messages:
            if (message[-4:].lower() in imageExtensions):
                messages[i] = "<img src={} className='pictures' height=45px;/>".format(messages[i])
            elif (message[-4:].lower() in urlExtensions):
                messages[i] = "<a href={}>{}</a>".format(messages[i], messages[i])
            else:
                pass
            i+=1