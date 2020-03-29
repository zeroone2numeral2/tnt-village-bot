import datetime
import logging
import re
import csv
import time
import threading
from pprint import pprint

import feedparser
import requests
from bs4 import BeautifulSoup
from telegram import Bot, ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.ext import CallbackContext

from bot import torrentsbot
from bot import db
from bot.categories import CATEGORIE
from bot.markups import InlineKeyboard
from bot.utils import utils
from bot.utils import decorators
from bot.strings import Strings
from config import config

logger = logging.getLogger(__name__)

FEED_URL = 'http://tntvillage.scambioetico.org/rss.php?c=0&p=10'


class Torrent:
    __SLOTHS__ = ['data', 'hash', 'topic', 'post', 'autore', 'titolo', 'descrizione', 'categoria', 'title_full',
                  'published', 'published_parsed', 'magnet', 'magnet_short', 'other_urls', 'torrent_url']

    def __init__(self, entry):
        # così come erano ordinati nel csv
        # self.data = entry.published_parsed.strftime("%Y-%m-%d %H:%M:%S"),
        self.data = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)
        self.hash = None
        self.topic = None
        self.post = None
        self.autore = entry.author
        self.titolo = None
        self.descrizione = None
        self.dimensione = None
        self.categoria = int(entry.tags[0]['term'])

        self.title_full = entry.title
        self.published = entry.published
        self.published_parsed = entry.published_parsed
        self.magnet = None
        self.magnet_short = None
        self.other_urls = list()
        self.deeplink = 'https://t.me/{}?start={}'.format(torrentsbot.bot.username, self.topic)

        match = re.search(r'(.*)\s\[(.*)\]$', entry.title, re.I)
        self.titolo = match.group(1).strip()
        self.descrizione = match.group(2).strip()

        for link in entry.links:
            if link['rel'] == 'alternate':
                self.forum_url = link['href']
                self.topic = int(re.search(r'=(\d+)$', link['href']).group(1))
            elif link['rel'] == 'enclosure':
                self.torrent_url = link['href']
                self.post = int(re.search(r'id=(\d+)$', link['href']).group(1))
            else:
                self.other_urls.append(link['href'])

    @property
    def dimensione_pretty(self):
        if not self.dimensione:
            return '? bytes'

        return utils.human_readable_size(self.dimensione)

    @property
    def categoria_pretty(self):
        if not self.categoria:
            return 'sconosciuta'

        return CATEGORIE[self.categoria]

    def set_magnet(self, magnet_url):
        self.magnet = magnet_url
        self.hash = re.search(r'magnet:\?xt=urn:btih:(\w+)&', self.magnet, re.I).group(1)
        self.magnet_short = 'magnet:?xt=urn:btih:{}'.format(self.hash)

    def db_tuple(self, magnet=True, torrent_url=True):
        result_list = [
            self.data,
            self.hash,
            self.topic,
            self.post,
            self.autore,
            self.titolo,
            self.descrizione,
            self.dimensione,
            self.categoria
        ]

        if magnet:
            result_list.append(self.magnet)

        if torrent_url:
            result_list.append(self.torrent_url)

        return tuple(result_list)

    def format_dict(self):
        ignored_properties = ('other_urls',)
        virtual_properties = ['dimensione_pretty', 'categoria_pretty']
        return {k: getattr(self, k) for k in self.__SLOTHS__ + virtual_properties if k not in ignored_properties}

    def __repr__(self):
        base_string = 'Torrent({})'
        properties = list()
        for key in self.__SLOTHS__:
            properties.append('{}: {}'.format(key, getattr(self, key)))

        return base_string.format(', '.join(properties))


def request_page(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    result = requests.get(
        url,
        headers={'User-Agent': user_agent}
    )

    return result.text


def entry_to_torrent(entry, fetch_forum_page=True):
    # pprint(entry)

    torrent = Torrent(entry)

    if db.topic_exists(torrent.topic):
        logger.info('torrent %s (topic: %d) already in the db, ignoring...', torrent.titolo, torrent.topic)
        return

    if fetch_forum_page:
        time.sleep(1)

        try:
            logger.info('requesting %s...', torrent.forum_url)

            start_time = time.time()
            html_page = request_page(torrent.forum_url)
            logger.info('request took %s seconds', time.time() - start_time)
        except Exception as e:
            logger.error('error while fetching forum page (%s): %s', torrent.forum_url, str(e), exc_info=True)
            return torrent

        soup = BeautifulSoup(html_page, features='html.parser')

        links = soup.find_all('a', {'title': 'Magnet link'})
        torrent.set_magnet(links[0]['href'])

        divs = soup.find_all('div')
        for div in divs:
            if 'Dimensione:' in div.text:
                match = re.search(r'.*Dimensione: ([\d,]+) bytes.*', div.text, re.I)
                if not match:
                    continue

                torrent.dimensione = int(match.group(1).replace(',', ''))
                break

    return torrent


def write_to_csv(torrents):
    logger.info('writing data to csv...')

    with open('incremental_releases.csv', 'a', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([t.db_tuple(magnet=False, torrent_url=False) for t in torrents])

    logger.info('completed')


def post_to_channel(bot: Bot, torrents: [Torrent]):
    if not config.feedsjob.get('new_torrents_notifications', None):
        logger.info('new releases notifications are disabled')
        return

    for torrent in torrents:
        logger.info('posting to channel topic %d...', torrent.topic)
        text = Strings.CHANNEL_NOTIFICATION_TEMPLATE.format(**torrent.format_dict())
        try:
            bot.send_message(
                config.feedsjob.new_torrents_notifications,
                text,
                parse_mode=ParseMode.HTML,
                disable_notification=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboard.release_deeplink(torrent.deeplink)
            )
        except (BadRequest, TelegramError) as e:
            logger.error('error while posting message to channel: %s', e.message)

        time.sleep(3)


@decorators.failwithmessage_job
def feeds_job(context: CallbackContext):
    logger.info('starting job')
    start_time = time.time()

    try:
        feed = feedparser.parse(FEED_URL)
    except Exception as e:
        logger.error('error while getting the feeds: %s', str(e), exc_info=True)
        return

    logger.info('fetched %d entries:', len(feed.entries))
    for i, entry in enumerate(feed.entries):
        # this is for debug purposes
        logger.info('%d. %s (%s)', i + 1, entry.title, entry.published)

    # if not feed.version:
    #     print('No feed.version:', feed_url)
    #     return

    new_torrents = list()
    for entry in feed.entries:
        torrent = entry_to_torrent(entry)
        if not torrent:
            # the torrent's topic (numeric) is already in the database
            continue

        logger.info('torrent %s (topic: %d) is new', torrent.titolo, torrent.topic)
        new_torrents.append(torrent)

        if not torrent.magnet:
            # we insert torrents without a magnet anyway because there should be a link to the torrent file
            # there should be a job that queries the db for magnet-less torrent and should try to fetch them again
            logger.warning('WARNING! We haven\'t been able to fetch a magnet for this torrent')

    if new_torrents:
        logger.info("%d new torrents to insert, %d of them don't have a magnet", len(new_torrents), len([t for t in new_torrents if not t.magnet]))
        with threading.Lock():
            db.insert_torrents(new_torrents)

        write_to_csv(new_torrents)
        post_to_channel(context.bot, new_torrents)
    else:
        logger.info('no new torrents to insert')

    logger.info('job executed in %s seconds', time.time() - start_time)


torrentsbot.register_job(feeds_job, interval=config.feedsjob.interval*60, first=config.feedsjob.first*60)
