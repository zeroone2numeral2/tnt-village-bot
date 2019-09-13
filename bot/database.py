import logging

import simplesqlitewrap as ssw

from bot import sql
from .utils import utils

logger = logging.getLogger(__name__)


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

DICT_FORMATTING = {
    'titolo': lambda release: release['titolo'],
    'titolo_escaped': lambda release: utils.escape(release['titolo']),
    'descrizione': lambda release: release['descrizione'],
    'descrizione_escaped': lambda release: utils.escape(release['descrizione']),
    'dimensione': lambda release: utils.human_readable_size(release['dimensione']),
    'dimensione_no_decimal': lambda release: utils.human_readable_size(release['dimensione'], precision=0),
    'autore': lambda release: release['autore'],
    'autore_escaped': lambda release: utils.html_escape(release['autore']),
    'categoria': lambda release: CATEGORIE[release['categoria']],
    'magnet': lambda release: 'magnet:?xt=urn:btih:{}'.format(release['hash']),
    'forum_url': lambda release: 'http://forum.tntvillage.scambioetico.org/index.php?showtopic={}'.format(release['topic']),
    'data': lambda release: release['data'],
    'topic': lambda release: release['topic'],
    'id': lambda release: release['id'],
    'hash': lambda release: release['hash'],
    'webarchive_url': lambda release: 'https://web.archive.org/web/http://forum.tntvillage.scambioetico.org/index.php?showtopic={}'.format(release['topic']),
}


class Database(ssw.Database):
    def __init__(self, filename):
        logger.debug('initing Database module')

        ssw.Database.__init__(self, filename)

        self._init_db()

    def _init_db(self):
        logger.debug('creating tables')

        self._execute(sql.CREATE_TABLE_RELEASES)

    def search(self, query):
        query = query.strip('%')
    
        releases = self._execute(sql.SELECT_RELEASE, (query, query), fetchall=True, as_dict=True)

        return [{k: DICT_FORMATTING.get(k, lambda x: x[k])(release) for k, v in DICT_FORMATTING.items()} for release in releases]
    
    def release_by_id(self, release_id):
        release_id = int(release_id)
        
        release = self._execute(sql.SELECT_RELEASE_ID, (release_id,), fetchone=True, as_dict=True)

        return {k: DICT_FORMATTING.get(k, lambda x: x[k])(release) for k, v in DICT_FORMATTING.items()}
