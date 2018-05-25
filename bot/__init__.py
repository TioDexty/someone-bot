import os

from telegram.ext import Updater

updater = Updater(token=os.environ.get('TG_TOKEN') or '')
dispatcher = updater.dispatcher
