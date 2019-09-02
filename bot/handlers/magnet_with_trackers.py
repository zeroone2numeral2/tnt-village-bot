import logging

# noinspection PyPackageRequirements
from telegram.ext import (
    CallbackQueryHandler,
    CallbackContext
)
# noinspection PyPackageRequirements
from telegram import (
    Update,
    ParseMode
)
from bot import torrentsbot
from bot import db
from bot.markups import InlineKeyboard
from bot.strings import Strings
from ..utils import decorators

logger = logging.getLogger(__name__)

TRACKERS = (
    'http://tracker.tntvillage.scambioetico.org:2710/announce',
    'udp://tracker.tntvillage.scambioetico.org:2710/announce',
    'udp://tracker.coppersurfer.tk:6969/announce',
    'udp://tracker.leechers-paradise.org:6969/announce',
    'udp://IPv6.leechers-paradise.org:6969/announce',
    'udp://tracker.internetwarriors.net:1337/announce',
    'udp://tracker.tiny-vps.com:6969/announce',
    'udp://tracker.mg64.net:2710/announce',
    'udp://tracker.openbittorrent.com:80/announce',
)

MAGNET_TEXT = """<code>magnet:?xt=urn:btih:{hash}&tr={trackers_list}</code>"""


@decorators.restricted
@decorators.failwithmessage
def on_expand_magnet_button(update: Update, context: CallbackContext):
    logger.info('%d: magnet with trackers button', update.effective_user.id)

    release_id = context.match[1]
    release = db.release_by_id(release_id)

    reply_markup = InlineKeyboard.collapse_magnet_button(release_id)
    update.callback_query.edit_message_text(
        MAGNET_TEXT.format(hash=release['hash'], trackers_list='&tr='.join(TRACKERS)),
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    update.callback_query.answer(Strings.CB_ANSWER_TRACKERS)


@decorators.restricted
@decorators.failwithmessage
def on_collapse_button(update: Update, context: CallbackContext):
    logger.info('%d: collapse button', update.effective_user.id)

    release_id = context.match[1]
    release = db.release_by_id(release_id)

    update.callback_query.edit_message_text(
        Strings.RELEASE.format(**release),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboard.release_info(release_id, release['webarchive_url']),
        parse_mode=ParseMode.HTML
    )
    update.callback_query.answer(Strings.CB_ANSWER_COLLAPSED)


torrentsbot.add_handler(CallbackQueryHandler(on_expand_magnet_button, pattern=r'expandmagnet:(\d+)', pass_groups=True))
torrentsbot.add_handler(CallbackQueryHandler(on_collapse_button, pattern=r'collapse:(\d+)', pass_groups=True))
