import sqlite3
import csv

from config import config

SQL_CREATE_TABLES = """CREATE TABLE IF NOT EXISTS releases (
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
);

CREATE VIRTUAL TABLE IF NOT EXISTS releases_fts
USING fts4(id, titolo, descrizione);
"""

SQL_INSERT = """INSERT OR IGNORE INTO releases (
    data,
    hash,
    topic,
    post,
    autore,
    titolo,
    descrizione,
    dimensione,
    categoria
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

FTS_INSERT = """INSERT INTO releases_fts (id, titolo, descrizione)
SELECT id, titolo, descrizione FROM releases;"""


def main():
    connection = sqlite3.connect(config.sqlite.filename)
    cursor = connection.cursor()

    cursor.executescript(SQL_CREATE_TABLES)
    connection.commit()

    with open('dump_release_tntvillage_2019-08-30.csv', encoding='utf8') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(read_csv):
            if not i:
                # skip header
                continue

            # YYYY-MM-DD HH:MM:SS
            row[0] = row[0].replace('T', ' ')  # row[0]: data della release, contiene una 'T' che possiamo rimuovere
            row[6] = row[6].lstrip('[').rstrip(']')  # row[6]: descrizione

            cursor.execute(SQL_INSERT, tuple(row))

    # build the full-text-search table
    cursor.execute(FTS_INSERT)

    connection.commit()


if __name__ == '__main__':
    main()
