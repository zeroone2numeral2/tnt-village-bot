# noinspection PyPackageRequirements
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboard:

    @staticmethod
    def release_info(release_id, webarchive_url):
        markup= [[
            InlineKeyboardButton('Wayback Machine', url=webarchive_url),
            InlineKeyboardButton('magnet con trackers', callback_data='expandmagnet:{}'.format(release_id)),
        ]]
        
        return InlineKeyboardMarkup(markup)

    @staticmethod
    def collapse_magnet_button(release_id):
        return InlineKeyboardMarkup([[
            InlineKeyboardButton('comprimi', callback_data='collapse:{}'.format(release_id))
        ]])
