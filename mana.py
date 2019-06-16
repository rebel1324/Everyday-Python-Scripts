
#-*- coding: utf-8 -*-
# Requires:
#   python-telegram-bot

import os
import time
import datetime
import re
import json
import urllib.parse
from requests import get
from datetime import datetime, timedelta

from telegram.ext import Updater
from telegram.bot import Bot

def curdir(newDir):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), newDir)

class Telegram:
    api_key = ""
    updater = None
    bot = None

    def registerKey(self, path):
        api_key_dir = curdir(path)

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

class Mana():
    name = ""
    url = ""
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def check():
        pass

    def getLastest():
        pass
        
urlRegex = re.compile("<a\s+[A-z=\"_\s]*href=\"([\d\w:/.가-힝,\s]+)\">([\d\w:/.가-힝,\s]+)<\/a>?")
dontSend = False
if __name__ == "__main__":
    mana_olddatabase = {}
    mana_newdatabase = {}

    mana_list = {
    }

    tele = Telegram()
    tele.registerKey('telegram_key') #open telegram_key on script's path
    tele.checkValid()
    
    jsonFile = curdir('manga_aware.json')
    with open(jsonFile) as input:  
        mana_olddatabase = json.load(input)

    count = 0
    telegramPayload = "새로운 만화를 찾았습니다.\n"

    print("Checking latest mana")
    for key, mana in mana_list.items():
        request = get(mana.url)
        text = request.text
        startIndex = text.find("<div class=\"col-sm-12\">")
        endIndex = text.find("<div class=\"latest-news-wrapper\">")
        results = re.findall(urlRegex, text[startIndex:endIndex])
        resultCount = len(results)
        print(f"Found {resultCount} of {mana.name}")
        mana_newdatabase[key] = {}
        for value in results:
            name = value[1]
            url = value[0]
            mana_newdatabase[key][url] = name

            if ((not key in mana_olddatabase) or (not url in mana_olddatabase[key])):
                telegramPayload += f"새로운 '{name}' 만화: {urllib.parse.quote(url, safe=':/')}\n"
                count += 1

    telegramPayload += f"\n... 이상 {count}개의 새로운 만화였습니다."
    print(f"Found {count} of new mangas.")
    
    if (count > 0 and not dontSend):
        tele.sendMessage(telegramPayload) #yeah it's my id buzz off

    with open(jsonFile, 'w') as output:  
        json.dump(mana_newdatabase, output)
            
            
