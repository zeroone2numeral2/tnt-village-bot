import logging
import re

# noinspection PyPackageRequirements
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
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
from ..utils import utils

logger = logging.getLogger(__name__)

WAITING_RELEASE = range(1)

CATEGORIE = {
    1: 'Film TV e programmi',
    2: 'Musica',
    3: 'E Books',
    4: 'Film',
    6: 'Linux',
    7: 'Anime',
    8: 'Cartoni',
    9: 'Macintosh',
    10: 'Windows Software',
    11: 'Pc Game',
    12: 'Playstation',
    13: 'Students Releases',
    14: 'Documentari',
    21: 'Video Musicali',
    22: 'Sport',
    23: 'Teatro',
    24: 'Wrestling',
    25: 'Varie',
    26: 'Xbox',
    27: 'Immagini sfondi',
    28: 'Altri Giochi',
    29: 'Serie TV',
    30: 'Fumetteria',
    31: 'Trash',
    32: 'Nintendo',
    34: 'A Book',
    35: 'Podc: st',
    36: 'Edicola',
    37: 'Mobile'
}


def search_release(update: Update, status_to_return_on_invalid_query=ConversationHandler.END):
    if len(update.message.text) < 3:
        update.message.reply_text(Strings.RELEASE_TOO_SHORT)
        return status_to_return_on_invalid_query

    releases = db.search(update.message.text, as_dict=True)[:64]
    if not releases:
        update.message.reply_text(Strings.RELEASES_EMPTY, reply_markup=Keyboard.HIDE, quote=True)

        return status_to_return_on_invalid_query
    else:
        markup = Keyboard.from_list(['{id}. {titolo}'.format(**release) for release in releases])
        update.message.reply_text(Strings.SELECT_RELEASE, reply_markup=markup)

        return WAITING_RELEASE


@decorators.action(ChatAction.TYPING)
@decorators.restricted
@decorators.failwithmessage
def on_search_query(update: Update, _):
    logger.info('%d: search query', update.effective_user.id)
    
    return search_release(update, ConversationHandler.END)


@decorators.action(ChatAction.TYPING)
@decorators.failwithmessage
def on_release_selected(update: Update, context: CallbackContext):
    logger.info('%d: user selected the release from the keyboard', update.effective_user.id)

    release_match = re.search(r'^(\d+)\.\s.*', update.message.text)
    if not release_match:
        # user changed his query
        return search_release(update, WAITING_RELEASE)
    
    release_id = release_match.group(1)
    release = db.release_by_id(release_id, as_dict=True)
    
    forum_url = 'http://forum.tntvillage.scambioetico.org/index.php?showtopic={}'.format(release['topic'])
    release_string = Strings.RELEASE.format(
        titolo=utils.html_escape(release['titolo']),
        descrizione=utils.html_escape(release['descrizione']),
        dimensione=utils.human_readable_size(release['dimensione']),
        autore=utils.html_escape(release['autore']),
        categoria=CATEGORIE[release['categoria']],
        data=release['data'],
        magnet='magnet:?xt=urn:btih:{}'.format(release['hash'])
        # forum_url=forum_url,
        # webarchive_url='https://web.archive.org/web/{}'.format(forum_url)
    )
    
    reply_markup = InlineKeyboard.forum_urls(forum_url, 'https://web.archive.org/web/{}'.format(forum_url))
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
