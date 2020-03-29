import logging

# noinspection PyPackageRequirements
from telegram.ext import MessageHandler, Filters
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
def on_unknown_command(update: Update, _):
    logger.info('%d: unknown command', update.effective_user.id)

    update.message.reply_html(Strings.UNKNOWN_COMMAND)


# this handler MUST be added to the bot after all other handlers has been added. Since
# plugins are loaded alphabetically, we are lucky this one is the last one right now
torrentsbot.add_handler(MessageHandler(Filters.command, on_unknown_command))
