import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Deers (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_created_at
AFTER INSERT ON Deers
BEGIN
UPDATE Deers SET created_at = CURRENT_TIMESTAMP WHERE
id = NEW.id;
END;
''')
connection.commit()
connection.close()

