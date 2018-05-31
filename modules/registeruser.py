import logging

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext.dispatcher import run_async

from bot import updater
from utils import db

logger = logging.getLogger(__name__)


@run_async
def on_new_member(bot, update):
    logger.info('new members in %d: %d new members', update.message.chat.id, len(update.message.new_chat_members))
    db.save_users(update.message.chat_id, update.message.new_chat_members)


@run_async
def on_left_member(bot, update):
    logger.info('left member in %d', update.message.chat.id)
    db.remove_user(update.message.chat_id, update.message.left_chat_member)


@run_async
def on_new_message(bot, update):
    logger.info('new message in %d from %d', update.message.chat_id, update.message.from_user.id)
    db.save_users(update.message.chat_id, update.message.from_user)
    if update.message.reply_to_message:
        db.save_users(update.message.chat_id, update.message.reply_to_message.from_user)


class module:
    name = 'registeruser'
    handlers = (
        MessageHandler(Filters.status_update.new_chat_members & ~Filters.user(user_id=updater.bot.id), on_new_member),
        MessageHandler(Filters.status_update.left_chat_member & ~Filters.user(user_id=updater.bot.id), on_left_member),
        MessageHandler(Filters.group, on_new_message),
    )
