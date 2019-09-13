import logging

# noinspection PyPackageRequirements
from telegram.ext import CommandHandler
# noinspection PyPackageRequirements
from telegram import (
    ChatAction,
    Update
)

from bot import torrentsbot
from bot.utils import decorators
from bot.strings import Strings

logger = logging.getLogger(__name__)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_disclaimer_command(update: Update, _):
    logger.info('%d: /disclaimer', update.effective_user.id)

    update.message.reply_html(Strings.DISCLAIMER, disable_web_page_preview=True)


torrentsbot.add_handler(CommandHandler('disclaimer', on_disclaimer_command))
