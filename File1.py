import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.close()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER)
''')

cursor.execute('CREATE INDEX idx_email ON Users (email)')

cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuser', 'newuser@example.com', 28))

cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'newuser'))

connection.commit()
connection.close()
