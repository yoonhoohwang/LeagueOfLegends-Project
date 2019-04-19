import telegram

class TelegramAPI(object):
    API_KEY = None

    bot = None

    def __init__(self):
        self.API_KEY = '661670678:AAFluBW-ZTSmxsUSv85WkzrcvH57AQF5nsA'
        self.bot = telegram.Bot(token = self.API_KEY)
    
    def sendMsg(self, text_barn):
        self.bot.sendMessage(chat_id = "704445567", text = text_barn)
