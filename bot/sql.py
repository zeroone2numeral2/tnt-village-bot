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
    categoria INT

);"""

SELECT_RELEASE = """SELECT *
FROM releases
WHERE id IN
    (SELECT id
     FROM releases_fts
     WHERE titolo MATCH ? OR descrizione MATCH ?
     LIMIT 80)
ORDER BY titolo;"""

SELECT_RELEASE_ID = """SELECT *
FROM releases
WHERE id = ?;"""
