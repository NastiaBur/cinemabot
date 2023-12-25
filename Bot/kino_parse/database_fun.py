import sqlite3
from logger.logger import db_logger
# Last Christmas I gave you my heart ...
# but the very next day you give it away



def user_exists(name):
    connector = sqlite3.connect("user_data.db")
    cur = connector.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS users
                (user_name TEXT, movie_name TEXT, genre TEXT, year TEXT, country TEXT)''')
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
    connector = sqlite3.connect("user_data.db")
    cur = connector.cursor()

    cur.execute(''' 
                INSERT INTO users (user_name, movie_name, genre, year, country) VALUES (?, ?, ?, ?, ?)
                ''', (name, movie, "None", "None", "None"))
    connector.commit()
    db_logger.debug(f"User {name} was added to the database with movie {movie}")
    cur.close()
    connector.close()

def user_update(name, item):
    connector = sqlite3.connect("user_data.db")
    cur = connector.cursor()

    cur.execute('''UPDATE users SET movie_name = ? WHERE user_name = ?''', (item, name))
    connector.commit()
    db_logger.debug(f"In user {name} setted new film {item}")

    cur.close()
    connector.close()

def choice_update(name, item, type):

    connector = sqlite3.connect("user_data.db")
    cur = connector.cursor()

    if type == "genre":
        cur.execute('''UPDATE users SET genre = ? WHERE user_name = ?''', (item, name))
        connector.commit()
        db_logger.debug(f"In user {name} setted new genre {item}")
    elif type == "year":
        cur.execute('''UPDATE users SET year = ? WHERE user_name = ?''', (item, name))
        connector.commit()
        db_logger.debug(f"In user {name} setted new year {item}")
    else:
        cur.execute('''UPDATE users SET country = ? WHERE user_name = ?''', (item, name))
        connector.commit()
        db_logger.debug(f"In user {name} setted new country {item}")

    cur.close()
    connector.close()


def get_movie(name):
    connector = sqlite3.connect("user_data.db")
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

def get_others(name):
    connector = sqlite3.connect("user_data.db")
    cur = connector.cursor()
    try:
        sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
        genre, year, country = "", "", ""
        for row in sm:
            genre, year, country = row[2], row[3], row[4]
            break
    except sqlite3.OperationalError:
        db_logger.error("There is no such user in database")
        genre, year, country = None, None, None

    cur.close()
    connector.close()
    return genre, year, country
