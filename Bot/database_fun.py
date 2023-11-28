import sqlite3

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





# conn = sqlite3.connect("db.db")

# cur = conn.cursor()

# cur.execute(''' CREATE TABLE IF NOT EXISTS users
#             (user_name TEXT, movie_name TEXT)''')
# conn.commit()
# name_list = [
#     ('a', 'aa'),
#     ('b', 'bb'),
#     ('c', 'cc')
# ]
# cur.executemany(''' 
#                 INSERT INTO users (user_name, movie_name) VALUES (?, ?)
#                 ''', name_list)

# conn.commit()
# sm = cur.execute("SELECT * FROM users")
# for row in sm:
#     row

# newPrice = 'aaaa'
# book_id = 'a'
# cur.execute('''UPDATE users SET movie_name = ? WHERE user_name = ?''', (newPrice, book_id))

# sm = cur.execute("SELECT * FROM users")
# for row in sm:
#     print(row)
# sm = cur.fetchall("SELECT * FROM users WHERE user_name=?", "a")
# for row in sm:
#     print(row)

# sm = cur.execute("SELECT * FROM users")
# for row in sm:
#     print(row)

# cur.execute(''' 
#                 INSERT INTO users (user_name, movie_name) VALUES (?, ?)
#                 ''', ('a', 'aa'))
# sm = cur.execute("SELECT * FROM users")
# for row in sm:
#     print(row)

# conn.commit()

# cur.close()
# conn.close()