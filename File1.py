import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('CREATE INDEX idx_username ON Deers(username)')

connection.commit()
connection.close()

