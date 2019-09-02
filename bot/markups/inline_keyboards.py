# noinspection PyPackageRequirements
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboard:

    @staticmethod
    def forum_urls(forum_url, webarchive_url):
        markup= [[
            InlineKeyboardButton('forum', url=forum_url),
            InlineKeyboardButton('Wayback Machine', url=webarchive_url),
        ]]
        
        return InlineKeyboardMarkup(markup)
