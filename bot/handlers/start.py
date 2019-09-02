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
@decorators.restricted
@decorators.failwithmessage
def on_help_command(update: Update, _):
    logger.info('%d: /help', update.effective_user.id)

    update.message.reply_html(Strings.HELP_MESSAGE, disable_web_page_preview=True)


@decorators.action(ChatAction.TYPING)
@decorators.restricted
@decorators.failwithmessage
def on_start_command(update: Update, _):
    logger.info('%d: /start', update.effective_user.id)

    update.message.reply_markdown(Strings.START_MESSAGE, disable_web_page_preview=True)


torrentsbot.add_handler(CommandHandler('help', on_help_command))
torrentsbot.add_handler(CommandHandler('start', on_start_command))
