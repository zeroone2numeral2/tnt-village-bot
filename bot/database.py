import logging

import simplesqlitewrap as ssw

from bot import sql

logger = logging.getLogger(__name__)


class Database(ssw.Database):
    def __init__(self, filename):
        logger.debug('initing Database module')

        ssw.Database.__init__(self, filename)

        self._init_db()

    def _init_db(self):
        logger.debug('creating tables')

        self._execute(sql.CREATE_TABLE_RELEASES)

    def search(self, query, **kwargs):
        query = query.strip('%')
        query = '%{}%'.format(query)
    
        return self._execute(sql.SELECT_RELEASE, (query, query), fetchall=True, **kwargs)
    
    def release_by_id(self, release_id, **kwargs):
        release_id = int(release_id)
        
        return self._execute(sql.SELECT_RELEASE_ID, (release_id,), fetchone=True, **kwargs)
