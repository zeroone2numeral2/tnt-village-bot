import logging

# noinspection PyPackageRequirements
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
# noinspection PyPackageRequirements
from telegram import (
    ChatAction,
    Update
)

from bot import torrentsbot
from bot import db
from bot.markups import InlineKeyboard
from bot.utils import decorators
from bot.strings import Strings

logger = logging.getLogger(__name__)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_help_command(update: Update, _):
    logger.info('%d: /help', update.effective_user.id)

    update.message.reply_html(Strings.HELP_MESSAGE, disable_web_page_preview=True)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_start_command(update: Update, _):
    logger.info('%d: /start', update.effective_user.id)

    update.message.reply_markdown(Strings.START_MESSAGE, disable_web_page_preview=True)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_start_deeplink(update: Update, context: CallbackContext):
    logger.info('%d: /start deeplink', update.effective_user.id)

    topic = int(context.matches[0].group(1))

    release = db.get_release(topic, search_by='topic')

    release_string = Strings.RELEASE.format(**release)

    reply_markup = InlineKeyboard.release_info(release['id'], release['webarchive_url'])
    update.message.reply_html(release_string, disable_web_page_preview=True, reply_markup=reply_markup)


torrentsbot.add_handler(CommandHandler('help', on_help_command))
torrentsbot.add_handler(MessageHandler(Filters.regex(r'^\/start (\d+)'), on_start_deeplink))
torrentsbot.add_handler(CommandHandler('start', on_start_command))
