#-*- coding: utf-8 -*-
# When I start coding or doing something, I usually forget to rest.
# I just want to continue working on my stuffs.
# man win10 toast is god damn worthless

# Requires:
#   python-telegram-bot

import os
import time
import datetime
from datetime import datetime, timedelta

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

restFirst = True
if __name__ == "__main__":
    tele = Telegram()
    tele.registerKey('telegram_key') #open telegram_key on script's path
    tele.checkValid()

    try:
        while True:
            if (not restFirst):
                myTime = datetime.today() + timedelta(seconds = 60*90)
                tele.sendMessage("일을 시작합니다. 다음 휴식 시간은 " + myTime.strftime("%H:%M:%S") + " 입니다.")
                time.sleep(60*90) # 1.5 hours
            
            myTime = datetime.today() + timedelta(seconds = 60*30)
            tele.sendMessage("휴식을 시작합니다. 다음 일 시간은 " + myTime.strftime("%H:%M:%S") + " 입니다.")
            time.sleep(60*30) # 0.5 hours
            restFirst = False
    except KeyboardInterrupt:
        print("일을 완전히 끝냅니다.")
