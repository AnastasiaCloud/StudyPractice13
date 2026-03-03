import sqlite3

with sqlite3.connect('my_database.db') as connection:
    cursor = connection.cursor()

    try:
        with connection:
        cursor.execute('INSERT INTO Users (username, email) VALUES (?,?)', ('user3', 'user3@example.com'))
        cursor.execute('INSERT INTO Users (username, email) VALUES (?,?)', ('user4', 'user4@example.com'))

    except:
        pass

