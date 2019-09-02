import sqlite3
import csv

from config import config


SQL_CREATE = """CREATE TABLE IF NOT EXISTS releases (
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


def main():
    connection = sqlite3.connect(config.sqlite.filename)
    cursor = connection.cursor()
    
    cursor.execute(SQL_CREATE)
    connection.commit()
    
    with open('dump_release_tntvillage_2019-08-30.csv', encoding='utf8') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(read_csv):
            if not i:
                # skip header
                continue
                
            # YYYY-MM-DD HH:MM:SS
            row[0] = row[0].replace('T', ' ')
            
            cursor.execute(SQL_INSERT, tuple(row))
    
    connection.commit()


if __name__ == '__main__':
    main()
