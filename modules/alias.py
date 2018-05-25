import logging

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext.dispatcher import run_async

from utils import db

logger = logging.getLogger(__name__)


@run_async
def on_alias_command(bot, update, args):
    logger.info('/alias')

    alias = ' '.join(args)

    user_id = update.effective_message.from_user.id
    if alias == '':
        update.message.reply_markdown('You have to tell me the alias\nUse: `/alias your alias`')
    elif alias == '-':
        db.set_alias(user_id)
        update.message.reply_text('Alias unset!')
    elif alias == 'get':
        alias = db.get_alias(user_id) or "You don't have an alias set right now"
        update.message.reply_text(alias)
    else:
        db.set_alias(user_id, alias[:161])
        update.message.reply_text('Alias set!')


class module:
    name = 'alias'
    handlers = (
        CommandHandler('alias', on_alias_command, filters=Filters.private, pass_args=True),
    )
