import sqlite3

conn = sqlite3.connect('sigfrota.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(usuarios)")
for row in cursor.fetchall():
    print(row)
conn.close()
