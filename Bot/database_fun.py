import sqlite3
#Last Christmas I gave you my heart ...
def user_exists(name):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS users
                (user_name TEXT, movie_name TEXT)''')
    conn.commit()

    sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
    count = 0
    for _ in sm:
        count += 1
    cur.close()
    conn.close()

    if count > 0:
        return True
    return False


def user_add(name, movie):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute(''' 
                INSERT INTO users (user_name, movie_name) VALUES (?, ?)
                ''', (name, movie))
    conn.commit()

    cur.close()
    conn.close()

def user_update(name, movie):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute('''UPDATE users SET movie_name = ? WHERE user_name = ?''', (movie, name))
    conn.commit()

    cur.close()
    conn.close()

def get_movie(name):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    sm = cur.execute("SELECT * FROM users WHERE user_name=?", (name, ))
    film = ""
    for row in sm:
        film = row[1]
        break

    cur.close()
    conn.close()
    return film
