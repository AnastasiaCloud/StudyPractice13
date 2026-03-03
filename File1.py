import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

try:
    cursor.execute('BEGIN')
    cursor.execute('INSERT INTO Users (username, email) VALUES (?,?)', ('user1', 'user1@example.com'))
    cursor.execute('INSERT INTO Users (username, email) VALUES (?,?)', ('user2', 'user2@example.com'))

    cursor.execute('COMMIT')
except:
    cursor.execute('ROLLBACK')

connection.close()
