import requests
import random

class Verminbot:
    
    BOT_PREFIX = '~/ '
    ABOUT_COMMAND='about'
    HELP_COMMAND='help'
    FUNTRANS_COMMAND='funtranslate'
    LEET_COMMAND='1337'
    CAT_COMMAND='catfact'
    
    
    def __init__(self):
        self.bot = "ratbot"
    
    
    def handle_command(self, messageContent):
        # strip spaces and figure out what command is being called
        cleanInput=str(messageContent).strip()
        if (cleanInput[0:len(self.ABOUT_COMMAND)]==self.ABOUT_COMMAND):
            return self.BOT_PREFIX + self.aboutCommand()
            
        elif (cleanInput[0:len(self.HELP_COMMAND)]==self.HELP_COMMAND):
            return self.BOT_PREFIX + self.helpCommand()

        elif (cleanInput[0:len(self.FUNTRANS_COMMAND)]==self.FUNTRANS_COMMAND):
            return self.BOT_PREFIX + self.funtranslateCommand(cleanInput[len(self.FUNTRANS_COMMAND):].strip())
            
        elif (cleanInput[0:len(self.LEET_COMMAND)]==self.LEET_COMMAND):
            return self.BOT_PREFIX + self.leetCommand(cleanInput[len(self.LEET_COMMAND):].strip())
            
        elif (cleanInput[0:len(self.CAT_COMMAND)]==self.CAT_COMMAND):
            return self.BOT_PREFIX + self.catfactCommand()
            
        else:
            return "That command was unrecognized. For a list of commands, type !!help"
        
        
    def aboutCommand(self):
        return "I am the Verminlord."
    
    
    def helpCommand(self):
        return "Commands: !!about; !!catfact; !!1337 <text>; !!funtranslate <text>; !!help;"
    
    
    def funtranslateCommand(self, toTranslate):
        reqResponse = requests.get('https://api.funtranslations.com/translate/mandalorian.json?text="' + toTranslate + '"').json()
        try:
            return reqResponse['contents']['translated']
        except KeyError:
            return "Too many translations, try again later"
        except:
            return reqResponse['error']['message']
    
    def leetCommand(self, messageContent):
        leetTranslation = messageContent.lower()
        
        translations = {
            'o':'0',
            't':'7',
            'l':'1',
            'e':'3',
            'a':'4',
            's':'5'    }
            
        for key in translations:
            leetTranslation = leetTranslation.replace(key, translations[key])
        return str(leetTranslation)
        
    def catfactCommand(self):
        reqResponse = requests.get('https://cat-fact.herokuapp.com/facts').json()['all']
        catFact = random.choice(reqResponse)['text']
        while len(catFact) > 115:
            catFact = random.choice(reqResponse)['text']
        return catFact
