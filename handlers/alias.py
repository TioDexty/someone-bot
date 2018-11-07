import logging

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext.dispatcher import run_async

from database import User

logger = logging.getLogger(__name__)


@run_async
def on_alias_command(bot, update, args):
    logger.info('/alias')

    alias = ' '.join(args)

    user_id = update.effective_user.id
    if alias == '':
        user = User.get(User.user_id == user_id)
        update.message.reply_markdown(user.alias or "You don't have an alias set right now, use `/alias something` "
                                                    "to set one")
    elif alias == '-':
        User.update(alias=None).where(User.user_id == user_id).execute()
        update.message.reply_text('Alias unset!')
    else:
        updated_rows = User.update(alias=alias[:161]).where(User.user_id == user_id).execute()
        logger.info('updated rows: %d', updated_rows)
        update.message.reply_text('Alias set!')


HANDLERS = (
    CommandHandler('alias', on_alias_command, filters=Filters.private, pass_args=True),
)
