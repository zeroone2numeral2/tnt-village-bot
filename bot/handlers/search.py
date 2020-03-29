import logging
import re

# noinspection PyPackageRequirements
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters
)
# noinspection PyPackageRequirements
from telegram import ChatAction, Update

from bot import torrentsbot
from bot.strings import Strings
from bot import db
from bot.markups import Keyboard
from bot.markups import InlineKeyboard
from .fallback_commands import cancel_command
from ..utils import decorators

logger = logging.getLogger(__name__)

WAITING_RELEASE = range(1)


def search_release(update: Update, status_to_return_on_invalid_query=ConversationHandler.END):
    if len(update.message.text) < 3:
        update.message.reply_text(Strings.RELEASE_TOO_SHORT)
        return status_to_return_on_invalid_query

    releases = db.search(update.message.text)[:64]
    if not releases:
        update.message.reply_text(Strings.RELEASES_EMPTY, reply_markup=Keyboard.HIDE, quote=True)

        return status_to_return_on_invalid_query
    else:
        markup = Keyboard.from_list(['{id}. {titolo} • {dimensione_no_decimal} [{descrizione}]'.format(**release) for release in releases])
        update.message.reply_text(Strings.SELECT_RELEASE, reply_markup=markup)

        return WAITING_RELEASE


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_search_query(update: Update, _):
    logger.info('%d: search query', update.effective_user.id)
    
    return search_release(update, ConversationHandler.END)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_release_selected(update: Update, _):
    logger.info('%d: user selected the release from the keyboard', update.effective_user.id)

    release_match = re.search(r'^(\d+)\.\s.*', update.message.text)
    if not release_match:
        # user changed his query
        return search_release(update, WAITING_RELEASE)
    
    release_id = release_match.group(1)
    release = db.release_by_id(release_id)
    
    release_string = Strings.RELEASE.format(**release)
    
    reply_markup = InlineKeyboard.release_info(release_id, release['webarchive_url'])
    update.message.reply_html(release_string, disable_web_page_preview=True, reply_markup=reply_markup)

    return WAITING_RELEASE


torrentsbot.add_handler(ConversationHandler(
    name='searching_releases',
    entry_points=[MessageHandler(Filters.text, on_search_query)],
    states={
        WAITING_RELEASE: [MessageHandler(Filters.text, on_release_selected)]
    },
    fallbacks=[CommandHandler(['annulla', 'fatto'], cancel_command)]
))
