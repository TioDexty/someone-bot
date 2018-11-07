import logging
import random
import re
from html import escape as html_escape

from telegram.error import BadRequest
from telegram.error import TelegramError
from telegram.ext import RegexHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

from database import Member

logger = logging.getLogger(__name__)

SOMEONE_REGEX = re.compile(r'^([!@^?]{0,2})@someone(?:\s+(.+))?', re.I)


@run_async
def on_someone(bot, update, groups):
    msg = update.effective_message
    if msg.chat_id < 0:  # groups only
        logger.info('@someone from %d in %d', msg.from_user.id, msg.chat_id)

        active_users = Member.get_active(msg.chat_id)
        if not active_users:
            logger.info('no users for this chat: %d', msg.chat_id)
            Member.upsert(msg.chat_id, msg.from_user)
            return

        rand_user = random.choice(active_users)

        if '@' in groups[0]:
            # mention with "@someone"
            user_mention = mention_html(rand_user.user.user_id, '@someone')
        elif '^' in groups[0]:
            # mention by first name
            user_mention = mention_html(rand_user.user.user_id, rand_user.user.first_name)
        elif '?' in groups[0]:
            # non-clickable mention using zero-width char
            user_mention = '<code>@someone</code>{}'.format(mention_html(rand_user.user.user_id, u'\u200B'))
        else:
            if rand_user.user.alias:  # alias
                # mention by alias if set
                user_mention = mention_html(rand_user.user.user_id, rand_user.user.alias)
            else:
                # mention by username if present, otherwise user the first name
                user_mention = '@' + rand_user.user.username if rand_user.user.username else mention_html(rand_user.user.user_id, rand_user.user.first_name)

        text = f'{user_mention} {html_escape(groups[1]) if groups[1] else ""}'

        msg.reply_html(text, disable_web_page_preview=True,
                       reply_to_message_id=msg.reply_to_message.message_id if msg.reply_to_message else None)

        # try to delete if the message starts with '!'
        if msg.text.startswith('!'):
            try:
                msg.delete()
            except (BadRequest, TelegramError) as e:
                logger.info("can't delete message: %s", str(e))


HANDLERS = (
    RegexHandler(SOMEONE_REGEX, on_someone, pass_groups=True, channel_post_updates=False),
)
