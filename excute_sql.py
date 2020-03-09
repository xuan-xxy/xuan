
import sqlite3

def get_db():
    conn = sqlite3.connect('create.db', check_same_thread=False)
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory
    cursor = conn.cursor()
    return conn, cursor


# conn, cursor = get_db()
# sql ="""CREATE TABLE article (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   author_id INTEGER NOT NULL,
#   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   title TEXT NOT NULL,
#   body TEXT NOT NULL,
#   FOREIGN KEY (author_id) REFERENCES user (id)
# )"""
#
# cursor.execute(sql)
