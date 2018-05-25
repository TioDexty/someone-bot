import logging
import random
import re
from html import escape as html_escape

from telegram.error import BadRequest
from telegram.ext import RegexHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

from utils import db

logger = logging.getLogger(__name__)

SOMEONE_REGEX = re.compile(r'^([!@^?]{0,2})@someone(?:\s+(.+))?', re.I)


@run_async
def on_someone(bot, update, groups):
    msg = update.effective_message
    if msg.chat_id < 0:  # groups only
        logger.info('@someone from %d in %d', msg.from_user.id, msg.chat_id)

        active_users = db.get_active_users(msg.chat_id)
        if not active_users:
            logger.info('no users for this chat: %d', msg.chat_id)
            db.save_users(msg.chat_id, msg.from_user)
            return

        rand_user = random.choice(active_users)

        if '@' in groups[0]:
            user_mention = mention_html(rand_user[0], '@someone')
        elif '^' in groups[0]:
            user_mention = mention_html(*rand_user[:2])
        elif '?' in groups[0]:
            user_mention = '<code>@someone</code>{}'.format(mention_html(rand_user[0], u'\u200B'))
        else:
            if rand_user[3]:  # alias
                user_mention = mention_html(rand_user[0], rand_user[3])
            else:
                user_mention = '@' + rand_user[2] if rand_user[2] else mention_html(rand_user[:1])

        text = f'{user_mention} {html_escape(groups[1]) if groups[1] else ""}'

        msg.reply_html(text, disable_web_page_preview=True,
                       reply_to_message_id=msg.reply_to_message.message_id if msg.reply_to_message else None)

        # try to delete if the message starts with '!'
        if msg.text.startswith('!'):
            try:
                msg.delete()
            except BadRequest as e:
                logger.info("can't delete message: %s", str(e))


class module:
    name = 'someone'
    handlers = (
        RegexHandler(SOMEONE_REGEX, on_someone, pass_groups=True, channel_post_updates=False),
    )
