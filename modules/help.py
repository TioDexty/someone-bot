import logging

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext.dispatcher import run_async

from utils import db


SHORT = """Telegram bot inspired to [Discord's @someone April fool](https://twitter.com/discordapp/status/980159255662637056)

Add me to a group and use @someone to mention a random user who has been active during the past three weeks

[source code](https://github.com/zeroone2numeral2/someone-bot)\
"""

LONG = """*@someone flavours*
`^@someone`: mention by first name, even if the user has an username
`@@someone`: mention an user without using his name/username, but mention him with "@someone" instead
`?@someone`: the mention will be contained in a zero-width character, resulting not visible and not clickable

*Command auto-deletion*
Add a leading question mark to make the bot delete your message. Obviously, \
the bot needs the permission to delete messages for this to work (examples: \
`!@someone`, `!@@someone`, `!^@someone` or `!?@someone`)

*Additional text*
If you write something after `@someone`, the bot will include it in its reply:
```
you >> @someone please ban this annoying bot!!
bot >> @durov please ban this annoying bot!!```

*Aliases*
You can set an alias in private with "`/alias your alias`".
Aliases will replace your name/username when @someone is used. \
Aliases are not used if a falvour is added (`^@someone`, `@@someone`...).
Use `/alias get` to get your currently set alias

*How does it work?*
Bots can't obtain the list of the users in a group - this implies that this bot remembers all the people \
who joined/talked in the chat, making it possible for him to mention them on request.

What is stored (per group):
- the chat id
- id, first name, username (if any) and date of the last sent message of every user who spoke/joined

These informations are updated on every message received, to assure correct outputs. If you don't feel ok \
with this amount of data being stored, you can always host the bot yourself


Names and aliases are saved with at most 160 charaters\
"""

logger = logging.getLogger(__name__)

extended_help_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton('extended help', callback_data='extend')]
])

short_help_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton('reduce', callback_data='reduce')]
])


@run_async
def help_message(bot, update):
    logger.info('/help or /start command')
    db.save_user(update.message.from_user)
    update.message.reply_markdown(SHORT, reply_markup=extended_help_markup,
                                  disable_web_page_preview=True)


@run_async
def on_extended_help_button(bot, update):
    logger.info('extend help')
    update.callback_query.message.edit_text(LONG, reply_markup=short_help_markup,
                                            parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def on_short_help_button(bot, update):
    logger.info('reduce help')
    update.callback_query.message.edit_text(SHORT, reply_markup=extended_help_markup,
                                            parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


class module:
    name = 'help'
    handlers = (
        CommandHandler(['start', 'help'], help_message, filters=Filters.private),
        CallbackQueryHandler(on_extended_help_button, pattern='^extend$'),
        CallbackQueryHandler(on_short_help_button, pattern='^reduce$'),
    )
