CREATE_TABLE_RELEASES = """CREATE TABLE IF NOT EXISTS releases (
    id INTEGER PRIMARY KEY,
    data TEXT,
    hash TEXT,
    topic INT,
    post INT,
    autore TEXT,
    titolo TEXT,
    descrizione TEXT,
    dimensione INT,
    categoria INT,

    -- custom
    magnet TEXT,
    torrent_url TEXT
);"""

CREATE_TABLE_RELEASES_FTS = """CREATE VIRTUAL TABLE IF NOT EXISTS releases_fts
USING fts4(id, titolo, descrizione);"""

SELECT_RELEASE = """SELECT *
FROM releases
WHERE id IN
    (SELECT id
     FROM releases_fts
     WHERE titolo MATCH ? OR descrizione MATCH ?
     LIMIT 80)
ORDER BY titolo;"""

SELECT_GENERIC = """SELECT *
FROM releases
WHERE {} = ?;"""

INSERT_TORRENTS = """INSERT OR IGNORE INTO releases (
    data,
    hash,
    topic,
    post,
    autore,
    titolo,
    descrizione,
    dimensione,
    categoria,
    hash,
    torrent_url
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

INSERT_TORRENTS_FTS = """INSERT INTO releases_fts (id, titolo, descrizione)
SELECT id, titolo, descrizione FROM releases WHERE topic = ?;"""
