import logging

# noinspection PyPackageRequirements
from telegram.ext import ConversationHandler
# noinspection PyPackageRequirements
from telegram import Update, ChatAction

from bot.markups import Keyboard
from bot.strings import Strings
from ..utils import decorators

logger = logging.getLogger(__name__)


@decorators.action(ChatAction.TYPING)
@decorators.restricted
@decorators.failwithmessage
def cancel_command(update: Update, _):
    logger.info('%s command', update.message.text)

    update.message.reply_text(Strings.CANCEL, reply_markup=Keyboard.HIDE)
    
    return ConversationHandler.END
