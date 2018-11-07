import os

from telegram.ext import Updater

updater = Updater(token=os.environ.get('TG_TOKEN') or '285333393:AAGNcUHU1Ct14LgyrmaN9dmha-frZjCgUV8')
dispatcher = updater.dispatcher
