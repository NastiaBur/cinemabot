import sqlite3
from logger import db_logger
# Last Christmas I gave you my heart ...
# but the very next day you give it away
def user_exists(name):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS users
                (user_name TEXT, movie_name TEXT, genre TEXT)''')
    connector.commit()

    sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
    count = 0
    for _ in sm:
        count += 1
    cur.close()
    connector.close()

    if count > 0:
        return True
    return False


def user_add(name, movie):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()

    cur.execute(''' 
                INSERT INTO users (user_name, movie_name, genre) VALUES (?, ?, ?)
                ''', (name, movie, "None"))
    connector.commit()
    db_logger.debug(f"User {name} was added to the database with movie {movie}")
    cur.close()
    connector.close()

def user_update(name, movie):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()

    cur.execute('''UPDATE users SET movie_name = ? WHERE user_name = ?''', (movie, name))
    connector.commit()
    db_logger.debug(f"In user {name} setted new film {movie}")
    cur.close()
    connector.close()

def genre_update(name, genre):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()

    cur.execute('''UPDATE users SET genre = ? WHERE user_name = ?''', (genre, name))
    connector.commit()
    db_logger.debug(f"In user {name} setted new genre {genre}")
    cur.close()
    connector.close()

def get_movie(name):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()
    try:
        sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
        film = ""
        for row in sm:
            film = row[1]
            break
    except sqlite3.OperationalError:
        db_logger.error("There is no such user in database")
        film = None

    cur.close()
    connector.close()
    return film

def get_genre(name):
    connector = sqlite3.connect("db.db")
    cur = connector.cursor()
    try:
        sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
        genre = ""
        for row in sm:
            genre = row[2]
            break
    except sqlite3.OperationalError:
        db_logger.error("There is no such user in database")
        genre = None

    cur.close()
    connector.close()
    return genre
