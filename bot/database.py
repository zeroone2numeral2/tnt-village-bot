import logging

import simplesqlitewrap as ssw

from bot import sql
from bot.categories import CATEGORIE
from .utils import utils

logger = logging.getLogger(__name__)

DICT_FORMATTING = {
    'titolo': lambda release: release['titolo'],
    'titolo_escaped': lambda release: utils.escape(release['titolo']),
    'descrizione': lambda release: release['descrizione'],
    'descrizione_escaped': lambda release: utils.escape(release['descrizione']),
    'dimensione': lambda release: utils.human_readable_size(release['dimensione']) if release['dimensione'] else '? kb',
    'dimensione_no_decimal': lambda release: utils.human_readable_size(release['dimensione'], precision=0) if release['dimensione'] else '? kb',
    'autore': lambda release: release['autore'],
    'autore_escaped': lambda release: utils.html_escape(release['autore']),
    'categoria': lambda release: CATEGORIE[release['categoria']],
    'magnet': lambda release: 'magnet:?xt=urn:btih:{}'.format(release['hash']) if release['hash'] else 'non disponibile',
    'forum_url': lambda release: 'http://forum.tntvillage.scambioetico.org/index.php?showtopic={}'.format(release['topic']),
    'data': lambda release: release['data'],
    'topic': lambda release: release['topic'],
    'id': lambda release: release['id'],
    'hash': lambda release: release['hash'],
    'torrent_url': lambda release: release['torrent_url'] if release['torrent_url'] else 'non disponibile',
    'webarchive_url': lambda release: 'https://web.archive.org/web/http://forum.tntvillage.scambioetico.org/index.php?showtopic={}'.format(release['topic']),
}


class Database(ssw.Database):
    def __init__(self, filename):
        logger.debug('initializing Database module')

        ssw.Database.__init__(self, filename)

        self._init_db()

    def _init_db(self):
        logger.debug('creating tables')

        self._execute(sql.CREATE_TABLE_RELEASES)
        self._execute(sql.CREATE_TABLE_RELEASES_FTS)

    def search(self, query, allow_truncated_searches=True):
        query = query.strip('%')
        if allow_truncated_searches:
            # allow to search truncated queries too (see #2)
            query = '*{}*'.format(query)
    
        releases = self._execute(sql.SELECT_RELEASE, (query, query), fetchall=True, as_dict=True)

        return [{k: DICT_FORMATTING.get(k, lambda x: x[k])(release) for k, v in DICT_FORMATTING.items()} for release in releases]

    def topic_exists(self, topic):
        return bool(self._execute(sql.SELECT_GENERIC.format('topic'), (topic,), fetchone=True))
    
    def get_release(self, release_id, raw=False, search_by='id'):
        release_id = int(release_id)  # can also be the topic, it depends on the value of 'search_by'
        
        release = self._execute(sql.SELECT_GENERIC.format(search_by), (release_id,), fetchone=True, as_dict=True)

        if raw:
            return release

        return {k: DICT_FORMATTING.get(k, lambda x: x[k])(release) for k, v in DICT_FORMATTING.items()}

    def insert_torrents(self, torrents):
        if not isinstance(torrents, (list, tuple)):
            torrents = [torrents]

        inserted_rows = self._execute(sql.INSERT_TORRENTS, [t.db_tuple() for t in torrents], rowcount=True, many=True)
        logger.info('inserted %d rows', inserted_rows)

        inserted_rows = self._execute(sql.INSERT_TORRENTS_FTS, [(t.topic,) for t in torrents], rowcount=True, many=True)
        logger.info('FTS: inserted %d rows', inserted_rows)
