import logging
from functools import wraps
from html import escape as html_escape

# noinspection PyPackageRequirements
from telegram import Update, ParseMode
# noinspection PyPackageRequirements
from telegram.error import TimedOut
from telegram.ext import CallbackContext

from config import config

logger = logging.getLogger(__name__)


def action(chat_action):
    def real_decorator(func):
        @wraps(func)
        def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
            context.bot.send_chat_action(update.effective_chat.id, chat_action)
            return func(update, context, *args, **kwargs)

        return wrapped

    return real_decorator


def failwithmessage(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return func(update, context, *args, **kwargs)
        except TimedOut:
            logger.error('TimedOut error')
            # memo: timed out errors break conversation handlers because the new state isn't returned
        except Exception as e:
            logger.error('unexpected error while running handler callback: %s', str(e), exc_info=True)
            text = 'An error occurred while processing the message: <code>{}</code>'.format(html_escape(str(e)))
            if update.callback_query:
                update.callback_query.message.reply_html(text)
            else:
                update.message.reply_html(text)

    return wrapped


def failwithmessage_job(func):
    @wraps(func)
    def wrapped(context: CallbackContext, *args, **kwargs):
        try:
            return func(context, *args, **kwargs)
        except Exception as e:
            logger.error('unexpected error while executing a job: %s', str(e), exc_info=True)
            text = 'An error occurred while executing a job: <code>{}</code>'.format(html_escape(str(e)))
            if config.telegram.get('unexpected_exceptions_notifications', None):
                context.bot.send_message(config.telegram.unexpected_exceptions_notifications, text, parse_mode=ParseMode.HTML)

    return wrapped
