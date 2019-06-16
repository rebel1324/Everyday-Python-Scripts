# When I start coding or doing something, I usually forget to rest.
# I just want to continue working on my stuffs.

# Requires:
#   win10toast
#   python-telegram-bot

import os
import time
import datetime
import logging
from win10toast import ToastNotifier
from telegram.ext import Updater
from telegram.bot import Bot

class Telegram:
    api_key = ""
    updater = None
    bot = None

    def registerKey(self, path):
        api_key_dir = os.path.dirname(os.path.abspath(__file__))
        api_key_dir = os.path.join(api_key_dir, path)
        
        try:
            f = open(api_key_dir, 'r')
            self.api_key = f.readline()
            self.updater = Updater(token=self.api_key)
            self.bot = Bot(token=self.api_key)
        except FileNotFoundError:
            print("Telegram API key does not exists.")
            quit()

    def isValid(self):
        return (len(self.api_key) > 0)

    def checkValid(self):
        print("Telegram Object is " + ("Valid!" if self.isValid() else "Invalid..?"))

    def sendMessage(self, message):
        self.bot.send_message(chat_id='538074142', text=message) #yeah it's my id buzz off

if __name__ == "__main__":
    toaster = ToastNotifier()
    tele = Telegram()
    tele.registerKey('telegram_key') #open telegram_key on script's path
    tele.checkValid()

    try:
        while True:
            toaster.show_toast("일 시작!", "일을 시작할 시간이 되었습니다.", duration=10)
            time.sleep(60*90) # 1.5 hours
            
            toaster.show_toast("휴식 시간", "휴식을 취할 시간이 되었습니다.", duration=10)
            time.sleep(60*30) # 0.5 hours
            tele.sendMessage("휴식 시간이 끝났습니다! 일을 해주세요")
    except KeyboardInterrupt:
        print("일을 완전히 끝냅니다.")
